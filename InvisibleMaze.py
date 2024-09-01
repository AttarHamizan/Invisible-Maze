from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect, QTime, QTimer
import random

class MazeGame(QWidget):
    def __init__(self,):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Invisible Maze')
        self.setGeometry(500, 500, 1000, 500)

        self.mazeWidget = MazeWidget()

        # Timer
        time = QTime(0, 0, 30)
        txt_timer = time.toString("hh:mm:ss")

        self.txt_countdown = QLabel(txt_timer)
        self.txt_countdown.setFont(QFont("Times", 36, QFont.Bold))

        # Layout 1
        self.up_button = QPushButton('^')
        self.up_button.clicked.connect(lambda: self.mazeWidget.keyEvent("UP"))
        self.down_button = QPushButton('V')
        self.down_button.clicked.connect(lambda: self.mazeWidget.keyEvent("DOWN"))
        self.right_button = QPushButton('>')
        self.right_button.clicked.connect(lambda: self.mazeWidget.keyEvent("RIGHT"))
        self.left_button = QPushButton('<')
        self.left_button.clicked.connect(lambda: self.mazeWidget.keyEvent("LEFT"))

        self.regenerate_button = QPushButton("Regenerate Maze")
        self.regenerate_button.clicked.connect(self.mazeWidget.restartMaze)
        self.regenerate_button.clicked.connect(self.timerCountdown)

        # Layout 2
        layout_timer = QHBoxLayout()
        layout_up = QHBoxLayout()
        layout_leftright = QHBoxLayout()
        layout_down = QHBoxLayout()
        layout_regenerate = QHBoxLayout()
        layout_timer.addWidget(self.txt_countdown, alignment=Qt.AlignCenter)
        layout_up.addWidget(self.up_button, alignment=Qt.AlignCenter)
        layout_leftright.addWidget(self.left_button, alignment=Qt.AlignLeft)
        layout_leftright.addWidget(self.right_button, alignment=Qt.AlignRight)
        layout_down.addWidget(self.down_button, alignment=Qt.AlignCenter)
        layout_regenerate.addWidget(self.regenerate_button, alignment=Qt.AlignCenter)

        layout_input = QVBoxLayout()
        layout_input.addLayout(layout_timer)
        layout_input.addLayout(layout_up)
        layout_input.addLayout(layout_leftright)
        layout_input.addLayout(layout_down)
        layout_input.addLayout(layout_regenerate)

        # Layout Main
        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_input)
        layout_main.addWidget(self.mazeWidget)

        self.setLayout(layout_main)

    def timerCountdown(self):
        global time
        time = QTime(0, 0, 30)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerCountdownEvent)
        self.timer.start(1000)

    def timerCountdownEvent(self):
        global time
        time = time.addSecs(-1)
        self.txt_countdown.setText(time.toString("hh:mm:ss"))
        self.txt_countdown.setFont(QFont("Times", 36, QFont.Bold))
        self.txt_countdown.setStyleSheet("color: rgb(0,0,0)")
        if time.toString("hh:mm:ss") == "00:00:00":
            self.timer.stop()
            self.mazeWidget.timer_finished = True
            self.mazeWidget.player_x = 0
            self.mazeWidget.player_y = 0
            self.mazeWidget.update()

class MazeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Maze
        self.rows = 15
        self.columns = 15
        self.cell_size = 30

        self.player_x = 0
        self.player_y = 0

        self.maze = [[1 for _ in range(self.columns)] for _ in range(self.rows)]

        self.end_x = self.columns - 1
        self.end_y = self.rows - 1

        self.timer_finished = False

    def generateMaze(self, x, y):
        self.maze[y][x] = 0

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)

        for direction in directions:
            new_x = x + direction[0] * 2
            new_y = y + direction[1] * 2

            if 0 <= new_x < self.columns and 0 <= new_y < self.rows and self.maze[new_y][new_x] == 1:
                self.maze[y + direction[1]][x + direction[0]] = 0
                self.generateMaze(new_x, new_y)

    def restartMaze(self):
        self.player_x = 0
        self.player_y = 0

        self.maze = [[1 for _ in range(self.columns)] for _ in range(self.rows)]
        self.generateMaze(0, 0)
        self.timer_finished = False
 
        self.update()

    def paintEvent(self, timer):
        painter = QPainter(self)
        if not painter.isActive():
            return
        
        if self.timer_finished:
            self.InvisibleMaze(painter)
        else:
            self.drawMaze(painter)
            self.drawPlayer(painter)
            self.drawFinish(painter)

    def drawMaze(self, painter):
        for y in range(self.rows):
            for x in range(self.columns):
                rect = QRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.maze[y][x] == 1:
                    painter.fillRect(rect, QColor('black'))
                else:
                    painter.drawRect(rect)
        
    def drawPlayer(self, painter):
        player_rect = QRect(self.player_x * self.cell_size, self.player_y * self.cell_size, self.cell_size, self.cell_size)
        painter.fillRect(player_rect, QColor('blue'))
        
    def drawFinish(self, painter):
        finish_rect = QRect(self.end_x * self.cell_size, self.end_y * self.cell_size, self.cell_size, self.cell_size)
        painter.fillRect(finish_rect, QColor('lime'))

    def InvisibleMaze(self, painter):
        for y in range(self.rows):
            for x in range(self.columns):
                rect = QRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                painter.drawRect(rect)
        
        player_rect = QRect(self.player_x * self.cell_size, self.player_y * self.cell_size, self.cell_size, self.cell_size)
        painter.fillRect(player_rect, QColor('blue'))

        finish_rect = QRect(self.end_x * self.cell_size, self.end_y * self.cell_size, self.cell_size, self.cell_size)
        painter.fillRect(finish_rect, QColor('lime'))

    def keyEvent(self, key):
        if key == "UP" and self.player_y > 0 and self.maze[self.player_y - 1][self.player_x] == 0:
            self.player_y -= 1
        elif key == "DOWN" and self.player_y < self.rows - 1 and self.maze[self.player_y + 1][self.player_x] == 0:
            self.player_y += 1
        elif key == "LEFT" and self.player_x > 0 and self.maze[self.player_y][self.player_x - 1] == 0:
            self.player_x -= 1
        elif key == "RIGHT" and self.player_x < self.columns - 1 and self.maze[self.player_y][self.player_x + 1] == 0:
            self.player_x += 1

        if self.player_x == self.end_x and self.player_y == self.end_y:
            print("You Win!")
            QMessageBox.information(self, 'Berhasil', "Anda Menang!")
            self.player_x = 0
            self.player_y = 0
        self.update()

app = QApplication([])
game = MazeGame()
game.show()
app.exec_()
