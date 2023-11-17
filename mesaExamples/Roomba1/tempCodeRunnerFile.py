    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )

        # Filter out cells with obstacles or non-empty cells (except TrashAgent)
        non_obstacle_steps = [p for p in possible_steps if self.model.grid.is_cell_empty(p) or any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(p))]

        # Update visited cells and battery
        self.visited_cells.add(self.pos)
        self.steps_taken += 1
        self.battery -= 1

        # If surrounded by visited cells, navigate around them randomly without repeating cells
        if all(isinstance(agent, VisitedCell) for agent in self.model.grid.get_cell_list_contents(self.pos)):
            visited_neighbors = [neighbor for neighbor in possible_steps if neighbor in self.visited_cells]
            unvisited_neighbors = [neighbor for neighbor in possible_steps if neighbor not in self.visited_cells]

            if unvisited_neighbors:
                next_move = self.random.choice(unvisited_neighbors)
                self.model.grid.move_agent(self, next_move)
                return
            elif visited_neighbors:
                visited_neighbors.remove(self.pos)  # Exclude the current position from visited neighbors
                next_move = self.random.choice(visited_neighbors)
                self.model.grid.move_agent(self, next_move)
                return

        # Choose from non-obstacle and non-empty cells
        if non_obstacle_steps:
            next_move = self.random.choice(non_obstacle_steps)
            cell_contents = self.model.grid.get_cell_list_contents(next_move)

            # Remove TrashAgent if present
            trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]
            if trash_agents:
                self.model.grid.remove_agent(trash_agents[0])
                self.battery -= 1

            # Move RoombaAgent
            self.model.grid.move_agent(self, next_move)

            # Place VisitedCell agent
            self.model.grid.place_agent(VisitedCell(self.unique_id, self.model), self.pos)