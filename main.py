import random
from collections import deque
from copy import deepcopy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget

class BoltWidget(Widget):
    def __init__(self, color_id, **kwargs):
        super().__init__(**kwargs)
        self.color_id = color_id
        self.colors = [
            (0.8, 0.8, 0.8, 1),  # 0 - Empty (Light Gray)
            (1, 0, 0, 1),        # 1 - Red
            (0, 1, 0, 1),        # 2 - Green
            (0, 0, 1, 1),        # 3 - Blue
            (1, 1, 0, 1),        # 4 - Yellow
            (1, 0, 1, 1),        # 5 - Magenta
            (0, 1, 1, 1),        # 6 - Cyan
            (1, 0.5, 0, 1),      # 7 - Orange
            (0.5, 0, 1, 1),      # 8 - Purple
        ]
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.color_id == 0:  # Empty slot
                Color(0.9, 0.9, 0.9, 0.3)
                Rectangle(pos=self.pos, size=self.size)
            else:
                # Draw bolt
                color = self.colors[self.color_id]
                Color(*color)
                # Body of bolt
                bolt_width = min(self.width * 0.6, self.height * 0.8)
                bolt_height = min(self.width * 0.6, self.height * 0.8)
                x = self.x + (self.width - bolt_width) / 2
                y = self.y + (self.height - bolt_height) / 2
                Rectangle(pos=(x, y), size=(bolt_width, bolt_height))
                
                # Head of bolt (circle)
                Color(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8, 1)
                head_size = bolt_width * 0.4
                head_x = x + (bolt_width - head_size) / 2
                head_y = y + bolt_height - head_size / 2
                Ellipse(pos=(head_x, head_y), size=(head_size, head_size))

class ColumnWidget(BoxLayout):
    def __init__(self, column_data, max_height, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.column_data = column_data
        self.max_height = max_height
        self.update_display()
        
    def update_display(self):
        self.clear_widgets()
        # Add empty slots from top
        for i in range(self.max_height - len(self.column_data)):
            bolt = BoltWidget(color_id=0, size_hint=(1, 1))
            self.add_widget(bolt)
        
        # Add bolts from top to bottom
        for color_id in reversed(self.column_data):
            bolt = BoltWidget(color_id=color_id, size_hint=(1, 1))
            self.add_widget(bolt)

class GameState:
    def __init__(self, columns):
        self.columns = [col[:] for col in columns]  # Deep copy
        
    def __eq__(self, other):
        return self.columns == other.columns
        
    def __hash__(self):
        return hash(str(self.columns))
        
    def is_solved(self):
        for col in self.columns:
            if len(col) == 0:
                continue
            if len(set(col)) > 1:  # Different colors in same column
                return False
        return True
        
    def get_valid_moves(self):
        moves = []
        for from_col in range(len(self.columns)):
            if len(self.columns[from_col]) == 0:
                continue
                
            top_bolt = self.columns[from_col][-1]
            
            # Count consecutive bolts of same color from top
            count = 1
            for i in range(len(self.columns[from_col]) - 2, -1, -1):
                if self.columns[from_col][i] == top_bolt:
                    count += 1
                else:
                    break
                    
            for to_col in range(len(self.columns)):
                if from_col == to_col:
                    continue
                    
                # Check if we can move to this column
                if len(self.columns[to_col]) == 0:
                    # Empty column - can move any number of bolts
                    for move_count in range(1, count + 1):
                        moves.append((from_col, to_col, move_count))
                else:
                    # Non-empty column - check if top colors match
                    if self.columns[to_col][-1] == top_bolt:
                        # Can move bolts of same color
                        available_space = 4 - len(self.columns[to_col])  # Assuming max 4 bolts per column
                        max_movable = min(count, available_space)
                        if max_movable > 0:
                            for move_count in range(1, max_movable + 1):
                                moves.append((from_col, to_col, move_count))
        
        return moves
        
    def apply_move(self, from_col, to_col, count):
        new_state = GameState(self.columns)
        
        # Move bolts
        for _ in range(count):
            if len(new_state.columns[from_col]) > 0:
                bolt = new_state.columns[from_col].pop()
                new_state.columns[to_col].append(bolt)
                
        return new_state

class BoltSortingSolver:
    def __init__(self):
        self.solution_path = []
        
    def solve_bfs(self, initial_state):
        if initial_state.is_solved():
            return []
            
        queue = deque([(initial_state, [])])
        visited = {initial_state}
        max_iterations = 10000  # Prevent infinite loops
        iteration = 0
        
        while queue and iteration < max_iterations:
            iteration += 1
            current_state, moves = queue.popleft()
            
            for move in current_state.get_valid_moves():
                from_col, to_col, count = move
                new_state = current_state.apply_move(from_col, to_col, count)
                
                if new_state in visited:
                    continue
                    
                new_moves = moves + [move]
                
                if new_state.is_solved():
                    return new_moves
                    
                visited.add(new_state)
                queue.append((new_state, new_moves))
                
        return None  # No solution found

class CivataBotApp(App):
    def build(self):
        self.title = "CivataBot - Nut Sorting Puzzle"
        
        # Game state
        self.level = 1
        self.columns = []
        self.max_height = 4
        self.solver = BoltSortingSolver()
        self.solution = []
        self.play_index = 0
        self.is_playing = False
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.level_label = Label(text=f'Level: {self.level}', size_hint_x=0.3)
        self.status_label = Label(text='Tap New Game to start!', size_hint_x=0.7)
        header.add_widget(self.level_label)
        header.add_widget(self.status_label)
        main_layout.add_widget(header)
        
        # Game board
        self.game_board = GridLayout(cols=5, spacing=5, size_hint_y=0.7)
        main_layout.add_widget(self.game_board)
        
        # Control buttons
        controls = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.new_game_btn = Button(text='New Game')
        self.new_game_btn.bind(on_press=self.new_game)
        
        self.solve_btn = Button(text='Solve')
        self.solve_btn.bind(on_press=self.solve_puzzle)
        
        self.play_btn = Button(text='Play Solution', disabled=True)
        self.play_btn.bind(on_press=self.play_solution)
        
        self.next_level_btn = Button(text='Next Level')
        self.next_level_btn.bind(on_press=self.next_level)
        
        controls.add_widget(self.new_game_btn)
        controls.add_widget(self.solve_btn)
        controls.add_widget(self.play_btn)
        controls.add_widget(self.next_level_btn)
        
        main_layout.add_widget(controls)
        
        # Initialize first level
        self.generate_level()
        
        return main_layout
    
    def generate_level(self):
        # Calculate level parameters
        num_colors = min(2 + self.level // 2, 8)  # Start with 2 colors, max 8
        num_columns = min(4 + self.level // 3, 7)  # Start with 4 columns, max 7
        empty_columns = max(1, 3 - self.level // 4)  # Decrease empty columns as level increases
        
        # Generate puzzle
        self.columns = []
        
        # Create color distribution
        colors_per_column = []
        for color_id in range(1, num_colors + 1):
            colors_per_column.extend([color_id] * self.max_height)
        
        random.shuffle(colors_per_column)
        
        # Fill columns
        filled_columns = num_columns - empty_columns
        for i in range(filled_columns):
            column = []
            for j in range(self.max_height):
                if colors_per_column:
                    column.append(colors_per_column.pop())
            self.columns.append(column)
        
        # Add empty columns
        for i in range(empty_columns):
            self.columns.append([])
        
        # Ensure puzzle is solvable by shuffling moves
        self.shuffle_puzzle()
        
        self.update_display()
        self.status_label.text = f'Level {self.level} - {num_colors} colors, {num_columns} columns'
        self.solution = []
        self.play_btn.disabled = True
    
    def shuffle_puzzle(self):
        # Perform random valid moves to ensure solvability
        current_state = GameState(self.columns)
        
        for _ in range(20 + self.level * 5):  # More shuffles for higher levels
            moves = current_state.get_valid_moves()
            if moves:
                move = random.choice(moves)
                current_state = current_state.apply_move(*move)
        
        self.columns = current_state.columns
    
    def update_display(self):
        self.game_board.clear_widgets()
        self.game_board.cols = len(self.columns)
        
        for i, column_data in enumerate(self.columns):
            column_widget = ColumnWidget(column_data, self.max_height)
            self.game_board.add_widget(column_widget)
    
    def new_game(self, instance):
        self.generate_level()
        self.is_playing = False
        Clock.unschedule(self.play_next_move)
    
    def solve_puzzle(self, instance):
        self.status_label.text = 'Solving...'
        
        # Create initial state
        initial_state = GameState(self.columns)
        
        # Check if already solved
        if initial_state.is_solved():
            self.status_label.text = 'Already solved!'
            return
        
        # Solve using BFS
        self.solution = self.solver.solve_bfs(initial_state)
        
        if self.solution is None:
            self.show_popup("Unsolvable", "This puzzle has no solution!")
            self.status_label.text = 'No solution found!'
            self.play_btn.disabled = True
        else:
            self.status_label.text = f'Solution found! {len(self.solution)} moves'
            self.play_btn.disabled = False
    
    def play_solution(self, instance):
        if not self.solution:
            return
            
        self.is_playing = True
        self.play_index = 0
        self.play_btn.disabled = True
        Clock.schedule_interval(self.play_next_move, 1.0)  # 1 second between moves
    
    def play_next_move(self, dt):
        if self.play_index >= len(self.solution):
            Clock.unschedule(self.play_next_move)
            self.is_playing = False
            self.play_btn.disabled = False
            self.status_label.text = 'Solution completed!'
            
            # Check if solved
            current_state = GameState(self.columns)
            if current_state.is_solved():
                self.show_popup("Congratulations!", "Puzzle solved! Ready for next level?")
            return
        
        # Apply next move
        from_col, to_col, count = self.solution[self.play_index]
        
        # Move bolts one by one for visual effect
        for _ in range(count):
            if len(self.columns[from_col]) > 0:
                bolt = self.columns[from_col].pop()
                self.columns[to_col].append(bolt)
        
        self.update_display()
        self.status_label.text = f'Move {self.play_index + 1}/{len(self.solution)}: Column {from_col + 1} → Column {to_col + 1} ({count} bolts)'
        self.play_index += 1
    
    def next_level(self, instance):
        self.level += 1
        self.level_label.text = f'Level: {self.level}'
        self.generate_level()
        self.is_playing = False
        Clock.unschedule(self.play_next_move)
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        
        close_btn = Button(text='Close', size_hint_y=None, height=50)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    CivataBotApp().run()
