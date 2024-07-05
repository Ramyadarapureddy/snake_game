from tkinter import *
import random
from tkcolorpicker import askcolor

# Constants
GAME_WIDTH = 800
GAME_HEIGHT = 700
BACKGROUND_COLOR = "black"
SPACE_SIZE = 50
BODY_PARTS = 3
DEFAULT_SNAKE_COLOR = "#36DE05"
FOOD_COLOR = "RED"
SPEEDS = {"low": 150, "medium": 100, "high": 50}

class Snake:
    def __init__(self, color=DEFAULT_SNAKE_COLOR):
        self.body = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = color  # Initialize with default color

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)

    def change_color(self, color):
        self.color = color
        for square in self.squares:
            canvas.itemconfig(square, fill=self.color)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    window.after(2000, show_menu)

def start_game():
    global snake, food, score, direction, SPEED
    score = 0
    direction = 'down'
    SPEED = SPEEDS[level_var.get()]
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    snake = Snake(snake_color_var.get())  # Initialize Snake with selected color
    food = Food()
    next_turn(snake, food)
    hide_menu()
    label.pack()

def hide_menu():
    heading.place_forget()
    new_game.place_forget()
    level.place_forget()
    setting.place_forget()
    level_label.place_forget()
    level_toggle.place_forget()

def show_menu():
    canvas.delete(ALL)
    heading.place(x=150, y=100)
    new_game.place(x=320, y=230)
    level.place(x=320, y=340)
    setting.place(x=320, y=450)
    label.pack_forget()

def show_level_selection():
    global level_var
    
    # Create a new Toplevel window for level selection
    level_window = Toplevel(window)
    level_window.title("Select Level")
    level_window.geometry("350x100")
    level_window.config(bg="black")
    
    # Center the level selection window relative to the main window
    level_window.update_idletasks()
    level_width = level_window.winfo_width()
    level_height = level_window.winfo_height()
    x = window.winfo_rootx() + (window.winfo_width() - level_width) // 2
    y = window.winfo_rooty() + (window.winfo_height() - level_height) // 2
    level_window.geometry(f"+{x}+{y}")
    
    # Create Radiobuttons for level selection
    low_level_radio = Radiobutton(level_window, text="Low", font=("Times New Roman", 15, "italic"), fg="white", bg="green", variable=level_var, value="low")
    medium_level_radio = Radiobutton(level_window, text="Medium", font=("Times New Roman", 15, "italic"), fg="white", bg="green", variable=level_var, value="medium")
    high_level_radio = Radiobutton(level_window, text="High", font=("Times New Roman", 15, "italic"), fg="white", bg="green", variable=level_var, value="high")
    
    low_level_radio.grid(row=0, column=0, padx=20, pady=10)
    medium_level_radio.grid(row=0, column=1, padx=20, pady=10)
    high_level_radio.grid(row=0, column=2, padx=20, pady=10)



def open_settings():
    settings_window = Toplevel(window)
    settings_window.title("Snake Game Settings")
    settings_window.geometry("400x400")
    settings_window.resizable(False, False)
    settings_window.config(bg=BACKGROUND_COLOR)

    # Snake color selection
    snake_color_label = Label(settings_window, text="Snake Color:", font=("Times New Roman", 15, "italic"), fg="white", bg="black")
    snake_color_label.pack(pady=30)

    def pick_color():
        color = askcolor(color=DEFAULT_SNAKE_COLOR, parent=settings_window)
        if color[1]:  # Check if a color was chosen
            snake_color_var.set(color[1])

    pick_color_button = Button(settings_window, text="Pick Color", font=("Times New Roman", 12), fg="white", bg="green", activeforeground="White", activebackground="#5EDE05", width=15, command=pick_color)
    pick_color_button.pack(pady=5)

    # Theme selection
    theme_label = Label(settings_window, text="Select Theme:", font=("Times New Roman", 15, "italic"), fg="white", bg="black")
    theme_label.pack(pady=30)

    theme_var = StringVar(value="dark")

    def change_theme_option():
        theme = theme_var.get()
        change_theme(theme)

    dark_theme_radio = Radiobutton(settings_window, text="Dark", font=("Times New Roman", 12), fg="white", bg="green", variable=theme_var, value="dark", command=change_theme_option)
    dark_theme_radio.place(x=120,y=200)

    light_theme_radio = Radiobutton(settings_window, text="Light", font=("Times New Roman", 12), fg="white", bg="green", variable=theme_var, value="light", command=change_theme_option)
    light_theme_radio.place(x=200,y=200)

def change_theme(theme):
    global BACKGROUND_COLOR, DEFAULT_SNAKE_COLOR
    if theme == "dark":
        BACKGROUND_COLOR = "black"
        DEFAULT_SNAKE_COLOR = "#36DE05"
        canvas.config(bg=BACKGROUND_COLOR)
    elif theme == "light":
        BACKGROUND_COLOR = "white"
        DEFAULT_SNAKE_COLOR = "green"
        canvas.config(bg=BACKGROUND_COLOR)

# Main Window
window = Tk()
window.geometry("800x750")
window.title("Snake Game 🐍")
window.resizable(False, False)

# Score label
score = 0
direction = 'down'
SPEED = SPEEDS["medium"]  # Default speed is medium
label = Label(window, text="Score: {}".format(score), font=('Arial', 30))

# Canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center Window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind Keys
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Menu Elements
heading = Label(window, text="Welcome to Snake Game 🐍", font=("Times New Roman", 40, "italic"), fg="Green",bg="gray")
heading.place(x=150, y=100)

new_game = Button(window, text="New Game", font=("Times New Roman", 30, "italic"), fg="white", bg="Green", activeforeground="White", activebackground="#5EDE05", width=10, relief=RAISED, bd=10, command=start_game)
new_game.place(x=320, y=230)

level = Button(window, text="Level", font=("Times new Roman", 30, "italic"), fg="white", bg="green", activeforeground="White", activebackground="#5EDE05", width=10, relief=RAISED, bd=10, command=show_level_selection)
level.place(x=320, y=340)

setting = Button(window, text="Setting", font=("Times new Roman", 30, "italic"), fg="white", bg="green", activeforeground="White", activebackground="#5EDE05", width=10, relief=RAISED, bd=10, command=open_settings)
setting.place(x=320, y=450)

# Level Selection
level_var = StringVar(value="medium")
level_label = Label(window, text="Select Level:", font=("Times New Roman", 20, "italic"), fg="white", bg="black")
level_toggle = OptionMenu(window, level_var, "low", "medium", "high")
level_toggle.config(font=("Times New Roman", 20, "italic"), fg="white", bg="green", activeforeground="white", activebackground="#5EDE05")

# Snake Color Selection Variable
snake_color_var = StringVar(value=DEFAULT_SNAKE_COLOR)

icon = PhotoImage(file="icon.png")
window.iconphoto(window,icon)

window.config(background="black")
window.mainloop()
