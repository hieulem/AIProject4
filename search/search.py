# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util,time

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):

  #get map's outline

  w = problem.walls.width
  h = problem.walls.height
  sx, sy = problem.getStartState()
  goalx,goaly = problem.goal

 #define the notion to each position in map: (1,1) --> cell01

  notion = []
  t=0
  for i in range(0,w):
    notion.append([])
  for i in range(0,w):
    for j in range(0,h):
        notion[i].append(t)
        t=t+1

 #prolog file contains connection between cell
  fname = 'connection.P'
  from game import Directions
  dict ={}
  with open(fname, 'w') as fout:

    fout.write('\n')
    for i in range(0,w):
        for j in range(0,h):
            if not problem.walls[i][j]:
                if i+1 <= w :
                    if not problem.walls[i+1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i+1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i+1][j].__str__()
                        dict[word] = Directions.EAST                #dictionary translating from strings "cellXcellY" to the real direction in game
                if i-1 >= 0 :
                    if not problem.walls[i-1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i-1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i-1][j].__str__()
                        dict[word] = Directions.WEST
                if j+1 <= h :
                    if not problem.walls[i][j+1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j+1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j+1].__str__()
                        dict[word] = Directions.NORTH
                if j-1 >= 0 :
                    if not problem.walls[i][j-1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j-1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j-1].__str__()
                        dict[word] = Directions.SOUTH

    fout.close()

 #load prolog fact
  from spade import pyxf
  brain = pyxf.xsb('/home/hieule/Downloads/XSB/bin/xsb')
  brain.load(fname)
  brain.load('dfs.P')
  goal = 'cell'+notion[goalx][goaly].__str__()
  start = 'cell'+notion[sx][sy].__str__()
  feedback = brain.query('dfs('+start+',['+start+'],'+goal+',X).')
  #feedback = brain.query('solve2('+start+','+goal+',X).')
  path=feedback[0].__str__()


  path = path[8:len(path)-3]
  path = path.split(',', 9999)
  #translate the path using dictionary
  path_translated=[]
  for i in range(0,len(path)-1):
      path_translated.append(dict[path[i]+path[i+1]])

  return path_translated

def breadthFirstSearch(problem=None):

  print problem
 #get map's outline

  w = problem.walls.width
  h = problem.walls.height
  sx, sy = problem.getStartState()
  goalx,goaly = problem.goal

 #define the notion to each position in map: (1,1) --> cell01

  notion = []
  t=0
  for i in range(0,w):
    notion.append([])
  for i in range(0,w):
    for j in range(0,h):
        notion[i].append(t)
        t=t+1

 #prolog file contains connection between cell
  fname = 'connection.P'
  from game import Directions
  dict ={}
  with open(fname, 'w') as fout:

    fout.write('\n')
    for i in range(0,w):
        for j in range(0,h):
            if not problem.walls[i][j]:
                if i+1 <= w :
                    if not problem.walls[i+1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i+1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i+1][j].__str__()
                        dict[word] = Directions.EAST                #dictionary translating from strings "cellXcellY" to the real direction in game
                if i-1 >= 0 :
                    if not problem.walls[i-1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i-1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i-1][j].__str__()
                        dict[word] = Directions.WEST
                if j+1 <= h :
                    if not problem.walls[i][j+1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j+1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j+1].__str__()
                        dict[word] = Directions.NORTH
                if j-1 >= 0 :
                    if not problem.walls[i][j-1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j-1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j-1].__str__()
                        dict[word] = Directions.SOUTH

    fout.close()

 #load prolog fact
  from spade import pyxf
  brain = pyxf.xsb('/home/hieule/Downloads/XSB/bin/xsb')
  brain.load(fname)
  brain.load('bfs.P')
  goal = 'cell'+notion[goalx][goaly].__str__()
  start = 'cell'+notion[sx][sy].__str__()
  #feedback = brain.query('dfs('+start+',['+start+'],'+goal+',X).')
  feedback = brain.query('solve('+start+','+goal+',X).')
  path=feedback[0].__str__()
  path = path[8:len(path)-3]
  path = path.split(',', 9999)
  #reverse the path
  path= path[::-1]
  #translate the path using dictionary
  path_translated=[]
  for i in range(0,len(path)-1):
      path_translated.append(dict[path[i]+path[i+1]])

  return path_translated
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."


  "*** YOUR CODE HERE ***"
#get map's outline

  w = problem.walls.width
  h = problem.walls.height
  sx, sy = problem.getStartState()
  goalx,goaly = problem.goal

 #define the notion to each position in map: (1,1) --> cell01

  notion = []
  t=0
  for i in range(0,w):
    notion.append([])
  for i in range(0,w):
    for j in range(0,h):
        notion[i].append(t)
        t=t+1

 #prolog file contains connection between cell
  fname = 'connection.P'
  from game import Directions
  dict ={}
  with open(fname, 'w') as fout:

    fout.write('\n')
    for i in range(0,w):
        for j in range(0,h):
            if not problem.walls[i][j]:
                if i+1 <= w :
                    if not problem.walls[i+1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i+1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i+1][j].__str__()
                        dict[word] = Directions.EAST                #dictionary translating from strings "cellXcellY" to the real direction in game
                if i-1 >= 0 :
                    if not problem.walls[i-1][j]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i-1][j].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i-1][j].__str__()
                        dict[word] = Directions.WEST
                if j+1 <= h :
                    if not problem.walls[i][j+1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j+1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j+1].__str__()
                        dict[word] = Directions.NORTH
                if j-1 >= 0 :
                    if not problem.walls[i][j-1]:
                        fout.write('connect(cell'+ notion[i][j].__str__() +',cell'+ notion[i][j-1].__str__()+ ').')
                        fout.write('\n')
                        word = 'cell'+ notion[i][j].__str__()+'cell'+ notion[i][j-1].__str__()
                        dict[word] = Directions.SOUTH

    fout.close()

    global hname
    hname = 'heuristicvalues.P'
    with open(hname, 'w') as fout:
        for i in range(0,w):
            for j in range(0,h):
                if not problem.walls[i][j]:
                    distant=abs(i - goalx) + abs(j - goaly)
                    fout.write('h(cell'+ notion[i][j].__str__()+ ','+ distant.__str__() + ').')
                    fout.write('\n')

    fout.close()
 #load prolog fact
  from spade import pyxf
  brain = pyxf.xsb('/home/hieule/Downloads/XSB/bin/xsb')
  brain.load(fname)
  brain.load(hname)

  brain.load('astar.P')
  goal = 'cell'+notion[goalx][goaly].__str__()
  start = 'cell'+notion[sx][sy].__str__()
  #feedback = brain.query('dfs('+start+',['+start+'],'+goal+',X).')
  feedback = brain.query('solve2('+start+','+goal+',X).')
  path=feedback[0].__str__()


  path = path[8:len(path)-3]
  path = path.split(',', 9999)
  #reverse the path
  path= path[::-1]
  #translate the path using dictionary
  path_translated=[]
  for i in range(0,len(path)-1):
      path_translated.append(dict[path[i]+path[i+1]])

  return path_translated

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch