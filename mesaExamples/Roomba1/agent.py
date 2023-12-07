# David Santiago Vieyra García A01656030

from mesa import Agent
import numpy as np
from scipy.spatial import distance
import networkx as nx

class RoombaAgent(Agent):
    def __init__(self, unique_id, model, charging_station_pos):
        super().__init__(unique_id, model)
        self.charging_station_pos = charging_station_pos
        self.direction = 4 # 4 is the center of the grid 
        self.steps_taken = 0 # Number of steps taken by the agent\
        self.visited_cells = set()  # Store visited positions
        self.nonVisited_cells = set() # Store non visited positions
        self.obstacles = set()  # Lista de obstáculos en el camino del coche
        self.trash = set()  # Lista de basura en el camino del coche
        self.isCharging = False
        self.battery = 100
        self.state = "Alive"
        self.path = None
    
    def addNeighborstoSet(self, pos):
        """
        Adds the neighbors of a position to the nonVisited_cells set
        """
        neighbors = self.model.grid.get_neighborhood(
            pos,
            moore=False,
            include_center=True
        )
        for neighbor in neighbors:
            contents = self.model.grid.get_cell_list_contents(neighbor)
            if any(isinstance(agent, ObstacleAgent) for agent in contents):
                self.obstacles.add(neighbor)
            elif any(isinstance(agent, VisitedCell) for agent in contents):
                self.visited_cells.add(neighbor)
            elif any(isinstance(agent, TrashAgent) for agent in contents):
                self.trash.add(neighbor)
            else:
                self.nonVisited_cells.add(neighbor)

    def route2Cell(self, target_cell):
        start = self.pos
        goal = target_cell
        visited_cells = self.visited_cells
        obstacles = self.obstacles
        unvisited_cells = self.nonVisited_cells

        G = nx.Graph()

        for cell in unvisited_cells.union(visited_cells).difference(obstacles):
            G.add_node(cell)
            for neighbor in self.model.grid.get_neighborhood(cell, moore=False):
                if neighbor not in obstacles:
                    G.add_edge(cell, neighbor, weight=1)
        if start not in G or goal not in G:
            return []

        try:
            path = nx.shortest_path(
                G, source=start, target=goal, weight='weight')
            return path
        except nx.NetworkXNoPath:
            return []

    def check_and_share_unvisited_cells(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=2
        )
        for neighbor in neighbors:
            if isinstance(neighbor, RoombaAgent):
                self.nonVisited_cells = self.nonVisited_cells.union(neighbor.nonVisited_cells)

    def move(self):
        # self.check_and_share_unvisited_cells()     
        print("RoombaAgent pos and battery", self.pos, self.battery, self.unique_id)
        self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)
        charging_station_route = self.route2Cell(self.charging_station_pos)           
        if self.isCharging and self.battery < 100:
            # While charging, increment the battery level
            self.battery += 5
        elif self.isCharging and self.battery == 100:
            # If fully charged, stop charging
            self.isCharging = False
            self.battery = 100
        elif self.battery > len(charging_station_route):
            # Normal movement logic
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,
                include_center=True
            )
            # Filter out cells with obstacles
            non_obstacle_steps = [p for p in possible_steps if not any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(p))]

            # Priorize trash neighbor cells
            trash_neighbors = [p for p in non_obstacle_steps if any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(p))]
            # print("Trash neighbors", trash_neighbors)
            # Filter visited and unvisited cells
            #Visited_unvisited with non obstacle cellls and trash cells
            visited_unvisited = [p for p in non_obstacle_steps if p not in self.visited_cells] # This is the list of unvisited cells

            # if visited_unvisited is not empty, add neighbors to nonVisited_cells
            if len(visited_unvisited) > 0:
                for cell in visited_unvisited:
                    self.addNeighborstoSet(cell)
                    
            if len(trash_neighbors) > 0:
                for cell in trash_neighbors:
                    self.addNeighborstoSet(cell)

            print("Visited unvisited", visited_unvisited)
            print("Non visited cells", self.nonVisited_cells)
            self.nonVisited_cells.discard(self.pos)
            # closest_trash = min(self.trash, key=lambda x: distance.euclidean(x, self.pos))
            if self.nonVisited_cells:
                closest_unvisited = min(self.nonVisited_cells, key=lambda x: distance.euclidean(x, self.pos))
                print("Closest unvisited", closest_unvisited)
                if trash_neighbors:
                    next_move = self.random.choice(trash_neighbors)
                    content = self.model.grid.get_cell_list_contents(next_move)
                    self.model.grid.move_agent(self, next_move)
                    self.battery -= 1
                    self.steps_taken += 1
                    self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)
                    if any(isinstance(agent, TrashAgent) for agent in content):
                        self.battery -= 1
                        self.model.grid.remove_agent(content[0])
                        return
                elif closest_unvisited:
                    path_to_unvisited = self.route2Cell(closest_unvisited)
                    if path_to_unvisited and len(path_to_unvisited) > 1:
                        print("Path to unvisited", path_to_unvisited)
                        next_move = path_to_unvisited[1]
                        print("Next move", next_move)
                        self.model.grid.move_agent(self, next_move)
                        self.nonVisited_cells.discard(self.pos)
                        self.visited_cells.add(self.pos)
                        self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)
                        self.steps_taken += 1
                        self.battery -= 1
                        print("Non visited",self.nonVisited_cells)
                        return
            else:
    
                print("Tamaño de charhing station route",len(charging_station_route))
                print("Charging station route", charging_station_route)
                if len(charging_station_route) > 1:
                    # If no available cells go back to charging station and start charging and if no charging station route, 
                    next_move = charging_station_route[1]
                    self.steps_taken += 1
                    self.model.grid.move_agent(self, next_move)
                    self.battery -= 1
                    charging_station_route.pop(0)
                    if self.pos == self.charging_station_pos:
                        self.isCharging = True
                else: 
                    # self.pos == self.charging_station_pos and self.battery == 100:
                    self.state = "Finished"
                    # self.model.running = False
                    print("RoombaAgent Finished, Battery: ",self.battery, "Unique Id: ",self.unique_id)
                    print("In", self.steps_taken, "steps")
                    return
                    
        elif self.battery <= 0:
            self.state = "Dead"
            self.battery = 0
            #finish simulation
            # self.model.running = False
            print("RoombaAgent Dead", self.battery, self.unique_id)
            
        print("RoombaAgent charging_station_route", charging_station_route)
        # Check if the battery is low and Roomba is not currently charging
        if self.battery <= len(charging_station_route) and not self.isCharging:
            print("RoombaAgent battery low", self.battery)
            # Move towards the charging station position
            print("Next Move before pop", charging_station_route[1])
            next_move = charging_station_route[1]
            print("Actual position", self.pos)
            self.model.grid.move_agent(self, next_move)
            self.battery -= 1
            charging_station_route.pop(0)
            print ("Next Move ater pop", next_move)
            # If Roomba reaches the charging station, start charging
            if self.pos == self.charging_station_pos:
                self.isCharging = True   

    def step(self):
        self.move() # Move the agent
    
class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass  
    
class TrashAgent(Agent):
    """
    Trash agent. Just to add trash to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass

class ChargingStationAgent(Agent):
    """
    Charging Station agent. Just to add charging stations to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass
    
class VisitedCell(Agent):
    """
    Visited cell agent. Just to add visited cells to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass
