import heapq
from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


class AStarNode(SearchNode):    
    def __init__(self, node: SearchNode, estimate: float = 0):
        self.node = node
        self.cost = node.cost
        self.estimate = estimate
        self.priority = self.cost + estimate
    
    def __get_priority(self):
        return self.priority
        
    def get_search_node(self):
        return self.node
        
    def __lt__(self, other):
        return self.__get_priority() < other.__get_priority()


class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, node: any) -> None:
        heapq.heappush(self.queue, node)
    
    def pop(self) -> any:
        return heapq.heappop(self.queue)

    def is_empty(self) -> bool:
        return len(self.queue) == 0
    
    def to_list(self) -> List[any]:
        return self.queue
    
    def clear(self):
        self.queue = []
class AStarSearch(BaseSearch):
    """
    A* search explores the top node provided by a priority queue ordered by f(n) = g(n) + h(n)
    Given: 
        g(n): the path cost 
        h(n): the heuristic estimate.
    """    
    def estimate(self, node: GridPos, goal: GridPos) -> float:
        """
        estimate by manhattan distance
        """
        return abs(node.x - goal.x) + abs(node.y - goal.y)
        

    def __init__(self):
        super().__init__()
        self.frontier: PriorityQueue = PriorityQueue()
    
    def __get_next_node(self) -> (SearchNode):
        if self.frontier.is_empty():
            return None

        try:
            pnode = self.frontier.pop()
            return pnode.get_search_node()
        except IndexError:
            # heap is already empty
            return None
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform a Breadth-First search to find a path to goal.
        """
        self.path = []
        self.visited = set()
        self.explored = []
        self.frontier.clear()
        
        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)
        self.frontier.push(AStarNode(node=current_node, estimate=self.estimate(initial_state, problem.goal_state)))
        
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
                self.path = current_node.get_path_from_root()
                return self.path
            
            # Get all possible successors
            successors = problem.get_successors(current_state)
            
            if not successors:
                break

            # In Consistent A-Star search, we add all unvisited successors to the frontier
            for next_state in successors:
                if next_state not in self.visited:
                    next_node = SearchNode(next_state, current_node, None, current_node.get_cost() + 1)
                    self.frontier.push(AStarNode(node=next_node, estimate=self.estimate(next_state, problem.goal_state)))
            
            current_node = next_node
            
            steps += 1
        
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return self.frontier.to_list()
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored
    
    def get_all_expanded_nodes(self) -> List[SearchNode]:
        return []
    