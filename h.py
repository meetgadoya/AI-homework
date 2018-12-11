import numpy
import time
import copy

######################    Defining Input    #####################################

def next(g, state, act):
   #global g
   a, b = state
   # print(state[1]-1)
   if act == "North":
       b = state[1] - 1
   elif act == "South":
       b = state[1] + 1
   elif act == "East":
       a = state[0] + 1
   elif act == "West":
       a = state[0] - 1

   if (a, b) in g:
       return (a, b)
   else:
       return state


def left(action):
   if action == "North":
       return ("West")
   elif action == "West":
       return ("South")
   elif action == "South":
       return ("East")
   elif action == "East":
       return ("North")


def right(action):
   if action == "North":
       return ("East")
   elif action == "West":
       return ("North")
   elif action == "South":
       return ("West")
   elif action == "East":
       return ("South")


def trans(g, state, action):
   return [(0.7, next(g, state, action)), (0.1, next(g, state, left(action))), (0.1, next(g, state, left(left(action)))), (0.1, next(g, state, right(action)))]


def loop(g, m, n):
   global action
   while True:
       temp = copy.deepcopy(g)
       #print(temp)
       delta = 0
       print(g)

       for state in g:
           maxj = -10000000
           if(state==(m,n)):
           #if (temp[state]["Utility"] == 99):
               continue
           for act in action:
               maxi = sum([p * temp[state1]["Utility"] for (p, state1) in trans(g, state, act)])
               g[state][act] = 0
               if (maxi > maxj):
                   maxj = maxi
                   dir = act

           g[state]["Utility"] = g[state]["Reward"] + 0.9 * maxj
           g[state][dir] = 1

           delta = max(delta, abs(g[state]["Utility"] - temp[state]["Utility"]))

       if (delta < (0.1*0.1/0.9)):
           return temp



start = time.time()


global obs, aa, zz
obs = []
aa = []
zz = []
global s, n, o
#global g
g = {}
i = open("input0.txt", "r")
f = open("output.txt", "w")
global action
s = int(i.readline().rstrip())  # size
n = int(i.readline().rstrip())  # no of cars
o = int(i.readline().rstrip())  # no of obstacles


action = ["North", "South", "East", "West"]
for j in range(s):
   for k in range(s):
       g[(j, k)] = {"North": 0, "South": 0, "East": 0, "West": 0, "Reward": -1, "Utility": 0}

for k in range(o):
   x, y = (i.readline().rstrip().split(','))
   y = int(y)
   x = int(x)
   obs.append((x, y))
   g[(x, y)]["Reward"] -= 100
   #g[(x, y)]["Utility"] -= 100

for k in range(n):
   x, y = (i.readline().rstrip().split(','))
   y = int(y)
   x = int(x)
   aa.append((x, y))

for k in range(n):
   x, y = (i.readline().rstrip().split(','))
   y = int(y)
   x = int(x)
   zz.append((x, y))


while (len(aa) != 0):
   x, y = aa.pop(0)

   m, n = zz.pop(0)
   g[(m, n)]["Reward"] += 100
   g[(m, n)]["Utility"] += 100

   l = loop(g, m, n)
   #for k in l:
    #   print(k, l[k])
   ss = 0

   # for each car 10 times
   for j in range(10):
       #print("##################################### Loop ################################",j)
       r=0
       numpy.random.seed(j)
       swerve=numpy.random.random_sample(1000000)
       k=0
       s1 = (x, y)
       while s1 != (m, n):
           r += l[s1]["Reward"]

           for act in action:
               if l[s1][act] == 1:
                   #print("Swerve:",swerve[k])
                   #print(s1,act)

                   if swerve[k]>0.7:
                       if swerve[k]>0.8:
                           if swerve[k]>0.9:
                               act=left(left(act))
                           else:
                               act=right(act)
                       else:
                           act=left(act)
                   k += 1
                   #print(s1,act)
                   s1 = next(g, s1, act)
                   break
       r+=100
       ss+=r
       #print("Reward", r)

   #print("Reward",ss, (ss//10))
   f.write(str(ss//10)+'\n')
   for p in range(s):
       for q in range(s):
           g[(p,q)] = {"North": 0, "South": 0, "East": 0, "West": 0, "Reward": -1, "Utility": 0}

   for p,q in obs:
       g[(p,q)]={"North": 0, "South": 0, "East": 0, "West": 0, "Reward": -101, "Utility": 0}



#print("Final outcome",final)

end = time.time()
print("Total time=", end - start)

