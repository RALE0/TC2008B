from model import RandomModel, ObstacleAgent, RoombaAgent, TrashAgent, ChargingStationAgent
from agent import VisitedCell
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    
    if (isinstance(agent, RoombaAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        
        # Change color of visited cells
        # if agent.visited_cells and agent.pos in agent.visited_cells:
        #     portrayal["Color"] = "lightgreen"

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7
        
    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2
    
    if (isinstance(agent, ChargingStationAgent)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.7
    
    if (isinstance(agent, VisitedCell)):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

model_params = {"N":5, "width":10, "height":10, "max_time_seconds": 120, "max_steps": 200, "dirty_cells_percent": 10, "obstacles_cells_percent": 10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()