from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch


# 定义DFS类
class DepthFirstSearch(BaseSearch):
    def __init__(self): #构造函数
        super().__init__()
        self.explored_nodes = set()
        self.stack = []
        self.path = []

    def search(self, problem):
        start_state = problem.get_initial_state()
        start_node = SearchNode(start_state)
        self.stack = [start_node]
        explored = set()
        self.explored_nodes = set()

        while self.stack:
            node = self.stack.pop()
            state = node.state
            print(f'explored {state}')

            if problem.is_goal_state(state):
                print(f'goal state', node.get_path_from_root())
                self.path = node.get_path_from_root()
                return node.get_path_from_root()
            
            if state in explored:
                continue

            explored.add(state)
            self.explored_nodes.add(node)

            for succ_state in problem.get_successors(state):
                if succ_state not in explored:
                    succ_node = SearchNode(succ_state, parent=node)
                    self.stack.append(succ_node)

        return []
    
    def get_explored_nodes(self):
        return list(self.explored_nodes)
    
    def get_frontier_nodes(self):
        return list(self.stack)