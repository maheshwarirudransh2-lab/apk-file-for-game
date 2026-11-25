import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class SlidingPuzzleApp(App):
    def build(self):
        self.title = "Sliding Tile Puzzle"
        self.grid = GridLayout(cols=4, rows=4, spacing=5, padding=5)
        self.buttons = {}  # map (r, c) -> Button
        self.empty_pos = (3, 3)
        self.values = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]
        self._shuffle_board()

        for r in range(4):
            for c in range(4):
                val = self.values[r][c]
                btn = Button(
                    text=str(val) if val != 0 else "",
                    font_size="32sp",
                    background_normal="",
                    background_color=(0.8, 0.8, 0.8, 1),
                )
                btn.pos_grid = (r, c)
                btn.bind(on_release=self.on_button_press)
                self.grid.add_widget(btn)
                self.buttons[(r, c)] = btn

        return self.grid

    def _shuffle_board(self, moves=100):
        """Make valid random moves so the puzzle is always solvable."""
        for _ in range(moves):
            er, ec = self.empty_pos
            neighbors = [
                (er + dr, ec + dc)
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= er + dr < 4 and 0 <= ec + dc < 4
            ]
            nr, nc = random.choice(neighbors)
            self.values[er][ec], self.values[nr][nc] = (
                self.values[nr][nc],
                self.values[er][ec],
            )
            self.empty_pos = (nr, nc)

    def on_button_press(self, button):
        r, c = button.pos_grid
        er, ec = self.empty_pos
        if (abs(r - er) == 1 and c == ec) or (abs(c - ec) == 1 and r == er):
            # Swap values
            self.values[er][ec] = self.values[r][c]
            self.values[r][c] = 0

            # Update both buttons' labels
            self.buttons[(er, ec)].text = str(self.values[er][ec])
            button.text = ""

            self.empty_pos = (r, c)
            self._check_solved()

    def _check_solved(self):
        flat = [val for row in self.values for val in row]
        if flat == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]:
            self._show_success()

    def _show_success(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        layout.add_widget(Label(text="You solved the puzzle!"))
        ok_btn = Button(text="OK", size_hint=(1, None), height=48)
        layout.add_widget(ok_btn)

        popup = Popup(
            title="Congratulations!",
            content=layout,
            size_hint=(0.8, 0.35),
        )
        ok_btn.bind(on_release=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    SlidingPuzzleApp().run()