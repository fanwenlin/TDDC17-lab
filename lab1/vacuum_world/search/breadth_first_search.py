from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch

from collections import deque


class BreadthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
        # for Breadth-First search, we use queue as frontier
        self.frontier = deque()

        # record visited nodes, to avoid revisiting abundant searching path
        self.visited = set()

        # record where each node state is from
        self.parent_of_node = {}
    
    def __get_next_node(self) -> (SearchNode):
        if self.frontier:
            return self.frontier.popleft()
        else:
            return None
    
    def __find_path(self, goal_node: SearchNode) -> List[SearchNode]:
        path = []
        current_node = goal_node
        while current_node:
            path.append(current_node)
            current_node = self.parent_of_node[current_node.get_state()]
        return path[::-1]
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform a Breadth-First search to find a path to goal.
        """
        self.path = []
        self.visited = set()
        self.explored = []
        
        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)
        self.frontier.append(current_node)
        # keep a record of path codes is not suitable for BFS
        # we'd better keep a record of where is each node expanded from as a hashmap
        # so that when we find the goal, we can find the back path easily
        self.parent_of_node = {initial_state: None}
        steps = 0
        
        while steps < self.max_depth:
            current_node = self.__get_next_node()

            # print(f'explored node: {current_node}')
            if current_node is None:
                # No solutions
                return []

            current_state = current_node.get_state()
            self.visited.add(current_state)
            self.explored.append(current_node)
            
            # Check if we've reached the goal
            if problem.is_goal_state(current_state):
                self.path = self.__find_path(current_node)
                return self.path
            
            # Get all possible successors
            successors = problem.get_successors(current_state)
            
            if not successors:
                break

            # In Breadth-First search, we add all unvisited successors to the frontier
            for next_state in successors:
                if next_state not in self.visited:
                    self.parent_of_node[next_state] = current_node
                    self.frontier.append(SearchNode(next_state, current_node, None, current_node.get_cost() + 1))

            # Create next node and add to path
            next_node = SearchNode(next_state, current_node, None, current_node.get_cost() + 1)
            
            current_node = next_node
            
            steps += 1
        
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored