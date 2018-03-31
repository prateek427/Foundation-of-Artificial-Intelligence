from collections import deque
import copy
import time

# Function to calculate score of a particular move
def score(i,j,visited,board):
  for direction in ['l','r','d','u']:
    if direction == 'l':
      if j > 0:
        if board[i][j-1] == board[i][j] and (i,j-1) not in visited:
          visited.add((i,j-1))
          score(i,j-1,visited, board)
    elif direction == 'r':
      if j < n-1:
        if board[i][j+1] == board[i][j] and (i,j+1) not in visited:
          visited.add((i,j+1))
          score(i,j+1,visited, board)
    elif direction == 'u':
      if i > 0:
        if board[i-1][j] == board[i][j] and (i-1,j) not in visited:
          visited.add((i-1,j))
          score(i-1,j,visited, board)
    elif direction == 'd':
      if i < n-1:
        if board[i+1][j] == board[i][j] and (i+1,j) not in visited:
          visited.add((i+1,j))
          score(i+1,j,visited, board)
  return visited

# function to generate gravity on a particular board
def generateGravityMinMax(visited, board):
  for i in range(0,n):
    for j in range(0,n):
      if (i,j) in visited:
        board[i][j] = "*"


  for j in range(0,n):
    new_col =  deque()
    count = 0
    for i in range(0,n):
      if board[i][j] == '*':
        count+=1
      if board[i][j]!= '*':
        new_col.append(board[i][j])

    if count>0:
      for i in range(0,n):
        if count > 0:
          board[i][j] = '*'
          count = count-1
          continue
        board[i][j] = new_col.popleft()

  return board

# Function to generate matrix filled with stars
def generateStarMatrix(visited, board):
  for i in range(0,n):
    for j in range(0,n):
      if (i,j) in visited:
        board[i][j] = "*"

  return board


# Function to check if there are any open positions in the board
def checkStar(board):
  for i in range(0,n):
    for j in range(0,n):
      if board[i][j] != '*':
        return False

  return True

# Function to perform MiniMax Algorithm on the board
def minimax(maxP, minP, board, depth, Max, alpha, beta):

  if depth == 0 or checkStar(board):
    return maxP - minP


  if Max == 'player2':
    boardMin = copy.deepcopy(board)
    bestMin = 1000
    for i in range(0,n):
      for j in range(0,n):
        visited = set()
        if boardMin[i][j] != '*':
          visited.add((i,j))
          visited = score(i,j,visited,board)
          minPoints = len(visited)
          boardMin = generateStarMatrix(visited, boardMin)
          boardMinCopy = generateGravityMinMax(visited, copy.deepcopy(board))
          points = minimax(maxP, (minP+minPoints), boardMinCopy, depth+1, 'player1', alpha, beta)
          if points < bestMin:
            bestMin = points
          if bestMin < beta:
            beta = bestMin
          if alpha >= beta:
            break
    return bestMin
  else:
    boardMax = copy.deepcopy(board)
    bestMax = -1000
    for i in range(0,n):
      for j in range(0,n):
        visited = set()
        if boardMax[i][j] != '*':
          visited.add((i,j))
          visited = score(i,j,visited,board)
          maxPoints = len(visited)
          boardMax = generateStarMatrix(visited, boardMax)
          boardMaxCopy = generateGravityMinMax(visited, copy.deepcopy(board))
          points = minimax(maxPoints+maxP, minP, boardMaxCopy, depth+1, 'player2', alpha, beta)
          if points > bestMax:
            bestMax = points
          if bestMax > alpha:
            alpha = bestMax
          if alpha >= beta:
            break
    return bestMax

def game():
  best = -1000
  total_stars = 0
  board = copy.deepcopy(x)
  for i in range(0,n):
    for j in range(0,n):
      visited = set()
      if board[i][j] != '*':
        visited.add((i,j))
        visited = score(i,j,visited,board)
        maxPoints = len(visited)
        generateStarMatrix(visited, board)
        resultpoints = minimax(maxPoints, 0, generateGravityMinMax(visited, copy.deepcopy(x)), 0, 'player2', -1000, 1000)
        total_stars = total_stars+maxPoints
        if resultpoints > best:
          best = resultpoints
          bestPoints = maxPoints
          move = (i,j)
          bestVisited = visited

read_data = ''
with open('input.txt', 'rw+') as f:
  n = int(f.readline().strip())
  q = f.readline().strip()
  a = f.readline().strip()
  for line in f:
    read_data = read_data + line.strip()

x = [[0 for i in range(n)] for j in range(n)]
k = 0
for i in range(0, n):
  for j in range(0,n):
    x[i][j] = read_data[k]
    k+=1

start_time = time.time()
game()
