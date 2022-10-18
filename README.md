# Shortest Route
This python app finds the shortest route between two geographical points, using the A* algorithm and the OSMNX
library. <br/>
It finds the shortest path considering the length and does not take into account speed limits for the moment.

<img width="50%" src="https://i.ibb.co/QJkC4yv/example.png" alt="Shortest route example">

---
## How to use
Clone this repo and install the requirements with `pip install -r requirements.txt` (if it doesn't work you may need to use winpip and install Fiona then GDAL first).<br/>
Change the start and ending points coordinates in the `main.py` file.

---
## To Do
- Implement Dijkstra and Bellman-Ford algorithm
