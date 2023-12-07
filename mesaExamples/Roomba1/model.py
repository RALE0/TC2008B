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
        agent_reporters={"Battery": lambda a: a.battery if isinstance(a, RoombaAgent) else 0}
        )
        
        self.dirty_cells_percentage = dirty_cells_percent
        self.obstacles_cells_percentage = obstacles_cells_percent
        
        # Calculate the number of dirty cells and obstacle cells based on percentages
        num_total_cells = width * height - 1 # -1 because the charging station is always in the position 1,1
        num_dirty_cells = int(num_total_cells * (dirty_cells_percent / 100))
        num_obstacle_cells = int(num_total_cells * (obstacles_cells_percent / 100))        

        # Creates the border of the grid
        # border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # # Add obstacles to the grid border
        # for pos in border:
        #     obs = ObstacleAgent(pos, self)
        #     self.grid.place_agent(obs, pos)
            
        # Add roomba agents to the grid in the position 1,1 
        # roomba = RoombaAgent(0, self, (1,1))
        # self.grid.place_agent(roomba, (1,1))
        # self.schedule.add(roomba)
        
        # # Add Charging station to the grid in the position 1,1
        # station = ChargingStationAgent(1, self)
        # self.schedule.add(station)
        # self.grid.place_agent(station, (1,1))
        # Add the Charging station agent to the random empty grid cell selected for the roomba agents
        

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        if N == 1:
            # Si solo hay un agente, colocarlo en la posición (1,1)
            station_id = 2
            roomba_id = 3
            station = ChargingStationAgent(station_id, self)
            roomba = RoombaAgent(roomba_id, self, (1,1))

            # Agregar estación y Roomba al modelo
            self.schedule.add(station)
            self.grid.place_agent(station, (1,1))
            self.schedule.add(roomba)
            self.grid.place_agent(roomba, (1,1))
        else:
            for i in range(N):
                # IDs separados para estaciones y Roombas
                station_id = i * 2 + 2
                roomba_id = i * 2 + 3
                charging_station_pos = pos = pos_gen(self.grid.width-1, self.grid.height-1)

                station = ChargingStationAgent(station_id, self)
                roomba = RoombaAgent(roomba_id, self, charging_station_pos)

                # Agregar estaciones y Roombas al modelo
                self.schedule.add(station)
                self.grid.place_agent(station, charging_station_pos)
                self.schedule.add(roomba)
                self.grid.place_agent(roomba, charging_station_pos)
            
        
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

        # all_at_charging_stations = all(
        #     isinstance(agent, RoombaAgent) and agent.pos == agent.charging_station_pos
        #     for agent in self.schedule.agents
        # )
        # if all_at_charging_stations:
        #     print("All agents at charging stations")
        #     print("Simulation finished")
        #     self.running = False
        self.max_time_seconds = max_time_seconds
        self.max_steps = max_steps
        self.start_time = time.time()

    def step(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        if elapsed_time < self.max_time_seconds:
            '''Advance the model by one step.'''
            self.schedule.step()
            self.datacollector.collect(self)
            print(f"Elapsed time: {elapsed_time}\n")
        else:
            self.running = False # Stop the model if the time is over
            print("Time is over")
        
  