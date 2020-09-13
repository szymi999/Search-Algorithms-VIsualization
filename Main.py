import tkinter as tk
import PlayVisualization as pv
import Fields

class Gui(tk.Tk):

	def __init__(self, title="title", width=600, height=400):
		super().__init__()

		#---------- configuring some of window options --------------
		self.title(title)
		self.windowWidth = width
		self.windowHeight = height
		self.windowPositionX = self.winfo_screenwidth() / 2 - self.windowWidth / 2
		self.windowPositionY = self.winfo_screenheight() / 2 - self.windowHeight / 2
		self.geometry("{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, int(self.windowPositionX), int(self.windowPositionY)))

		# ------------ declaring variables and lists -------------
		self.s = tk.IntVar() 	# value of radiobuttons
		self.fields = []	# list of Fields classes, that class have information about every node
		self.fieldHeight = 10	# height of node
		self.fieldWidth = 10	# width of node
		self.ready = False	# true if vusialization is ready to start, if everything is set
		self.walls = [] # list which contains every wall node
		self.vis = pv.PlayVisualization(self.windowWidth, self.windowHeight, self.fieldWidth, self.fieldHeight) # initialize PlayVisualization class

		self.create_widgets_menu()	# creating widgets

	def create_widgets_menu(self):	
		#--------------------- creating widgets for menu and configuring them -------------------
		frame = tk.Frame(self, width=self.windowWidth, height=self.windowHeight)
		frame.place(relx=0, rely=0, relwidth=1, relheight=1)

		text = tk.Label(frame, text="Wybierz algorytm przeszukiwania:")
		text.place(relx=0.37, rely=0.05, relwidth=0.26, relheight=0.1)

		bfsRB = tk.Radiobutton(frame, text="Szukanie w szerz", variable=self.s, value=0)
		bfsRB.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.1)

		dfsRB = tk.Radiobutton(frame, text="Szukanie w głąb", variable=self.s, value=1)
		dfsRB.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.1)

		aStarRB = tk.Radiobutton(frame, text="Algorytm A*", variable=self.s, value=2)
		aStarRB.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)

		dijkstraRB = tk.Radiobutton(frame, text="Algorytm Dijkstry", variable=self.s, value=3)
		dijkstraRB.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.1)

		startBT = tk.Button(frame, text="Rozpocznij", command=lambda: self.start(frame))
		startBT.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

	def start(self, frame):
		#------------- action after clicking start button ----------------
		self.walls = [] # reset this list
		frame.destroy()	# destroy frame
		self.vis.set_algorithm(self.check_radiobuttons()) # initialize variables
		self.create_widgets_visualization()
		self.ready = True

	def create_widgets_visualization(self):
		#------------- creating view for visualization of algorithm ----------------

		#------------- save where user created walls with mouse --------------------
		def mouse_clicked(event):
			if not self.vis.simulation:
				x = int(event.x/self.fieldWidth) * self.fieldWidth
				y = int(event.y/self.fieldHeight) * self.fieldHeight
				self.fields[int(y/self.fieldHeight)][int(x/self.fieldWidth)].wall = True
				self.walls.append([int(y/self.fieldHeight), int(x/self.fieldWidth)])
				canvas.create_rectangle(x, y, x + self.fieldWidth, y + self.fieldHeight, outline="black", fill="black")
				canvas.update()

		#------------- first prepare canvas and its inside -------------------------
		canvas = tk.Canvas(self, width=self.windowWidth, height=0.75 * self.windowHeight)
		canvas.bind("<B1-Motion>", mouse_clicked)
		canvas.place(relx=0, rely=0, relwidth=1, relheight=0.75)
		self.make_canvas(canvas)

		#------------- preparing frame where the buttons will be -------------------
		frame = tk.Frame(self, width=self.windowWidth, height=0.25 * self.windowHeight)
		frame.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)

		backBT = tk.Button(frame, text="Powrót do menu", command=lambda: self.return_to_menu(canvas, frame))
		backBT.place(relx=0.1, rely=0.25, relwidth=0.2, relheight=0.5)

		visualizationBT = tk.Button(frame, text="Rozpocznij", command=lambda: self.start_visualization(canvas))
		visualizationBT.place(relx=0.7, rely=0.25, relwidth=0.2, relheight=0.5)

	def start_visualization(self, canvas):
		# ---------------- starting visualization -----------------
		if self.ready:
			self.make_canvas(canvas)
		self.vis.set_fields(self.fields)
		self.vis.simulation = True
		self.vis.play(canvas)

	def return_to_menu(self, canvas, frame):
		#------------------ clearing actual frame and canvas --------------
		self.ready = False
		self.vis.simulation = False
		canvas.delete("all")
		frame.destroy()
		self.create_widgets_menu()

	def check_radiobuttons(self):
		#------------- check which radiobutton is active -----------------
		return self.s.get()

	def make_canvas(self, canvas):
		# -------------- making actual look of map -----------------------
		tmp = []
		self.fields = []
		for y in range(int(0.75 * self.windowHeight / self.fieldHeight)):
			for x in range(int(self.windowWidth / self.fieldWidth)):
				if x == 5 and y == 5:
					start = True
				else:
					start = False

				if x == 20 and y == 1:
					finish = True
				else:
					finish = False

				tmp.append(Fields.Field(x * self.fieldWidth, y * self.fieldHeight, x * self.fieldWidth + self.fieldWidth, y * self.fieldHeight + self.fieldHeight, start, finish, 0))
			self.fields.append(tmp)
			tmp = []

		for w in self.walls:
			self.fields[w[0]][w[1]].wall = True

		self.draw_fields(canvas)
			
	def draw_fields(self, canvas):
		#----------------------- draw map ----------------------
		for field in self.fields:
			for f in field:
				if f.x == 0 or f.x == int(int(self.windowWidth / self.fieldWidth) * self.fieldWidth - self.fieldWidth) or f.y == 0 or f.y == int(int(0.75 * self.windowHeight / self.fieldHeight) * self.fieldHeight - self.fieldHeight):
					color = "black"
				elif f.start or f.finish:
					color = "red"
				elif f.wall:
					color = "black"
				else:
					color = "white"
				canvas.create_rectangle(f.x, f.y, f.width, f.height, outline="black", fill=color)
			

gui = Gui("Wizualizacja szukania", 1000, 600)
gui.mainloop()	