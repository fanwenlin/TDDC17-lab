from vacuum_world.search.breadth_first_search import BreadthFirstSearch
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.world import World
from vacuum_world.world.maze import Maze
from vacuum_world.world.grid_pos import GridPos


def problem1() -> SearchProblem:
    """
    Compose a problem for the search.
    """
    # create a world with a small size for testing
    world = World(width=3, height=3, num_dirt=2, seed=42)
    
    # get the current agent position
    agent_pos = GridPos(world.agent.x, world.agent.y)
    
    # get the first dirt position as goal
    dirt_list = world.get_all_uncleaned_dirt()
    if dirt_list:
        goal_pos = GridPos(dirt_list[0].x, dirt_list[0].y)
    else:
        # fallback to a different position if no dirt
        goal_pos = GridPos(1, 1)

    # compose a problem
    problem = SearchProblem(world, agent_pos, goal_pos)
    return problem

def problem2() -> SearchProblem:
    """
    Compose a problem for the search.
    """
    # create a world with different parameters for testing
    world = World(width=4, height=4, num_dirt=3, seed=123)
    
    # get the current agent position
    agent_pos = GridPos(world.agent.x, world.agent.y)
    
    # get the second dirt position as goal (if exists)
    dirt_list = world.get_all_uncleaned_dirt()
    if len(dirt_list) > 1:
        goal_pos = GridPos(dirt_list[1].x, dirt_list[1].y)
    elif dirt_list:
        goal_pos = GridPos(dirt_list[0].x, dirt_list[0].y)
    else:
        # fallback to a different position if no dirt
        goal_pos = GridPos(2, 2)

    # compose a problem
    problem = SearchProblem(world, agent_pos, goal_pos)
    return problem
    
def test_breadth_first_search():
    search = BreadthFirstSearch()

    p1 = problem1()

    path = search.search(p1)
    print(path)
    assert len(path) > 0