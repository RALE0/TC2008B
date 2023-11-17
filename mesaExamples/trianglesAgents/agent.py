from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Dead", "Alive"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    # def __init__(self, pos, model):
    #     """
    #     Create a new tree.

    #     Args:
    #         pos: The tree's coordinates on the grid.
    #         model: standard model reference for agent.
    #     """
    #     super().__init__(pos, model)
    #     self.pos = pos
    #     self.condition = "Dead"
    #     self._next_condition = None
    #     self.row_updated = False

#     # def step(self):
#     #     """
#     #     If the tree is Alive, spread it to Dead trees nearby.
#     #     """
#     #     if self.condition == "Alive":
#     #         for neighbor in self.model.grid.iter_neighbors(self.pos, True):
#     #             if neighbor.condition == "Dead":
#     #                 neighbor._next_condition = "Alive"
    
#     # def step(self):
#     #     """
#     #     If the tree is Alive, spread it to Dead trees below.
#     #     """
#     #     neighbors_top_coords = [(self.pos[0]-1, self.pos[1]+1), (self.pos[0], self.pos[1]+1), (self.pos[0]+1, self.pos[1]+1)]
#     #     coord_range = [coord for coord in neighbors_top_coords if self.in_range(*coord)]
#     #     neighbors = self.model.grid.get_cell_list_contents(coord_range)
#     #     neighbors_top_conditions = [neighbor.condition for neighbor in neighbors if neighbor]
        
#     #     if self.condition == "Alive":
#     #         for neighbor in self.model.grid.iter_neighbors(self.pos, True):
#     #             if neighbor.pos[1] < self.pos[1]:
#     #                 if neighbors_top_conditions == "Dead":
#     #                     neighbor._next_condition = "Alive"
#     #                 neighbor._next_condition = "Alive"
#     #             elif neighbor.condition == "Dead" and neighbor.pos[1] == self.pos[1]-1:
#     #                 neighbor._next_condition = "Dead"
#     #             print(f"Self at position {self.pos} has condition {self.condition}")
#     #             print(f"Self at position {self.pos[1]-1} neighnor {neighbor.pos[1]}")
#     #             print(f"Neighbor at position {neighbor.pos} has condition {neighbor.condition}")

    # def step(self):
    #     """
    #     Apply rules to update the condition based on top neighbors.
    #     """
    #     if self.row_updated:
    #         # consultar los vecinos de arriba
    #         top_neighbors_coords = [(self.pos[0]-1, self.pos[1]+1), (self.pos[0], self.pos[1]+1), (self.pos[0]+1, self.pos[1]+1)]
            
    #         coord_range = [coord for coord in top_neighbors_coords if self.in_range(*coord)]
    #         neighbors = self.model.grid.get_cell_list_contents(coord_range)
            
    #         print(f"Neighbor coords {top_neighbors_coords}")
    #         print(f"Valid coords {coord_range}")
    #         print(f"Neighbors {neighbors}")
            
    #         # Extract conditions from neighbors
    #         top_conditions = [neighbor.condition for neighbor in neighbors if neighbor]
            
    #         # print(f"Self at position {self.pos} has condition {self.condition}")
    #         print(f"Top conditions: {top_conditions}")
            
    #         # Define las reglas de actualización
    #         if self.pos[1] < top_neighbors_coords[1][1]:        
    #             # Define the rules
    #             if all(condition == "Dead" for condition in top_conditions):
    #                 self._next_condition = "Dead"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Dead" and top_conditions[1] == "Dead" and top_conditions[2] == "Alive":
    #                 self._next_condition = "Alive"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Dead" and top_conditions[1] == "Alive" and top_conditions[2] == "Dead":
    #                 self._next_condition = "Dead"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Dead" and top_conditions[1] == "Alive" and top_conditions[2] == "Alive":
    #                 self._next_condition = "Alive"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Alive" and top_conditions[1] == "Dead" and top_conditions[2] == "Dead":
    #                 self._next_condition = "Alive"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Alive" and top_conditions[1] == "Dead" and top_conditions[2] == "Alive":
    #                 self._next_condition = "Dead"
    #             elif len(top_conditions) == 3 and top_conditions[0] == "Alive" and top_conditions[1] == "Alive" and top_conditions[2] == "Dead":
    #                 self._next_condition = "Alive"
    #             elif len(top_conditions) == 3 and all(condition == "Alive" for condition in top_conditions):
    #                 self._next_condition = "Dead"
    #         print(f"Next condition: {self._next_condition}")
        
    #     # Marca la fila actual como actualizada
    #     self.row_updated = True

    # def in_range(self, x, y):
    #     return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height

#     # def step(self):
#     #     """
#     #     If the tree is Alive, spread it to Dead trees below and set the condition to "Dead" for trees at the same height.
#     #     """
#     #     if self.condition == "Alive":
#     #         for neighbor in self.model.grid.iter_neighbors(self.pos, True):
#     #             if neighbor.condition == "Dead" and neighbor.pos[1] < self.pos[1]:
#     #                 neighbor._next_condition = "Alive"
#     #             elif neighbor.pos[1] == self.pos[1]:
#     #                 neighbor._next_condition = "Dead"
    
#     # def step(self):
#     #     """
#     #     If the tree is Alive, spread it to Dead trees below and set the condition to "Dead" for trees at the same height.
#     #     """
#     #     if self.condition == "Alive":
#     #         for neighbor in self.model.grid.iter_neighbors(self.pos, True):
#     #             if neighbor.condition == "Dead" and neighbor.pos[1] < self.pos[1]:
#     #                 neighbor._next_condition = "Alive"
#     #             elif neighbor.pos[1] == self.pos[1]:
#     #                 neighbor._next_condition = "Dead"
#     #             print(f"Self at position {self.pos} has condition {self.condition}")
#     #             print(f"Neighbor at position {neighbor.pos} has condition {neighbor.condition}")

#     def step(self):
#         neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
#         state_str = ''.join("1" if neigh.state == "Alive" else "0" for neigh in neighbors)
#         if self.model.current_row > 0:
#             if state_str in {'000', '010', '101', '111'}:
#                 self.next_state = "Dead"
#             else:
#                 self.next_state = "Alive"

    
    
#     def advance(self):
#         """
#         Advance the model by one step.
#         """
#         if self._next_condition is not None:
#             self.condition = self._next_condition


# class TreeCell(Agent):
#     """
#     A tree cell.
    
#     Attributes:
#         x, y: Grid coordinates
#         condition: Can be "Dead", "Alive"
#         unique_id: (x,y) tuple.
#         unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
#     """

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
        self.row_updated = False

    def step(self):
        top_neighbors_coords = [(self.pos[0]-1, self.pos[1]+1), (self.pos[0], self.pos[1]+1), (self.pos[0]+1, self.pos[1]+1)]

        coord_range = [coord for coord in top_neighbors_coords if self.in_range(*coord)]
        neighbors = self.model.grid.get_cell_list_contents(coord_range)
        print(f"Neighbor coords {top_neighbors_coords}")
        print(f"Valid coords {coord_range}")
        print(f"Neighbors {neighbors}")
            
        # Extract conditions from neighbors, considering out-of-range as "Dead"
        top_conditions = [neighbor.condition if neighbor else "Dead" for neighbor in neighbors]
            
        # print(f"Self at position {self.pos} has condition {self.condition}")
        print(f"Top conditions: {top_conditions}")
        x, y = self.pos  # Extraer las coordenadas x e y
        state_str = ''.join("1" if neigh.condition == "Alive" else "0" for neigh in neighbors)
        print(f"{state_str}")
        if self.row_updated:
            if state_str in {'000', '010', '101', '111'}:
                self._next_condition = "Dead"
            else:
                self._next_condition = "Alive"
                
    def in_range(self, x, y):
        return 0 <= x < self.model.grid.width and 0 <= y < self.model.grid.height

    def advance(self):
        if self.pos[1] == self.model.current_row:
            if self._next_condition is not None:
                self.condition = self._next_condition
                self._next_condition = None
