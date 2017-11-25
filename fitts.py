from tkinter import Tk, Canvas, Frame, Button
from tkinter import BOTH, W, E, NW, SUNKEN, TOP, X, FLAT, LEFT, CENTER
from math import *
import time
from random import *

class Fitts(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.width = 800
        self.height = 800
        self.mid_x = self.width/2
        self.mid_y = self.height/2
        self.radii = [110, 200, 300]
        self.target_sizes = [10, 20]
        self.pairs = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
        self.pairs_visited_order = []
        self.times = []
        self.raw_data = []
        self.disabled_count = 0
        self.parent = parent
        self.canvas1 = Canvas(self, relief=FLAT, background="#FFFFFF",
                        width=self.width, height=self.height)
        self.initCanvas()

    def initCanvas(self):
        self.parent.title("HMW3: Fitt's Law")
        self.config(bg='#D3D3D3')
        self.pack(fill=BOTH, expand=1)

        # Create canvas
        self.canvas1.pack(side=TOP, anchor=CENTER, padx=10, pady=10)

        # Add quit button
        button1 = Button(self, text="Quit", command=self.quit)
        button1.configure(width=10, activebackground="#FF0000", relief=FLAT)
        button1_window = self.canvas1.create_window(500, 50, window=button1)

        # Add Start Button
        button2 = Button(self, text="Start", command=self.fitts_cycle_start)
        button2.configure(width=10, activebackground="#33B5E5", relief=FLAT)
        button2_window = self.canvas1.create_window(300, 50, window=button2)

    # Get Y Coordinate, uses Pythagorean Theorem
    def getY(self, x, hyp):
        print("x: " + str(x))
        print("hyp: " + str(hyp))
        y = sqrt(abs(pow(hyp, 2)-pow(x, 2)))
        print("calculated y: " + str(y))
        return y

    # Enable next object after circle is clicked
    def onCircleClick(self, event):
        time_clicked = time.time()
        print("time: " + str(time_clicked))
        self.raw_data.append(time_clicked)

        print("got object click: ", event.x, event.y)
        id = event.widget.find_closest(event.x, event.y)
        print("closest object: " + str(id))

        # disable closest object
        self.canvas1.itemconfig(id[0], state="disabled", fill="#FFFFFF")
        self.disabled_count += 1
        print("disabled count: " + str(self.disabled_count))

        if (self.disabled_count % 2) == 0:
            time_diff = (self.raw_data[-1])-(self.raw_data[-2])
            self.times.append(time_diff)
            print("time diff: " + str(time_diff))

        # enable the next object (second in a pair, or first in a pair)
        self.canvas1.itemconfig(id[0]+1, state="normal", fill="#FF0000")

    # Erases all objects after last circle in Fitt's Law series is clicked
    def lastCircleClick(self, event):
        time_clicked = time.time()
        print("time clicked: " + str(time_clicked))
        self.raw_data.append(time_clicked)

        print("LAST CIRCLE")
        print("got object click: ", event.x, event.y)
        id = event.widget.find_closest(event.x, event.y)
        print("closest object: " + str(id))

        self.canvas1.itemconfig(id[0], state="disabled", fill="#FFFFFF")
        self.disabled_count += 1
        print("disabled count: " + str(self.disabled_count))

        time_diff = (self.raw_data[-1])-(self.raw_data[-2])
        self.times.append(time_diff)
        print("time diff: " + str(time_diff))

        # delete all current canvas objects from canvas
        for i in range(id[0], id[0]-self.disabled_count, -1):
            self.canvas1.delete(i)
        # reset deleted count
        self.disabled_count = 0
        print("data: " + str(self.raw_data))
        print("data: " + str(self.times))
        self.fitts_cycle_start()

    def choose_width_distance(self):
        while 1:
            rand_i = randrange(0,3)
            rand_j = randrange(0,2)

            if (rand_i, rand_j) in self.pairs:
                return (rand_i, rand_j)
            else:
                print("redo, rand i: " + str(rand_i) + " rand j: " + str(rand_j))
                print("self.pairs: " + str(self.pairs))
                print("self.pairs_visited: " + str(self.pairs))
                continue

    def fitts_cycle_start(self):
        if (len(self.pairs) != 0):
            (rand_i, rand_j) = self.choose_width_distance()
            self.pairs.remove((rand_i, rand_j))
            self.pairs_visited_order.append((rand_i, rand_j))
            self.raw_data.append((self.radii[rand_i], self.target_sizes[rand_j]))
            self.fitts_cycle(rand_i, rand_j)
            return
        else:
            print("experiment end")
            print("data returned: " + str(self.raw_data))
            print("data returned: " + str(self.times))


    def fitts_cycle(self, i, j):
        print("click!")
        x_axis_adjustments = [.4, .7, .93]

        # top circle
        circle3 = self._create_circle(self.mid_x, self.mid_y-self.radii[i], self.target_sizes[j], "#000000")
        self.canvas1.tag_bind(circle3, "<ButtonPress-1>", self.onCircleClick)

        # bottom circle
        circle4 = self._create_circle(self.mid_x, self.mid_y+self.radii[i], self.target_sizes[j], "#000000")
        self.canvas1.tag_bind(circle4, "<ButtonPress-1>", self.onCircleClick)

        for k in range(0, len(x_axis_adjustments)):
            # Quadrant I
            # Choose X
            pytha_x = (self.radii[i] * (x_axis_adjustments[k]))
            x_pos = self.mid_x + pytha_x
            # Derive Y
            pytha_y = self.getY(pytha_x, self.radii[i])
            y_pos = self.mid_y - pytha_y

            # Quadrant III
            q3_x_pos = self.mid_x - pytha_x
            q3_y_pos = self.mid_y + pytha_y

            circle5 = self._create_circle(x_pos, y_pos, self.target_sizes[j], "#0000FF")
            self.canvas1.tag_bind(circle5, "<ButtonPress-1>", self.onCircleClick)

            circle6 = self._create_circle(q3_x_pos, q3_y_pos, self.target_sizes[j], "#0000FF")
            self.canvas1.tag_bind(circle6, "<ButtonPress-1>", self.onCircleClick)

        # right circle
        circle2 = self._create_circle(self.mid_x+self.radii[i], self.mid_y, self.target_sizes[j], "#000000")
        self.canvas1.tag_bind(circle2, "<ButtonPress-1>", self.onCircleClick)

        # left circle
        circle1 = self._create_circle(self.mid_x-self.radii[i], self.mid_y, self.target_sizes[j], "#000000")
        self.canvas1.tag_bind(circle1, "<ButtonPress-1>", self.onCircleClick)

        for k in range(2, -1, -1):
            # Quadrant I
            # Choose X
            pytha_x = (self.radii[i] * (x_axis_adjustments[k]))
            x_pos = self.mid_x + pytha_x
            # Derive Y
            pytha_y = self.getY(pytha_x, self.radii[i])
            y_pos = self.mid_y + pytha_y

            # Quadrant III
            q3_x_pos = self.mid_x - pytha_x
            q3_y_pos = self.mid_y - pytha_y

            circle5 = self._create_circle(x_pos, y_pos, self.target_sizes[j], "#0000FF")
            self.canvas1.tag_bind(circle5, "<ButtonPress-1>", self.onCircleClick)

            circle6 = self._create_circle(q3_x_pos, q3_y_pos, self.target_sizes[j], "#0000FF")
            if k == 0:
                self.canvas1.tag_bind(circle6, "<ButtonPress-1>", self.lastCircleClick)
            else:
                self.canvas1.tag_bind(circle6, "<ButtonPress-1>", self.onCircleClick)

        self.canvas1.itemconfig(circle3, state="normal", fill="#FF0000")

    def _create_circle(self, center_x, center_y, radius, color):
        print("creating circle")
        circle = self.canvas1.create_oval(center_x-radius, center_y-radius,
                                          center_x+radius, center_y+radius, outline="#808080", fill="#FFFFFF", state="disabled")
        return circle


def main():
    tk = Tk()
    # Geometry of the Application Window
    tk.geometry('900x800+10+50')
    fitts_app = Fitts(tk)
    fitts_app.mainloop()


if __name__ == '__main__':
    main()