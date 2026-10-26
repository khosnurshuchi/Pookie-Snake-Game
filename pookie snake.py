import tkinter as tk
import math
import random

# ---------- Colors (soft maroon + blush) ----------
bg = "#f8e8e6"
tile_a = "#fbeeec"
tile_b = "#f3dbd8"
maroon = "#7a1f33"
burgundy = "#8b2635"
rose = "#c9667a"
dusty_pink = "#e8a5b0"
cherry = "#d62850"

# Snake colors
body_a = "#8b2635"
body_b = "#76202f"
spot = "#b5485e"
head_col = "#6e1a2b"
head_edge = "#4a0f1c"
eye_col = "#e8c15a"
tongue_col = "#c2334f"

# ---------- Layout (design size 700 x 780, scaled to the window) ----------
DW, DH = 700, 780
BX, BY = 80, 110          # top-left of the board in design units
COLS = ROWS = 27
CELL = 20

root = tk.Tk()
root.title("🎀 Pookie Snake 🎀")
root.minsize(320, 360)
h0 = min(780, root.winfo_screenheight() - 120)
w0 = int(h0 * DW / DH)
root.geometry("{}x{}".format(w0, h0))

canvas = tk.Canvas(root, bg=bg, highlightthickness=0)
canvas.pack(fill="both", expand=True)

W, H = w0, h0
S, OX, OY = 1.0, 0.0, 0.0


def layout():
    global S, OX, OY, W, H
    W, H = max(canvas.winfo_width(), 50), max(canvas.winfo_height(), 50)
    S = min(W / DW, H / DH)
    OX = (W - DW * S) / 2
    OY = (H - DH * S) / 2


def X(x):
    return OX + x * S


def Y(y):
    return OY + y * S


def font(size):
    return ("Arial", max(7, int(size * S)), "bold")


# ---------- Game state ----------
START = (COLS // 2, ROWS // 2)
snake = [START]
direction = (0, 0)
facing = (0, -1)
queue = []
food = (COLS // 2, 5)
score = 0
high_score = 0
delay = 100
state = "ready"      # ready, playing, paused, over
message = "press an arrow key to start"
tickn = 0


def place_food():
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    return random.choice(free) if free else (-1, -1)


def reset_game():
    global snake, direction, queue, score, delay, food
    snake = [START]
    direction = (0, 0)
    queue = []
    score = 0
    delay = 100
    food = place_food()


def die():
    global state, message
    reset_game()
    state = "over"
    message = "oops! try again, bestie  -  press an arrow key"


def set_dir(d):
    global direction, state, message
    if state in ("ready", "over"):
        direction = d
        state = "playing"
        message = ""
        return
    if state != "playing":
        return
    last = queue[-1] if queue else direction
    if d == last or (len(snake) > 1 and d == (-last[0], -last[1])):
        return
    if len(queue) < 2:
        queue.append(d)


def toggle_pause():
    global state, message
    if state == "playing":
        state = "paused"
        message = "paused  -  press space to continue"
    elif state == "paused":
        state = "playing"
        message = ""


def step():
    global direction, facing, score, high_score, delay, food
    if queue:
        direction = queue.pop(0)
    facing = direction
    hx, hy = snake[0]
    new = (hx + direction[0], hy + direction[1])

    if not (0 <= new[0] < COLS and 0 <= new[1] < ROWS):
        die()
        return

    eating = new == food
    body = snake if eating else snake[:-1]
    if new in body:
        die()
        return

    snake.insert(0, new)
    if eating:
        score += 10
        high_score = max(high_score, score)
        delay = max(45, delay - 2)
        food = place_food()
    else:
        snake.pop()


# ---------- Drawing ----------
def draw_static():
    canvas.delete("static")
    canvas.create_rectangle(0, 0, W, H, fill=bg, outline="", tags="static")

    for r in range(ROWS):
        for c in range(COLS):
            canvas.create_rectangle(
                X(BX + c * CELL), Y(BY + r * CELL),
                X(BX + (c + 1) * CELL), Y(BY + (r + 1) * CELL),
                fill=tile_a if (r + c) % 2 == 0 else tile_b,
                outline="", tags="static")

    size = COLS * CELL
    for pad, color, width in ((4, maroon, 6), (11, rose, 2)):
        canvas.create_rectangle(
            X(BX - pad), Y(BY - pad), X(BX + size + pad), Y(BY + size + pad),
            outline=color, width=max(1, width * S), tags="static")

    canvas.create_text(X(DW / 2), Y(36), text="♥   P O O K I E   S N A K E   ♥",
                       fill=maroon, font=font(20), tags="static")
    canvas.create_text(X(DW / 2), Y(738), text="stay cute • eat hearts • be iconic",
                       fill=rose, font=font(12), tags="static")
    canvas.tag_lower("static")


def cell_center(g):
    return (X(BX + (g[0] + 0.5) * CELL), Y(BY + (g[1] + 0.5) * CELL))


def ellipse_pts(cx, cy, a, b, fwd, n=28):
    perp = (-fwd[1], fwd[0])
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        px, py = a * math.cos(t), b * math.sin(t)
        pts += [cx + px * fwd[0] + py * perp[0], cy + px * fwd[1] + py * perp[1]]
    return pts


def draw_snake(c):
    n = len(snake)
    pts = [cell_center(g) for g in snake]

    # body, tail first so the head ends up on top
    for i in range(n - 1, 0, -1):
        r = c * 0.46 * (1 - 0.5 * i / n)
        a, b = pts[i], pts[i - 1]
        canvas.create_line(a[0], a[1], b[0], b[1], width=2 * r,
                           fill=body_a if i % 2 else body_b,
                           capstyle="round", tags="dyn")
        if i % 2 == 0:
            rs = r * 0.5
            canvas.create_oval(a[0] - rs, a[1] - rs, a[0] + rs, a[1] + rs,
                               fill=spot, outline="", tags="dyn")

    # head
    hx, hy = pts[0]
    fwd = facing
    perp = (-fwd[1], fwd[0])
    canvas.create_polygon(
        ellipse_pts(hx + fwd[0] * c * 0.08, hy + fwd[1] * c * 0.08, c * 0.62, c * 0.5, fwd),
        fill=head_col, outline=head_edge, width=max(1, S), tags="dyn")

    # eyes with slit pupils
    for side in (-1, 1):
        ex = hx + fwd[0] * c * 0.2 + perp[0] * side * c * 0.28
        ey = hy + fwd[1] * c * 0.2 + perp[1] * side * c * 0.28
        er = c * 0.13
        canvas.create_oval(ex - er, ey - er, ex + er, ey + er,
                           fill=eye_col, outline=head_edge, tags="dyn")
        canvas.create_line(ex - fwd[0] * er * 0.8, ey - fwd[1] * er * 0.8,
                           ex + fwd[0] * er * 0.8, ey + fwd[1] * er * 0.8,
                           width=max(1, c * 0.06), fill="black", tags="dyn")
        # nostril
        nx = hx + fwd[0] * c * 0.5 + perp[0] * side * c * 0.1
        ny = hy + fwd[1] * c * 0.5 + perp[1] * side * c * 0.1
        canvas.create_oval(nx - 1, ny - 1, nx + 1, ny + 1, fill="black", outline="", tags="dyn")

    # flicking tongue
    if tickn % 8 < 3:
        w = max(1, c * 0.07)
        sx, sy = hx + fwd[0] * c * 0.68, hy + fwd[1] * c * 0.68
        tx, ty = hx + fwd[0] * c * 1.1, hy + fwd[1] * c * 1.1
        canvas.create_line(sx, sy, tx, ty, width=w, fill=tongue_col, tags="dyn")
        for side in (-1, 1):
            canvas.create_line(tx, ty,
                               tx + fwd[0] * c * 0.22 + perp[0] * side * c * 0.14,
                               ty + fwd[1] * c * 0.22 + perp[1] * side * c * 0.14,
                               width=w, fill=tongue_col, tags="dyn")


def draw_heart(c):
    if food[0] < 0:
        return
    fx, fy = cell_center(food)
    k = c * 1.3 / 32 * (1 + 0.06 * math.sin(tickn * 0.5))
    pts = []
    for i in range(0, 360, 8):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts += [fx + x * k, fy - (y + 2.5) * k]
    canvas.create_polygon(pts, fill=cherry, outline="#8f1030", width=max(1, S), tags="dyn")
    hx, hy = fx - 8 * k, fy - 10 * k
    canvas.create_oval(hx - 2.2 * k, hy - 1.6 * k, hx + 2.2 * k, hy + 1.6 * k,
                       fill="#f7b4c2", outline="", tags="dyn")

    # tiny sparkles
    for j in range(3):
        ang = tickn * 0.25 + j * 2.1
        sx = fx + math.cos(ang) * c * 0.95
        sy = fy + math.sin(ang) * c * 0.95
        sz = c * 0.12
        canvas.create_line(sx - sz, sy, sx + sz, sy, fill=rose, width=max(1, S), tags="dyn")
        canvas.create_line(sx, sy - sz, sx, sy + sz, fill=rose, width=max(1, S), tags="dyn")


def draw_dynamic():
    canvas.delete("dyn")
    c = CELL * S
    draw_heart(c)
    draw_snake(c)
    canvas.create_text(X(DW / 2), Y(82),
                       text="Score: {}     ♥     Bestie Score: {}".format(score, high_score),
                       fill=burgundy, font=font(15), tags="dyn")
    if message:
        canvas.create_text(X(DW / 2), Y(692), text=message,
                           fill=rose, font=font(15), tags="dyn")


# ---------- Events ----------
pending = None


def redraw_all():
    global pending
    pending = None
    layout()
    draw_static()
    draw_dynamic()


def on_resize(event):
    global pending
    if pending:
        root.after_cancel(pending)
    pending = root.after(20, redraw_all)


def on_key(event):
    keys = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0),
            "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
    if event.keysym in keys:
        set_dir(keys[event.keysym])
    elif event.keysym == "space":
        toggle_pause()


def tick():
    global tickn
    tickn += 1
    if state == "playing":
        step()
    draw_dynamic()
    root.after(delay, tick)


canvas.bind("<Configure>", on_resize)
root.bind("<Key>", on_key)
root.update_idletasks()
reset_game()
redraw_all()
tick()
root.mainloop()
