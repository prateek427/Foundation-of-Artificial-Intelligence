from math import *
from collections import deque
import random, time, math
import decimal
import sys
import random

# A class for BFS which holds the number of Lizards and possible moves

class BFS:
  def __init__(self, lizards, moves):
    self.lizards = lizards
    self.moves = moves

  def set_queens(self, lizards):
    self.lizards = lizards
  def set_moves(self, moves):
    self.moves = moves


# A function which runs the BFS algorithm and returns the positions of the lizards

def bfs():
  bfsq = deque()
  if n == 1:
    if q == 1 and not treeBFS:
      return [1]
    else:
      return False

  counter = 0
  for i in range(0, n*n):
    if i not in treeBFS:
      bfsq.append(BFS([i], available_board_moves(i, sorted(list(set(xrange(i,n*n)) - set(treeBFS))), [])))
      counter += 1
    if counter == q:
      break

  if q == 1:
    return bfsq.popleft().lizards

  while bfsq:
    a = bfsq.popleft()
    visited = []
    for num in a.moves:
      lizards = a.lizards[:]
      if treeBFS:
        treeCount = cumulativeTrees[(num/n)]
      else:
        treeCount = 0
      if (n - num/n) +  treeCount < (q - len(lizards)):
        break
      lizards.append(num)
      visited.append(num)
      if len(lizards) == q:
        return lizards
      else:
        g = BFS(lizards, dfsOperation(num, a.moves, visited))
        bfsq.append(g)

# A function which returns the available board moves after the operation is run

def available_board_moves(num,l,visited):
  leftDiagonalList = []
  for number in xrange(num, n*n, (n-1)):
    leftDiagonalList.append(number)
    if (number in xrange(0,(num/n)+(n-1)*n+1,n)):
      break

  rightDiagonalList = []
  for number in xrange(num, n*n, (n+1)):
    rightDiagonalList.append(number)
    if (number in xrange(n-1,n*n-1,n)):
      break

  if set(xrange(num, (num/n)*n+n)).intersection(treeBFS):
    rowTree = xrange(num,min(list(set(xrange(num, (num/n)*n+n)).intersection(treeBFS))))
  else:
    rowTree = xrange(num, (num/n)*n+n)

  if set(xrange(num, (num%n)+(n-1)*n+1, n)).intersection(treeBFS):
    columnTree = range(num, min(list(set(xrange(num, (num%n)+(n-1)*n+1, n)).intersection(treeBFS))), n)
  else:
    columnTree = xrange(num, (num%n)+(n-1)*n+1, n)

  if set(leftDiagonalList).intersection(treeBFS):
    leftTree = xrange(num, min(list(set(leftDiagonalList).intersection(treeBFS))), n-1)
  else:
    leftTree = leftDiagonalList

  if set(rightDiagonalList).intersection(treeBFS):
    rightTree = xrange(num, min(list(set(rightDiagonalList).intersection(treeBFS))), n+1)
  else:
    rightTree = rightDiagonalList

  available_moves = list(set(l) - set(rowTree) - set(columnTree) - set(leftTree) - set(rightTree)- set(visited))
  return sorted(available_moves)

# Checks if there are any lizards in the diagonals
def check_lizards_in_diagonals(x,y,a,b):
  if x - a == 1:
    return False

  t = x+1
  for i in treeRow[x+1:a]:
    for j in i:
      if abs(t - a) == abs(j - b) and abs(t - x) == abs(j - y):
        return True
    t = t+1

  return False


# Check (i,j) xan be placed at that specific place.
def place(i,j,k):
  x_values = []
  y_values = []
  u = 0

  if j in treeRow[i]:
    return False
  while u < k:
    if j == y_val[u]:
      if filter(lambda x: x in range(0, i), treeColumn[j]):
        if x_val[u] > max(filter(lambda x: x in range(0, i), treeColumn[j])):
          return False
      else:
        return False
    if abs(i - x_val[u]) == abs(j - y_val[u]):
      if tree:
        if not check_lizards_in_diagonals(x_val[u], y_val[u], i, j):
          return False
      else:
        return False
    u = u+1

  return True

# Checks if (i,j) has already been visited
def check_if_visited(i,j, visited):
  if (i,j) not in visited:
    return True
  else:
    return False

# Returns the next (i,j) value.
def return_next_ij(i,j):
  if filter(lambda x: x in range(j, n), treeRow[i]):
    nearestTree =  min(filter(lambda x: x in range(j, n), treeRow[i]))
    if nearestTree + 1 < n:
      return(i, min(filter(lambda x: x in range(j, n), treeRow[i])) + 1)
    else:
      return (i+1,0)
  else:
    return (i+1,0)

# Run DFS and return possible positions of the lizards
def dfs(k, i, j):
  if (k == q):
    return True

  visited = set()

  while i < n:
    if tree:
      treeNumber = cumulativeTrees[i]
    else:
      treeNumber = 0
    if n - i + treeNumber < q - len(x_val):
      break
    if place(i,j,k) and  check_if_visited(i,j,visited):
      visited.add((i,j))
      x_val.append(i)
      y_val.append(j)
      x,y = return_next_ij(i,j)

      if dfs(k+1, x ,y):
        return True
      else:
        del x_val[-1]
        del y_val[-1]

    j = (j+1)%n
    if j == 0:
      i = i+1


  return False

# Calculate the threats posed by lizards to each other
def calculate_threats(num, r):

  threat = 0

  for i  in r:
    if num[0] == i[0]:
      start = min(num[1], i[1])+1
      end   = max(num[1], i[1])
      threat = threat + 1
      while start < end:
        if Matrix[num[0]][start] == 2:
          threat = threat - 1
          break
        start = start+1


    if num[1] == i[1]:
      threat = threat + 1
      start = min(num[0], i[0])+1
      end = max(num[0],i[0])
      while start < end:
        if Matrix[start][num[1]] == 2:
          threat = threat -1
          break
        start = start+1


    if abs(num[0] - i[0]) == abs(num[1] - i[1]):
      threat = threat + 1
      if num[0] < i[0]:
        startVertice = num
        endVertice = i
      else:
        startVertice = i
        endVertice  = num
      if startVertice[1] < endVertice[1]:
        start = startVertice[0]+1
        startY = startVertice[1]+1
        end   = endVertice[0]
        while start < end:
          if Matrix[start][startY] == 2:
            threat = threat - 1
            break
          start = start+1
          startY = startY +1
      else:
        start = startVertice[0]+1
        startY = startVertice[1]-1
        end   = endVertice[0]
        while start < end:
          if Matrix[start][startY] == 2:
            threat = threat - 1
            break
          start = start+1
          startY = startY -1

  return threat

# Generate random queens

def generate_random_queens():
  queens = set()
  while True:
    i = random.randint(0,n-1)
    j = random.randint(0,n-1)
    if (i,j) not in queens and (i,j) not in tree:
      queens.add((i,j))

    if len(queens) == q:
      return queens

# Generate score

def generate_score(queens):
  score = []
  for i in queens:
    queens.remove(i)
    sc = calculate_threats(i, queens)
    queens.add(i)
    score.append(sc)
  return score

# Run the simulated annealing algorithm

def simulated_annealing():
  sch = 0.999
  if len(total) < q:
    return False

  if n + len(tree) < q:
    return False

  queens = generate_random_queens()
  while True:
    temperature = 1600000*14*10
    while temperature > 0.0001:
      # To prevent crossing time limit

      if time.time() - start_time > 280:
        return False
      temperature *= sch
      score =  generate_score(queens)
      sc = sum(score)
      sideQueens = queens.copy()
      if len(total) == q and sc!=0:
        return False
      if sc == 0:
        return queens
      else:
        randomQueen = random.choice(list(queens))
        sideQueens.remove(randomQueen)
        availableMoves = list(total - queens - set(randomQueen))
        sideQueens.add(random.choice(availableMoves))

        dw = sum(generate_score(sideQueens)) - sum(generate_score(queens))
        try:
          exp = decimal.Decimal(decimal.Decimal(math.e) ** (decimal.Decimal(-dw) * decimal.Decimal(temperature)))
        except:
          exp = random.uniform(0,1)


      if dw < 0 or random.uniform(0, 1) < exp:
        queens = sideQueens.copy()
  return "fail"


# Handle input from file
tree = set()
read_data = ""
with open('input.txt', 'rw+') as f:
  algo = f.readline().strip()
  n = int(f.readline().strip())
  q = int(f.readline().strip())
  for line in f:
    read_data = read_data + line.strip()

# Create board for the lizards
Matrix = [[0 for x in range(n)] for y in range(n)]
treeBFS = []

if read_data:
  w = 0
  for i in range(0,n):
    for j in range(0,n):
      if read_data[w] == '2':
        Matrix[i][j] = 2
        treeBFS.append(w)
        tree.add((i,j))
      w = w+1

total = set()
for i in range (0,n):
  for j in range (0,n):
    if (i,j) not in tree:
      total.add((i,j))

if tree:
  numOfTrees = [0 for i in range(0,n)]
  for i in tree:
    numOfTrees[i[0]]+=1
  cumulativeTrees = []
  cumulativeTrees.append(numOfTrees[-1])
  abc = list(reversed(numOfTrees))
  k = 1
  while k < n:
    cumulativeTrees.append(cumulativeTrees[k-1] + abc[k])
    k= k+1

  cumulativeTrees = list(reversed(cumulativeTrees))



treeRow = [[] for item in range(0,n)]
treeColumn = [[] for item in range(0,n)]
for i in tree:
  treeRow[i[0]].append(i[1])
  treeColumn[i[1]].append(i[0])


if algo == 'SA':
  start_time = time.time()
  hasSoultion =  simulated_annealing()
  counter = 0
  if hasSoultion:
    sol = "OK \n"
    for i in range(0,n):
      for j in range(0,n):
        if (i,j) in hasSoultion:
          sol+= "1"
        elif (i,j) in tree:
          sol+="2"
        else:
          sol+="0"
      sol+="\n"
  else:
    sol = "FAIL\n"
elif algo == 'DFS':
  x_val = []
  y_val = []
  start_time = time.time()
  result =  dfs(0,0,0)
  c = 0
  v = 0
  i = 0
  r = []
  if result:
    sol = "OK \n"
    while i < q:
      r.append({x_val[i]: y_val[i]})
      i+=1
    for i in range(0,n):
      for j in range(0,n):
        if {i:j} in r:
          sol+= "1"
        elif (i,j) in tree:
          sol+="2"
        else:
          sol+="0"
      sol+="\n"
  else:
    sol = "FAIL\n"
else:
  hasSoultion = bfs()
  counter = 0
  if hasSoultion:
    sol = "OK \n"
    if n!=1:
      for i in range(0,n*n):
        if i in hasSoultion:
          sol+="1"
        elif i in treeBFS:
          sol+="2"
        else:
          sol+="0"
        counter += 1
        if counter == n:
          sol+="\n"
          counter = 0
    elif n ==1 and q == 1 and not treeBFS:
      sol+="1\n"
  else:
    sol="FAIL\n"

# Write output into the file
f = open('output.txt', 'w+')
f.write(sol)
f.close()
