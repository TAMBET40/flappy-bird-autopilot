import random
import tkinter as tk


WIDTH = 800
HEIGHT = 560
GROUND_HEIGHT = 58
BIRD_X = 190
PIPE_WIDTH = 76
PIPE_GAP = 174
PIPE_SPACING = 278


class FlappyAutopilot:
	def __init__(self, root):
		self.root = root
		self.root.title("Flappy Bird | Autopilot")
		self.root.resizable(False, False)
		self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#9be3df", highlightthickness=0)
		self.canvas.pack()
		self.best_score = 0
		self.reset()
		self.tick()

	def reset(self):
		self.bird_y = HEIGHT * 0.47
		self.velocity = 0.0
		self.score = 0
		self.frame = 0
		self.dead = False
		self.restart_in = 0
		self.pipes = []
		first_x = WIDTH + 50
		for index in range(3):
			self.pipes.append({
				"x": first_x + index * PIPE_SPACING,
				"gap": random.randint(150, 286),
				"scored": False,
			})

	def flap(self):
		self.velocity = -6.0

	def next_pipe(self):
		return min((pipe for pipe in self.pipes if pipe["x"] + PIPE_WIDTH >= BIRD_X), key=lambda pipe: pipe["x"])

	def pilot(self):
		pipe = self.next_pipe()
		flap_height = pipe["gap"] + 128
		if self.bird_y > flap_height and self.velocity > -1.5:
			self.flap()

	def update(self):
		self.frame += 1
		if self.dead:
			self.restart_in -= 1
			if self.restart_in <= 0:
				self.reset()
			return

		self.pilot()
		self.velocity = min(self.velocity + 0.19, 7.2)
		self.bird_y += self.velocity

		for pipe in self.pipes:
			pipe["x"] -= 3.25
			if not pipe["scored"] and pipe["x"] + PIPE_WIDTH <= BIRD_X - 15:
				pipe["scored"] = True
				self.score += 1
				self.best_score = max(self.best_score, self.score)

		if self.pipes[0]["x"] < -PIPE_WIDTH:
			self.pipes.pop(0)
			last_x = self.pipes[-1]["x"]
			self.pipes.append({
				"x": last_x + PIPE_SPACING,
				"gap": random.randint(150, 286),
				"scored": False,
			})

		self.check_collision()

	def check_collision(self):
		bird_left = BIRD_X - 15
		bird_right = BIRD_X + 15
		bird_top = self.bird_y - 12
		bird_bottom = self.bird_y + 12
		if bird_top < 38 or bird_bottom > HEIGHT - GROUND_HEIGHT:
			self.dead = True
		for pipe in self.pipes:
			if bird_right > pipe["x"] and bird_left < pipe["x"] + PIPE_WIDTH:
				if bird_top < pipe["gap"] or bird_bottom > pipe["gap"] + PIPE_GAP:
					self.dead = True
		if self.dead:
			self.restart_in = 48

	def draw_background(self):
		canvas = self.canvas
		canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#080808", outline="")
		canvas.create_rectangle(9, 9, WIDTH - 9, HEIGHT - 9, outline="#686868", width=2)
		canvas.create_rectangle(15, 15, WIDTH - 15, HEIGHT - 15, outline="#252525")
		canvas.create_rectangle(20, 64, WIDTH - 20, HEIGHT - GROUND_HEIGHT, fill="#111111", outline="")
		stars = [(45, 103), (93, 184), (148, 82), (219, 225), (278, 127), (333, 88),
			(397, 192), (454, 111), (523, 77), (576, 211), (641, 139), (747, 183),
			(704, 93), (369, 240), (171, 258), (604, 260), (70, 287), (744, 305)]
		for index, (star_x, star_y) in enumerate(stars):
			star_size = 4 if (index + self.frame // 18) % 5 == 0 else 2
			canvas.create_rectangle(star_x, star_y, star_x + star_size, star_y + star_size, fill="#d8d8d8", outline="")
			if star_size == 4:
				canvas.create_rectangle(star_x + 1, star_y - 3, star_x + 3, star_y + 7, fill="#777777", outline="")
				canvas.create_rectangle(star_x - 3, star_y + 1, star_x + 7, star_y + 3, fill="#777777", outline="")
		canvas.create_oval(633, 91, 693, 151, fill="#dddddd", outline="#ffffff", width=2)
		canvas.create_rectangle(666, 83, 701, 99, fill="#080808", outline="")
		canvas.create_rectangle(679, 97, 699, 119, fill="#080808", outline="")
		canvas.create_rectangle(641, 108, 648, 115, fill="#999999", outline="")
		canvas.create_rectangle(655, 133, 662, 140, fill="#999999", outline="")
		canvas.create_polygon(-20, 431, 81, 367, 153, 408, 247, 337, 349, 431, fill="#292929", outline="")
		canvas.create_polygon(250, 431, 359, 372, 444, 407, 551, 330, 674, 431, fill="#383838", outline="")
		canvas.create_polygon(531, 431, 637, 375, 714, 405, 804, 347, 830, 431, fill="#242424", outline="")
		canvas.create_rectangle(20, HEIGHT - GROUND_HEIGHT, WIDTH - 20, HEIGHT, fill="#1d1d1d", outline="")
		canvas.create_rectangle(20, HEIGHT - GROUND_HEIGHT, WIDTH - 20, HEIGHT - GROUND_HEIGHT + 7, fill="#eeeeee", outline="")
		canvas.create_rectangle(20, HEIGHT - GROUND_HEIGHT + 7, WIDTH - 20, HEIGHT - GROUND_HEIGHT + 10, fill="#777777", outline="")
		for x in range(-30, WIDTH + 36, 42):
			offset = (self.frame * 3) % 42
			canvas.create_rectangle(x - offset, HEIGHT - 17, x + 16 - offset, HEIGHT - 12, fill="#aaaaaa", outline="")
		for scan_y in range(69, HEIGHT - GROUND_HEIGHT, 6):
			canvas.create_line(21, scan_y, WIDTH - 21, scan_y, fill="#191919")

	def draw_pipe(self, pipe):
		canvas = self.canvas
		x = pipe["x"]
		gap_top = pipe["gap"]
		gap_bottom = gap_top + PIPE_GAP
		pipe_color = "#777777"
		edge_color = "#eeeeee"
		cap = 13
		canvas.create_rectangle(x + 7, 0, x + PIPE_WIDTH - 7, gap_top, fill=pipe_color, outline=edge_color, width=3)
		canvas.create_rectangle(x + 15, 4, x + 23, gap_top - cap, fill="#bdbdbd", outline="")
		canvas.create_rectangle(x + 31, 4, x + 34, gap_top - cap, fill="#999999", outline="")
		canvas.create_rectangle(x, gap_top - cap, x + PIPE_WIDTH, gap_top, fill="#bdbdbd", outline=edge_color, width=3)
		canvas.create_line(x + 5, gap_top - 3, x + PIPE_WIDTH - 5, gap_top - 3, fill="#ffffff", width=2)
		canvas.create_rectangle(x + 7, gap_bottom, x + PIPE_WIDTH - 7, HEIGHT - GROUND_HEIGHT, fill=pipe_color, outline=edge_color, width=3)
		canvas.create_rectangle(x + 15, gap_bottom + cap, x + 23, HEIGHT - GROUND_HEIGHT - 4, fill="#bdbdbd", outline="")
		canvas.create_rectangle(x + 31, gap_bottom + cap, x + 34, HEIGHT - GROUND_HEIGHT - 4, fill="#999999", outline="")
		canvas.create_rectangle(x, gap_bottom, x + PIPE_WIDTH, gap_bottom + cap, fill="#bdbdbd", outline=edge_color, width=3)
		canvas.create_line(x + 5, gap_bottom + 3, x + PIPE_WIDTH - 5, gap_bottom + 3, fill="#ffffff", width=2)

	def draw_bird(self):
		canvas = self.canvas
		wing_bob = (self.frame // 5) % 2 * 4
		canvas.create_rectangle(BIRD_X - 19, self.bird_y - 5, BIRD_X - 14, self.bird_y + 6, fill="#aaaaaa", outline="")
		canvas.create_rectangle(BIRD_X - 14, self.bird_y - 10, BIRD_X + 10, self.bird_y + 10, fill="#eeeeee", outline="#ffffff", width=2)
		canvas.create_rectangle(BIRD_X - 9, self.bird_y - 14 + wing_bob, BIRD_X + 5, self.bird_y + 2 + wing_bob, fill="#999999", outline="#eeeeee")
		canvas.create_rectangle(BIRD_X + 5, self.bird_y - 6, BIRD_X + 10, self.bird_y - 1, fill="#080808", outline="")
		canvas.create_rectangle(BIRD_X + 13, self.bird_y - 2, BIRD_X + 24, self.bird_y + 5, fill="#bdbdbd", outline="#ffffff")
		canvas.create_rectangle(BIRD_X - 10, self.bird_y + 11, BIRD_X - 3, self.bird_y + 14, fill="#bdbdbd", outline="")
		canvas.create_rectangle(BIRD_X + 3, self.bird_y + 11, BIRD_X + 10, self.bird_y + 14, fill="#bdbdbd", outline="")

	def draw(self):
		self.canvas.delete("all")
		self.draw_background()
		for pipe in self.pipes:
			self.draw_pipe(pipe)
		self.draw_bird()
		self.canvas.create_rectangle(22, 20, 240, 57, fill="#111111", outline="#777777")
		self.canvas.create_text(33, 27, anchor="nw", text="PLAYER 1", fill="#eeeeee", font=("TkFixedFont", 10, "bold"))
		self.canvas.create_oval(34, 44, 41, 51, fill="#ffffff", outline="")
		self.canvas.create_text(49, 39, anchor="nw", text="AUTO PILOT", fill="#aaaaaa", font=("TkFixedFont", 8, "bold"))
		self.canvas.create_rectangle(WIDTH / 2 - 51, 15, WIDTH / 2 + 51, 59, fill="#111111", outline="#aaaaaa", width=2)
		self.canvas.create_text(WIDTH / 2, 36, text=f"{self.score:03d}", fill="#ffffff", font=("TkFixedFont", 24, "bold"))
		self.canvas.create_rectangle(WIDTH - 223, 20, WIDTH - 22, 57, fill="#111111", outline="#777777")
		self.canvas.create_text(WIDTH - 33, 27, anchor="ne", text="FLAPPY 1984", fill="#eeeeee", font=("TkFixedFont", 10, "bold"))
		self.canvas.create_text(WIDTH - 33, 43, anchor="ne", text=f"HI  {self.best_score:03d}", fill="#aaaaaa", font=("TkFixedFont", 8, "bold"))
		self.canvas.create_line(22, 63, WIDTH - 22, 63, fill="#777777", width=2)
		if self.dead:
			self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#101010", stipple="gray50", outline="")
			self.canvas.create_rectangle(WIDTH / 2 - 170, HEIGHT / 2 - 50, WIDTH / 2 + 170, HEIGHT / 2 + 53, fill="#111111", outline="#eeeeee", width=3)
			self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 19, text="GAME OVER", fill="#ffffff", font=("TkFixedFont", 24, "bold"))
			self.canvas.create_line(WIDTH / 2 - 135, HEIGHT / 2 + 4, WIDTH / 2 + 135, HEIGHT / 2 + 4, fill="#777777")
			self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 27, text=f"SCORE {self.score:03d}  /  RESTARTING", fill="#bdbdbd", font=("TkFixedFont", 11, "bold"))

	def tick(self):
		self.update()
		self.draw()
		self.root.after(20, self.tick)


if __name__ == "__main__":
	window = tk.Tk()
	FlappyAutopilot(window)
	window.mainloop()
