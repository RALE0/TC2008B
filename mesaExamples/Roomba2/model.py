# David Santiago Vieyra García A01656030

from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import ObstacleAgent, RoombaAgent, TrashAgent, ChargingStationAgent
import time

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, max_time_seconds, max_steps, dirty_cells_percent, obstacles_cells_percent):
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False)  # width, height, and torus = False are parameters of the MultiGrid which means that the grid is not toroidal (no wrap around)

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        # agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0}
        agent_reporters={"Steps": lambda a: a.battery if isinstance(a, RoombaAgent) else 0}
        )
        
        self.dirty_cells_percentage = dirty_cells_percent
        self.obstacles_cells_percentage = obstacles_cells_percent
        
        # Calculate the number of dirty cells and obstacle cells based on percentages
        num_total_cells = width * height - 1 # -1 because the charging station is always in the position 1,1
        num_dirty_cells = int(num_total_cells * (dirty_cells_percent / 100))
        num_obstacle_cells = int(num_total_cells * (obstacles_cells_percent / 100))        

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Add obstacles to the grid border
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
            
        # Add roomba agents to the grid in the position 1,1 
        roomba = RoombaAgent(0, self, (1,1))
        self.grid.place_agent(roomba, (1,1))
        self.schedule.add(roomba)
        
        # Add Charging station to the grid in the position 1,1
        station = ChargingStationAgent(1, self)
        self.schedule.add(station)
        self.grid.place_agent(station, (1,1))
        
        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        
        
        
        # Add the obstacle agent to a random empty grid cell
        for i in range(num_obstacle_cells):
            a = ObstacleAgent(i+1000, self)
            if (a.pos != station.pos):
                self.schedule.add(a)
                pos = pos_gen(self.grid.width, self.grid.height)
                while (not self.grid.is_cell_empty(pos)):
                    pos = pos_gen(self.grid.width, self.grid.height)
                self.grid.place_agent(a, pos)
        
        # Add the trash agent to a random empty grid cell
        for i in range(num_dirty_cells):
                     
            a = TrashAgent(i+2000, self)
            # The position of the trash should be different from the position of the charging station
            if (a.pos != station.pos):
                self.schedule.add(a)
                pos = pos_gen(self.grid.width, self.grid.height)
                while (not self.grid.is_cell_empty(pos)):
                    pos = pos_gen(self.grid.width, self.grid.height)
                    
                self.grid.place_agent(a, pos)
        
        self.datacollector.collect(self)

        self.max_time_seconds = max_time_seconds
        self.max_steps = max_steps
        self.start_time = time.time()

    def step(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        # current_steps = RoombaAgent.steps_taken
        # print(f"current_steps: {current_steps}\n")
        
        # if self.max_steps >= current_steps:
        #     self.schedule.step()
        #     self.datacollector.collect(self)
        # else:
        #     self.running = False
        #     print("Max steps reached")
        
        if elapsed_time < self.max_time_seconds:
            '''Advance the model by one step.'''
            self.schedule.step()
            self.datacollector.collect(self)
            print(f"Elapsed time: {elapsed_time}\n")
        else:
            self.running = False # Stop the model if the time is over
            print("Time is over")
        
  