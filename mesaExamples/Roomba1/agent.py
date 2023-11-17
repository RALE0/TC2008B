# David Santiago Vieyra García A01656030

from mesa import Agent
import numpy as np
from scipy.spatial import distance

class RoombaAgent(Agent):
    def __init__(self, unique_id, model, charging_station_pos):
        super().__init__(unique_id, model)
        self.charging_station_pos = charging_station_pos
        self.direction = 4 # 4 is the center of the grid 
        self.steps_taken = 0 # Number of steps taken by the agent\
        self.visited_cells = set()  # Store visited positions
        self.nonVisited_cells = set()
        self.isCharging = False
        self.battery = 100
        self.state = "Alive"
        self.path = None
    

    def move_towards_charging_station(self):
        x, y = self.pos
        dx = self.charging_station_pos[0] - x
        dy = self.charging_station_pos[1] - y

        # Determine the movement direction towards the charging station
        if abs(dx) > abs(dy):
            new_x = x + np.sign(dx)
            new_y = y
        else:
            new_x = x
            new_y = y + np.sign(dy)

        new_position = (new_x, new_y)

        # Check if the new position is within the grid boundaries and not an obstacle
        if self.model.grid.is_cell_empty(new_position) or new_position == self.charging_station_pos:
            # Move RoombaAgent
            self.model.grid.move_agent(self, new_position)

            # Update visited cells and battery
            self.visited_cells.add(self.pos)
            self.steps_taken += 1
            self.battery -= 1

    def move(self):
        # Check if the battery is low and Roomba is not currently charging
        if self.battery <= 20 and not self.isCharging:
            # Move towards the charging station position
            self.move_towards_charging_station()
            # If Roomba reaches the charging station, start charging
            if self.pos == self.charging_station_pos:
                self.isCharging = True
        elif self.isCharging and self.battery < 100:
            # While charging, increment the battery level
            self.battery += 5
        elif self.isCharging and self.battery == 100:
            # If fully charged, stop charging
            self.isCharging = False
        elif not self.isCharging and self.battery >= 20:
            # Normal movement logic
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=False,
                include_center=True
            )

            # Filter out cells with obstacles
            non_obstacle_steps = [p for p in possible_steps if not any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(p))]

            # Filter visited and unvisited cells
            visited_unvisited = [p for p in non_obstacle_steps if p not in self.visited_cells]

            if visited_unvisited:
                next_move = self.random.choice(visited_unvisited)
            else:
                # If all surrounding cells are visited, randomly choose from available cells (including visited)
                if non_obstacle_steps:
                    next_move = self.random.choice(non_obstacle_steps)
                    # Remove TrashAgent if present
                    cell_contents = self.model.grid.get_cell_list_contents(next_move)
                    trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]
                    if trash_agents:
                        self.model.grid.remove_agent(trash_agents[0])
                        self.battery -= 1
                else:
                    # If no available cells (including visited cells), stay in the current cell
                    next_move = self.pos

            # Move RoombaAgent
            self.model.grid.move_agent(self, next_move)

            # Update visited cells and battery
            self.visited_cells.add(self.pos)
            self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)
            self.steps_taken += 1
            self.battery -= 1
    
        
    # def move(self):
    #     """ 
    #     Determines if the agent can move in the direction that was chosen
    #     """
        
    #     # Get the possible steps      
    #     possible_steps = self.model.grid.get_neighborhood(
    #         self.pos,
    #         moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
    #         include_center=True) 
        
    #     # Filter out cells with obstacles or non-empty cells (except TrashAgent)
    #     non_obstacle_steps = [p for p in possible_steps if self.model.grid.is_cell_empty(p) or any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(p))]
    #     visited_steps = [p for p in non_obstacle_steps if any(isinstance(agent, VisitedCell) for agent in self.model.grid.get_cell_list_contents(p))]
        
    #     # Choose from non-obstacle and non-empty cells
    #     if non_obstacle_steps:
    #         next_move = self.random.choice(non_obstacle_steps)
    #         cell_contents = self.model.grid.get_cell_list_contents(next_move)

    #         # Remove TrashAgent if present
    #         trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]
    #         if trash_agents:
    #             self.model.grid.remove_agent(trash_agents[0])
    #             self.battery -= 1

    #         # Move RoombaAgent
    #         self.model.grid.move_agent(self, next_move)

    #         # Update visited cells and battery
    #         # self.visited_cells.add(self.pos)
    #         self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)
    #         self.steps_taken += 1
    #         self.battery -= 1
    #         print(f"RoombaAgent battery: {self.battery}\n")
        
        
        # Checks which grid cells are empty
        # freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps)) # list(map(function, iterable)) applies the function to every item in the iterable and returns a list of the results.
        
        # next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True] # p for p, f in zip(possible_steps, freeSpaces) if f == True is a list comprehension that creates a list of possible_steps where freeSpaces is True.
        
        # next_move = self.random.choice(next_moves) # Randomly chooses one of the possible steps
        
        # self.battery = self.battery - 1
        
        if self.battery <= 0:
            self.state = "Dead"
            self.battery = 0
            #finish simulation
            self.model.running = False
        
        # # Now move:
        # if self.random.random() < 0.1 and self.battery > 0:
        #     self.visited_cells.add(self.pos)
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken = self.steps_taken + 1
        #     self.battery = self.battery - 1
        #     self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)

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
