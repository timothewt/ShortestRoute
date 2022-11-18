from OptimalPathFinder import *
import tkinter as tk
from tkinter import messagebox


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.optimal_path_finder = None
        self.title("Optimal Path Finder")
        self.geometry('290x185')
        self.make_widgets()

    def make_widgets(self):
        """
        Creates and places all the widgets (labels, text entries, button)
        """
        # Starting point
        self.label_start = tk.Label(self, text="Starting point", font='Helvetica 10 bold')
        self.lon1 = tk.StringVar()
        self.label_lon1 = tk.Label(self, text="Longitude")
        self.lat1 = tk.StringVar()
        self.label_lat1 = tk.Label(self, text="Latitude")
        self.entry_lon1 = tk.Entry(self, textvariable=self.lon1)
        self.entry_lat1 = tk.Entry(self, textvariable=self.lat1)
        # Placing widgets
        self.label_start.place(x=10, y=10)
        self.label_lon1.place(x=10, y=30)
        self.entry_lon1.place(x=10, y=51)
        self.entry_lat1.place(x=150, y=51)
        self.label_lat1.place(x=150, y=30)
        # Ending point
        self.label_end = tk.Label(self, text="Ending point", font='Helvetica 10 bold')
        self.lon2 = tk.StringVar()
        self.label_lon2 = tk.Label(self, text="Longitude")
        self.lat2 = tk.StringVar()
        self.label_lat2 = tk.Label(self, text="Latitude")
        self.entry_lon2 = tk.Entry(self, textvariable=self.lon2)
        self.entry_lat2 = tk.Entry(self, textvariable=self.lat2)
        # Placing widgets
        self.label_end.place(x=10, y=80)
        self.label_lon2.place(x=10, y=100)
        self.label_lat2.place(x=150, y=100)
        self.entry_lon2.place(x=10, y=120)
        self.entry_lat2.place(x=150, y=120)
        # Confirm button
        self.btn_find_path = tk.Button(self, text="Find path", command=self.start_finder, width=10, height=1, background="lightgray")
        self.btn_find_path.place(x=100, y=150)

    def start_finder(self) -> None:
        try:
            start = Coordinates(float(self.lon1.get()), float(self.lat1.get()))
            end = Coordinates(float(self.lon2.get()), float(self.lat2.get()))
            self.optimal_path_finder = OptimalPathFinder(start=start, end=end)
            graph, route = self.optimal_path_finder.solve()
            draw_graph(graph)
            draw_route(route)
            draw_node(Node(0, start.lat, start.lon), color="g")
            draw_node(Node(0, end.lat, end.lon), color="b")
            plt.show()
        except ValueError:
            messagebox.showwarning(title="Error", message="Please enter correct latitude and longitude values.")

    def start(self) -> None:
        """
        Starts the GUI (shows the window)
        """
        self.mainloop()
