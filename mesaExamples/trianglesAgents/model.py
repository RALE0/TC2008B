import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from agent import TreeCell

class Triangles(Model):
    """
        Simple Forest Fire model.

        Attributes:
            height, width: Grid size.
            density: What fraction of grid cells have a tree in them.
    """

    def __init__(self, height=50, width=50, density=0.50):
        """
        Create a new forest fire model.
        
        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """

        # Set up model objects
        # SimultaneousActivation is a Mesa object that runs all the agents at the same time. 
        # This is necessary in this model because the next state of each cell depends on the current state of all its neighbors -- before they've changed.
        # This activation method requires that all the agents have a step() and an advance() method. 
        # The step() method computes the next state of the agent, and the advance() method sets the state to the new computed state.
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=False)
        self.current_row = height - 2

        # A datacollector is a Mesa object for collecting data about the model.
        # We'll use it to count the number of trees in each condition each step.
        self.datacollector = DataCollector(
            {
                "Dead": lambda m: self.count_type(m, "Dead"),
                "Alive": lambda m: self.count_type(m, "Alive"),
            }
        )

        for contents, (x,y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree in the specified row (y=49)
                new_tree = TreeCell((x, y), self)
                
                # Set all trees in the first column Alive.
                if y == 49:  # Fila superior
                    if self.random.random() < 0.4:
                        new_tree.condition = "Alive"
                    else:
                        new_tree.condition = "Dead"
                        
                self.grid.place_agent(new_tree, (x, y)) 
                self.schedule.add(new_tree)
                
        
        self.running = True
        self.datacollector.collect(self)


    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if we at the bottom
        # if self.count_type(self, "Alive") == 0:
        #     self.running = False
        # Halt at the bottom
        self.current_row -= 1
        if self.current_row < 0: 
            self.running = False

    # staticmethod is a Python decorator that makes a method callable without an instance.
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count