from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import random

class CivataBot(App):
    def build(self):
        self.label = Label(text="Civata Bot başlıyor...")
        Clock.schedule_once(self.start_bot, 2)
        return self.label

    def start_bot(self, dt):
        # Burada ekran yakalama ve renk tespiti olmalı
        # Örnek zekâ: Rastgele 2 sütun seçip hamle yapıyor
        moves = [(1, 2), (0, 3), (2, 1)]
        if moves:
            m = random.choice(moves)
            self.label.text = f"Hamle yapıldı: {m[0]} → {m[1]}"
        else:
            self.label.text = "Hamle bulunamadı!"

if __name__ == "__main__":
    CivataBot().run()