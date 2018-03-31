# Function to negate a query
def negation(query):
  if '~' in query:
    nquery = query[1:]
  else:
    nquery = '~' + query
  return nquery

# function to perform unification between rules and query
def unification(query, rule, tempList):
  arrayRule = rule.split('|')
  index = 0
  f = False
  predicateQ = query[0:query.find('(')]
  arguDict = {}
  argumentsQ = query[query.find("(")+1:query.find(")")]
  listOfArguments = argumentsQ.split(',')
  for j,r in enumerate(arrayRule):
    predicateR = r[0:r.find('(')]
    argumentsR = r[r.find("(")+1:r.find(")")]
    checkFeasability = 0
    if predicateQ == predicateR:
      listOfArgumentsR = argumentsR.split(',')
      listOfArgumentsQ= argumentsQ.split(',')
      for m in xrange(len(listOfArgumentsR)):
        queryArgument = listOfArgumentsQ[m]
        ruleArgument = listOfArgumentsR[m]
        if queryArgument == ruleArgument:
          checkFeasability = checkFeasability + 1
          continue
        elif queryArgument[0].isupper() and ruleArgument[0].isupper():
          break
        else:
          if queryArgument[0].isupper():
            arguDict[ruleArgument] = queryArgument
          elif ruleArgument[0].isupper():
            arguDict[queryArgument] = ruleArgument
        checkFeasability = checkFeasability + 1
      if checkFeasability == len(listOfArguments):
        indexInRule = j
        f = True
        break

  if f == False:
    return False
  del arrayRule[indexInRule]


  finalArray = arrayRule

  newRule = []

  for i,fin in enumerate(finalArray):
    predicateF = fin[0:fin.find('(')]
    argumentsF = fin[fin.find("(")+1:fin.find(")")]
    listOfArguments = argumentsF.split(',')
    for i,each in enumerate(listOfArguments):
      if each in arguDict.keys():
        listOfArguments[i] = arguDict[each]

    newRule.append(predicateF + '(' + ','.join(listOfArguments) + ')')

  if tempList:
    tempString = '|'.join(tempList)
    for key, value in arguDict.iteritems():
      tempString = tempString.replace(key, value)

    newRul = tempString.split('|') + newRule
    newRuleList = list(set(newRul))
    newRuleList.sort()
    newRuleList = '|'.join(newRuleList)

  newRule.sort()
  newRule = '|'.join(newRule)
  if len(newRule) > 0:
    if tempList:
      # print "JUMANJI"
      return newRuleList
    else:
      return newRule
  else:
    if tempList:
      # print "JUMANJI"
      return newRuleList
    else:
      return True


# function to perform the resilution algorithm
def resolution(query, depth):
  nquery = negation(query)

  if '|' not in query:
    if nquery in lis:
      print query
      return True

  if '|' in query:
    queryList = query.split('|')
    for each in queryList:
      nquery = negation(each)
      for i,rule in enumerate(lis):
        tempList = query.split('|')
        tempList.remove(each)
        newRule = unification(nquery, rule, tempList)
        if not newRule:
          continue
        if newRule in visited:
          continue
        else:
          visited.add(newRule)
        lis.append(newRule)
    return False
  else:
    for i,rule in enumerate(lis):
      newRule = unification(nquery, rule, False)
      if type(newRule) == bool and newRule:
        return True
      if not newRule:
        continue
      if newRule in visited:
        continue
      else:
        visited.add(newRule)
      lis.append(newRule)
    return False

read_data = ''
inputQueries = []
kb = []
with open('input.txt', 'rw+') as f:
  nq = int(f.readline().strip())
  for i in xrange(nq):
    inputQueries.append(f.readline().strip().replace(' ', ''))
  nr = int(f.readline().strip())
  for i in xrange(nr):
    kb.append(f.readline().strip().replace(' ', ''))

nkb = []
for i,rule in enumerate(kb):
  clauses = rule.split('|')
  newClauses = []
  for clause in clauses:
    predicate = clause[0:clause.find('(')]
    arguments = clause[clause.find("(")+1:clause.find(")")].split(',')
    newArguments = []
    for argument in arguments:
      if argument.islower():
        argument = argument + str(i)
      newArguments.append(argument)
    newClauses.append(predicate + '(' + ','.join(newArguments) + ')')
  nkb.append('|'.join(newClauses))


results = []
added = {}
for query in inputQueries:
  lis = nkb[:]
  visited =set()
  predicate = query[0:query.find('(')]
  if '|' not in query and '~' in query:
    nquery = query[1:]
  else:
    nquery = '~' + query
  lis.append(nquery)
  j = 0
  for rule in lis:
    if '|' in rule:
      continue
    result = resolution(rule, 0)
    if result:
      break
    j = j+1
  results.append(result)



sol = ''
for result in results:
  if not result:
    sol = sol + "FALSE" + '\n'
  else:
    sol = sol + "TRUE" + '\n'


f = open('output.txt', 'w+')
f.write(sol)
f.close()

