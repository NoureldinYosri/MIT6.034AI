# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True;

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True;

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True;

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False;

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    queue = [start];
    parent = {start : ""};
    while len(queue):
        cur = queue.pop(0);
        if cur == goal: break;
        for nxt in graph.get_connected_nodes(cur):
            if nxt not in parent:
                parent[nxt] = cur;
                queue.append(nxt);
    if goal not in parent: return [];
    path = [];
    while goal != "":
        path.append(goal);
        goal = parent[goal];
    path.reverse();
    return path;


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    stack = [start];
    parent = {start : ""};
    while len(stack):
        cur = stack.pop();
        if cur == goal: break;
        for nxt in graph.get_connected_nodes(cur):
            if nxt not in parent:
                parent[nxt] = cur;
                stack.append(nxt);
    if goal not in parent: return [];
    path = [];
    while goal != "":
        path.append(goal);
        goal = parent[goal];
    path.reverse();
    return path;


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    queue = [[start]];
    closed = set();
    while len(queue):
        cur_path = queue.pop(0);
        cur_head = cur_path[-1];
        if cur_head == goal: return cur_path;
        if cur_head in closed: continue;
        closed.add(cur_head);
        frenge = [];
        for nxt in graph.get_connected_nodes(cur_head):
            if nxt not in closed and nxt not in cur_path:
                new_path = [x for x in cur_path];
                new_path.append(nxt);
                frenge.append(new_path);
        frenge.sort(key=lambda path:graph.get_heuristic(path[-1],goal));
        queue = frenge + queue;
    return [];

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    q1 = [];
    q2 = [[start]];
    while len(q2):
        q1 = [x for x in q2];
        q2 = [];
        q1.sort(key=lambda path:graph.get_heuristic(path[-1],goal));
        if len(q1) > beam_width: q1 = q1[:beam_width];
        while len(q1):
            cur_path = q1.pop(0);
            cur_head = cur_path[-1];
            if cur_head == goal: return cur_path;
            for nxt in graph.get_connected_nodes(cur_head):
                if nxt not in cur_path:
                    new_path = [x for x in cur_path];
                    new_path.append(nxt);
                    q2.append(new_path);
    return [];

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    ret = 0;
    for i in xrange(len(node_names) - 1):
        e = graph.get_edge(node_names[i],node_names[i + 1]);
        ret += e.length;
    return ret;

def branch_and_bound(graph, start, goal):
    queue = [[start]];
    while len(queue):
        cur_path = queue.pop(0);
        cur_head = cur_path[-1];
        if cur_head == goal: return cur_path;
        for nxt in graph.get_connected_nodes(cur_head):
            if nxt not in cur_path:
                new_path = [x for x in cur_path];
                new_path.append(nxt);
                queue.append(new_path);
        queue.sort(key=lambda path: path_length(graph,path));
    return [];

def a_star(graph, start, goal):
    queue = [[start]];
    closed = set();
    optimal = [];
    while len(queue):
        cur_path = queue.pop(0);
        cur_head = cur_path[-1];
        if optimal != [] and path_length(graph,cur_path) >= path_length(graph,optimal): break;
        if cur_head == goal:
            if optimal == [] or path_length(optimal) > path_length(cur_path):
                optimal = [x for x in cur_path];
        if cur_head in closed: continue;
        closed.add(cur_head);
        for nxt in graph.get_connected_nodes(cur_head):
            if nxt not in closed and nxt not in cur_path:
                new_path = [x for x in cur_path];
                new_path.append(nxt);
                queue.append(new_path);
        queue.sort(key=lambda path: path_length(graph,path) + graph.get_heuristic(path[-1],goal));
    return optimal;


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for start in graph.nodes:
        if graph.are_connected(start,goal):
            optimal = a_star(graph,start,goal);
            length = path_length(graph,optimal);
            h = graph.get_heuristic(start,goal);
            if h > length: return False;
        elif start == goal and graph.get_heuristic(start,goal) > 0:
            return False;
    return True;

def is_consistent(graph, goal):
    for e in graph.edges:
        u,v = e.node1,e.node2;
        h1,h2 = graph.get_heuristic(u,goal),graph.get_heuristic(v,goal);
        dh = abs(h1 - h2);
        if e.length < dh: return False;
    return True;

HOW_MANY_HOURS_THIS_PSET_TOOK = '1.3'
WHAT_I_FOUND_INTERESTING = 'None'
WHAT_I_FOUND_BORING = 'ALL :('

