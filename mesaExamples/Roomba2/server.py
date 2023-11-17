# David Santiago Vieyra García A01656030

from model import RandomModel, ObstacleAgent, RoombaAgent, TrashAgent, ChargingStationAgent
from agent import VisitedCell
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider, TextElement

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

model_params = {"N": Slider("Número de agentes", 1, 1, 10, 1),
                "width": 10,
                "height": 10,
                "max_time_seconds": Slider("Tiempo máximo de ejecución", 180, 1, 1000, 1),
                "max_steps": Slider("Pasos máximos de ejecución", 300, 1, 1000, 1),
                "dirty_cells_percent":  Slider("Porcentaje de suciedad", 10, 1, 25, 1),
                "obstacles_cells_percent": Slider("Porcentaje de obstáculos", 10, 1, 25, 1)}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Simulacion Roomba 1", model_params)
                       
server.port = 8521 # The default
server.launch()