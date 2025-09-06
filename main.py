# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List, Tuple, Optional
from threading import Thread
from functools import partial

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

# ------------------------------------------------------------
#  Puzzle model & solver (Water-Sort / Civata renk istifleme)
# ------------------------------------------------------------

ColorId = int                   # 1..N (0 = boş yok)
Move = Tuple[int, int, int]     # (src, dst, kaç parça)

def is_uniform_full(col: List[ColorId], H: int) -> bool:
    return len(col) == H and (len(col) == 0 or all(x == col[0] for x in col))

def is_solved(state: List[List[ColorId]], H: int) -> bool:
    for col in state:
        if len(col) == 0:
            continue
        if not is_uniform_full(col, H):
            return False
    return True

def canonical(state: List[List[ColorId]]) -> Tuple[Tuple[ColorId, ...], ...]:
    return tuple(tuple(c) for c in state)

def legal_moves(state: List[List[ColorId]], H: int, last: Optional[Tuple[int,int]]=None):
    n = len(state)
    for i in range(n):
        if not state[i]:
            continue
        if is_uniform_full(state[i], H):
            continue
        top = state[i][-1]
        # blok uzunluğu (üstte bitişik aynı renk kaç tane)
        block = 1
        for k in range(len(state[i]) - 2, -1, -1):
            if state[i][k] == top:
                block += 1
            else:
                break
        for j in range(n):
            if i == j: 
                continue
            # hemen geri alma hamlesini azalt
            if last and last == (j, i) and len(state[j]) and (not state[i] or state[i][-1] == state[j][-1]):
                continue
            if len(state[j]) == H:
                continue
            if state[j] and state[j][-1] != top:
                continue
            room = H - len(state[j])
            take = min(block, room)
            if take <= 0:
                continue
            yield (i, j, take)

def apply_move(state: List[List[ColorId]], mv: Move) -> List[List[ColorId]]:
    i, j, k = mv
    ns = [c[:] for c in state]
    moved = []
    for _ in range(k):
        if not ns[i]:
            break
        if ns[j] and ns[j][-1] != ns[i][-1]:
            break
        moved.append(ns[i].pop())
        ns[j].append(moved[-1])
    return ns

def solve_iterative_deepening(start: List[List[ColorId]], H: int, max_depth=80) -> Optional[List[Move]]:
    """
    Oldukça genel ve sağlam bir çözücü.
    DFS + iteratif derinleşme, ziyaret kümesi ve basit kırpmalar.
    """
    target_key = None  # sadece visited için
    start_key = canonical(start)

    for limit in range(0, max_depth + 1):
        visited = set()
        path: List[Move] = []

        def dfs(state, depth, last=None):
            key = canonical(state)
            if key in visited:
                return None
            visited.add(key)

            if is_solved(state, H):
                return list(path)
            if depth == 0:
                return None

            # küçük sezgisel sıralama: boşalan/tek renge yaklaşan varışları öne al
            ms = list(legal_moves(state, H, last))
            def score(m):
                i, j, k = m
                after = apply_move(state, m)
                good = 0
                if is_uniform_full(after[j], H):
                    good += 3
                if len(after[i]) == 0:
                    good += 2
                if len(after[j]) > 0:
                    # varışta tek renk mi?
                    t = after[j][-1]
                    if all(x == t for x in after[j]):
                        good += 1
                return -good  # küçükten büyüğe sıralıyor, eksi ile tersle
            ms.sort(key=score)

            for m in ms:
                path.append(m)
                res = dfs(apply_move(state, m), depth - 1, last=(m[0], m[1]))
                if res is not None:
                    return res
                path.pop()
            return None

        ans = dfs(start, limit)
        if ans is not None:
            return ans
    return None

# ------------------------------------------------------------
#  UI
# ------------------------------------------------------------

# Renk paleti (id -> (adı, RGBA))
PALETTE = {
    1: ("Blue",   (0.16, 0.52, 0.97, 1)),
    2: ("Yellow", (0.98, 0.80, 0.10, 1)),
    3: ("Red",    (0.95, 0.25, 0.25, 1)),
    4: ("Green",  (0.25, 0.75, 0.45, 1)),
    5: ("Purple", (0.55, 0.40, 0.90, 1)),
    6: ("Cyan",   (0.20, 0.85, 0.85, 1)),
    7: ("Orange", (0.99, 0.55, 0.10, 1)),
    8: ("Gray",   (0.70, 0.70, 0.75, 1)),
}

class ColumnWidget(Button):
    def __init__(self, capacity: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capacity = capacity
        self.stack: List[ColorId] = []
        self.background_color = (0, 0, 0, 0)
        self.border = (0, 0, 0, 0)
        self.update_canvas()

    def clear_stack(self):
        self.stack = []
        self.update_canvas()

    def push(self, cid: ColorId):
        if len(self.stack) < self.capacity:
            if len(self.stack) == 0 or self.stack[-1] == cid:
                self.stack.append(cid)
                self.update_canvas()

    def pop(self) -> Optional[ColorId]:
        if self.stack:
            c = self.stack.pop()
            self.update_canvas()
            return c
        return None

    def update_canvas(self, *_):
        self.canvas.after.clear()
        with self.canvas.after:
            # sütun çerçevesi
            Color(0.9, 0.9, 0.95, 1); RoundedRectangle(radius=[12,], pos=self.pos, size=self.size)
        # iç kısımda pulları çiz
        def _draw(*_):
            self.canvas.before.clear()
            with self.canvas.before:
                pad = 8
                cell_h = (self.height - 2*pad) / self.capacity
                x = self.x + pad
                y = self.y + pad
                w = self.width - 2*pad
                # zemin
                Color(0.12, 0.12, 0.16, 1)
                RoundedRectangle(pos=(self.x, self.y), size=(self.width, self.height), radius=[12,])
                # her parça
                for idx, cid in enumerate(self.stack):
                    c = PALETTE.get(cid, ("?", (0.8, 0.8, 0.8, 1)))[1]
                    Color(*c)
                    RoundedRectangle(pos=(x, y + idx*cell_h), size=(w, cell_h-2), radius=[8,])
        Clock.schedule_once(_draw, 0)

    def on_size(self, *_):
        self.update_canvas()

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.capacity = 4
        self.cols = 6

        # üst kontrol barı
        top = BoxLayout(size_hint_y=None, height=56, spacing=6, padding=6)
        self.add_widget(top)

        self.info = Label(text="Civata Bot • Edit mode: add/remove, Solve ile çöz", halign="left", valign="middle")
        self.info.bind(size=lambda *_: setattr(self.info, 'text_size', self.info.size))
        top.add_widget(self.info)

        self.edit_toggle = ToggleButton(text="Edit", state="down", size_hint_x=None, width=80)
        top.add_widget(self.edit_toggle)

        self.solve_btn = Button(text="Solve", size_hint_x=None, width=90, on_release=self.on_solve)
        top.add_widget(self.solve_btn)

        self.play_btn = Button(text="Play ▶", size_hint_x=None, width=90, on_release=self.on_play, disabled=True)
        top.add_widget(self.play_btn)

        # palet
        pal = BoxLayout(size_hint_y=None, height=56, spacing=6, padding=[6,0,6,6])
        self.add_widget(pal)
        self.active_color: ColorId = 1
        for cid, (name, rgba) in list(PALETTE.items())[:6]:
            b = ToggleButton(text=name, group="pal", size_hint_x=None, width=100)
            def _make_setter(c=cid):
                def _on(but):
                    if but.state == "down":
                        self.active_color = c
                return _on
            b.bind(on_release=_make_setter(cid))
            pal.add_widget(b)
            if cid == self.active_color:
                b.state = "down"

        # saha
        wrap = ScrollView()
        self.add_widget(wrap)
        self.grid = GridLayout(cols=self.cols, padding=8, spacing=8, size_hint_y=None)
        self.grid.bind(minimum_height=lambda _, h: setattr(self.grid, 'height', h))
        wrap.add_widget(self.grid)

        self.columns: List[ColumnWidget] = []
        self.solution: Optional[List[Move]] = None
        self.sol_step = 0

        self.build_board(cols=self.cols, capacity=self.capacity)
        self.make_sample()

    def build_board(self, cols: int, capacity: int):
        self.grid.clear_widgets()
        self.columns = []
        for _ in range(cols):
            c = ColumnWidget(capacity=capacity, size_hint=(None, None), width=90, height=260)
            c.bind(on_release=partial(self.on_col_tap, c))
            self.columns.append(c)
            self.grid.add_widget(c)

    def make_sample(self):
        # örnek karma bir tahta dolduralım (2 boş kolon bırak)
        data = [
            [1,2,1,2],
            [3,1,3,2],
            [2,3,1,3],
            [], []
        ]
        for col, arr in zip(self.columns, data + [[]]*(len(self.columns)-len(data))):
            col.clear_stack()
            for x in arr:
                col.push(x)

    def read_state(self) -> Tuple[List[List[ColorId]], int]:
        H = self.columns[0].capacity
        state = [c.stack[:] for c in self.columns]
        return state, H

    def set_state(self, state: List[List[ColorId]]):
        for col, arr in zip(self.columns, state):
            col.clear_stack()
            for x in arr:
                col.push(x)

    def on_col_tap(self, col: ColumnWidget, *_):
        if self.edit_toggle.state == "down":
            # edit modu: kısa dokunuş ekle, uzun dokunuş sil
            if len(col.stack) < col.capacity and (not col.stack or col.stack[-1] == self.active_color):
                col.push(self.active_color)
            else:
                col.pop()
        else:
            # oyun modu: kullanıcı hamle tıklatması (kaynak->hedef)
            if not hasattr(self, "_pending"):
                self._pending = col
                col.opacity = 0.7
            else:
                src = self._pending
                self._pending = None
                src.opacity = 1.0
                if src is col:
                    return
                # tek parça taşı
                if src.stack and (len(col.stack) < col.capacity) and (not col.stack or col.stack[-1] == src.stack[-1]):
                    col.push(src.pop())

    def on_play(self, *_):
        if not self.solution:
            return
        if self.sol_step >= len(self.solution):
            self.info.text = "Tüm adımlar oynatıldı ✔"
            self.play_btn.disabled = True
            return
        i, j, k = self.solution[self.sol_step]
        self.sol_step += 1

        # animasyon gibi sırayla k kez uygula
        def _one(_t=[0]):
            _t[0] += 1
            if _t[0] > k:
                return
            val = self.columns[i].pop()
            if val is not None:
                self.columns[j].push(val)
            if _t[0] < k:
                Clock.schedule_once(_one, 0.15)
        _one()
        self.info.text = f"Hamle {self.sol_step}/{len(self.solution)}: {i+1} → {j+1} (x{k})"

    def on_solve(self, *_):
        state, H = self.read_state()
        self.info.text = "Çözüm aranıyor…"
        self.solve_btn.disabled = True
        self.play_btn.disabled = True
        self.solution = None
        self.sol_step = 0

        def _run():
            ans = solve_iterative_deepening(state, H, max_depth=120)
            self._on_solved(ans)

        Thread(target=_run, daemon=True).start()

    @mainthread
    def _on_solved(self, ans: Optional[List[Move]]):
        self.solve_btn.disabled = False
        if not ans:
            self.info.text = "Çözüm bulunamadı (daha çok boş kolon eklemeyi deneyin)."
            return
        self.solution = ans
        self.sol_step = 0
        self.play_btn.disabled = False
        self.info.text = f"Çözüm bulundu: {len(ans)} hamle. ▶ Play ile adım adım uygula."

class CivataBotApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    CivataBotApp().run()
