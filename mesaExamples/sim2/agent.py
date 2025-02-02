from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Dead", "Alive", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
        """
        If the tree is Alive, spread it to Dead trees nearby.
        """
        if self.condition == "Alive":
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.condition == "Dead":
                    neighbor._next_condition = "Alive"
            self._next_condition = "Burned Out"

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition