import math
import sys
from functools import total_ordering

test = False
debug = False

minrun = 32
input = []
runstack = []
totalmerges = 0
totalruns = 0
if not test:
    file_info = open(sys.argv[1], "w")
    file_input = open(sys.argv[2], "r")
    file_output = open(sys.argv[3], "w")
    #file_info_more = open("my-info-more.txt", "w")

def doTest():
    global input

    amtelems = 1000

    input_raw = [5,9,0,1,8,6,11,12,7,31,24,23,91,3,92]
    amt_elems = len(input_raw)

    input1 = []
    for i in range(0,amt_elems):
        n = input_raw[i]
        input.append(TestPoint(n))
        input1.append(TestPoint(n))

    input1.sort()
    timsort()

    print ([str(x) for x in input])
    print ([str(x) for x in input1])
    
    if (input == input1):
        print("GOOD")
    else:
        print("NO--")

def init():
    global test
    # read file into input array
    numPoints = int(file_input.readline())
    for i in range(numPoints):
        line = file_input.readline()
        x = (float(line.split()[0]))
        y = (float(line.split()[1]))
        point = Point(x,y)
        input.append(point)
        #print(point)

    timsort()

    # write input array to file
    for pt in input:
        file_output.write(str(pt.x) + " " + str(pt.y) + "\n")

@total_ordering
class TestPoint:
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return str(self.x)

    def __eq__(self, other):
        return self.x == other.x

    def __lt__(self, other):
        return self.x < other.x
    
    def copy(self):
        return TestPoint(self.x)

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x)+" "+str(self.y)

    def __eq__(self, other):
        comp = compare(self,other)
        return comp[0] == comp[1]

    def __lt__(self, other):
        comp = compare(self,other)
        return comp[0] < comp[1]
    
    def copy(self):
        return Point(self.x,self.y)

def quad(ax, ay):

    """
           1.5
      2     |     1
            |
    2.5-----+-----0.5
            |
      3     |     4
           3.5
    """

    if (ax >  0 and ay == 0):
        aquad = 0.5
    if (ax >  0 and ay >  0):
        aquad = 1
    if (ax == 0 and ay >  0):
        aquad = 1.5
    if (ax <  0 and ay >  0):
        aquad = 2
    if (ax <  0 and ay == 0):
        aquad = 2.5
    if (ax <  0 and ay <  0):
        aquad = 3
    if (ax == 0 and ay <  0):
        aquad = 3.5
    if (ax >  0 and ay <  0):
        aquad = 4
    
    return aquad

# angular sort
# true if elems are sorted
def compare(a,b):
    global test
    #return a < b
    #print("\na: " + str(a) + " b: " + str(b))
    
    ax = a.x
    ay = a.y
    bx = b.x
    by = b.y

    if (   (ax == 0 and ay == 0) 
        or (bx == 0 and by == 0)):
        return True

    aquad = quad(ax,ay)
    bquad = quad(bx,by)

    if aquad == bquad:
        # theta = cos-1(x/sqrt(x^2 + y^2))
        atheta = math.acos(ax / (math.sqrt((ax ** 2) + (ay ** 2))))
        btheta = math.acos(bx / (math.sqrt((bx ** 2) + (by ** 2))))

        if aquad >= 3 or aquad <= 4:
            return [btheta,atheta]
        else:
            return [atheta,btheta]
    else:
        #ret = aquad < bquad
        return [aquad,bquad]

# takes a run in [index,length] form
# prints the elems in array input in the given run
def runToString(run):
    start = run[0]
    stop = start + run[1]
    portion = input[slice(start,stop)]
    return (str(run) + " ~ " + str(portion))

# insertion sort ele into section arr[a,b]
def insert(run):

    # i = position in input array
    # ele = elem to be inserted

    # start i at last elem in run
    i = run[0] + run[1] - 1

    if isinstance(input[i+1], Point):
        ele = input[i+1].copy()
    else:
        ele = input[i+1]

    while i >= run[0] and (ele <= input[i]):
        input[i+1] = input[i]
        input[i] = ele
        i -= 1

# merge sort two runs together
# returns merged run
def merge(run1,run2):

    global test
    global totalmerges
    totalmerges += 1

    # lengths of each run
    n1 = run1[1]
    n2 = run2[1]
 
    # copy to temp arrays L[] and R[]
    L = [0] * (n1)
    R = [0] * (n2)
    for i in range(0, n1):
        L[i] = input[run1[0] + i]
    for j in range(0, n2):
        R[j] = input[run2[0] + j]
 
    # merge temp arrays
    i = 0       # position in run1
    j = 0       # position in run2
    k = run1[0] # merged run

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            input[k] = L[i].copy()
            i += 1
        else:
            input[k] = R[j].copy()
            j += 1
        k += 1
 
    # copy remaining elements of L
    while i < n1:
        input[k] = L[i].copy()
        i += 1
        k += 1
 
    # copy remaining elements of R
    while j < n2:
        input[k] = R[j].copy()
        j += 1
        k += 1
    
    # return merged run
    return [run1[0],n1+n2]

# check for invariants
# (a) |z| >= |x| + |y|: If not, z and y are merged
# (b) |y| >= |x|:       If not, y with x are merged
def invariants():
    global test

    if debug: print("\n-- CHECKING INVARIANTS")

    cont = True
    while cont:

        cont = False

        if len(runstack) >= 3 :
            x = runstack.pop()
            y = runstack.pop()
            z = runstack.pop()

            if not (z[1] >= x[1] + y[1]):
                #file_info_more.write("Fixing invariant 1. Merging runs " + str(z) + " " + str(y) + "\n")
                mergedRun = merge(z,y)
                runstack.append(mergedRun)
                runstack.append(x)
                cont = True
                if debug: print("-- iv1 not satisfied. merging " +
                                 str(z) + " " + str(y))
                if debug: print("-- stack: " + str(runstack))
            else:
                runstack.append(z)
                runstack.append(y)
                runstack.append(x)
                if debug: print("-- iv1 satisfied!")

        if len(runstack) >= 3 :
            x = runstack.pop()
            y = runstack.pop()
            z = runstack.pop()

            if not (y[1] >= x[1]):
                #file_info_more.write("Fixing invariant 1. Merging runs " + str(y) + " " + str(x) + "\n")
                mergedRun = merge(y,x)
                runstack.append(z)
                runstack.append(mergedRun)
                cont = True
                if debug: print("-- iv2 not satisfied. merging " + 
                                str(y) + " " + str(x))
                if debug: print("-- stack: " + str(runstack))
            else:
                runstack.append(z)
                runstack.append(y)
                runstack.append(x)
                if debug: print("-- iv2 satisfied!")

def timsort():

    runcurr = [0,1]

    global test
    global totalruns
    totalruns = 1

    # scan through input array, 
    # start at index 1
    for i in range(1,len(input)):

        

        if debug: print("~ runcurr: " + str(runcurr))

        if (runcurr[1] < minrun) or (i >= len(input) - 2):
            # runcurr length is less than minrun
            # OR there are 2 or less elems left in input

            if debug: print("~     inserting elem to runcurr: " + str(input[i]))

            # add a[i] to current run (insert sort)
            insert(runcurr)
            runcurr[1] += 1


        else:
            # runcurr length is beyond minrun


            lastInRun = input[runcurr[0]+runcurr[1]-1]


            if (lastInRun <= input[i]):
                # if a[i] is larger than last elem in runcurr:


                # add a[i] to end of runcurr 
                # e.g. extend runcurr to include a[i]
                if debug: print("~     inserting elem to runcurr: " + str(input[i]))
                runcurr[1] += 1
            else:
                # else: push current run

                runstack.append(runcurr)

                if debug: print("~   run finished. pushing to runstack")
                if debug: print("~   runstack: " + str(runstack))


                # check for invariants
                if len(runstack) >= 3:
                    invariants()

                # loop on new run, increment totalruns
                totalruns += 1
                runcurr = [i,1]

    # push current run
    runstack.append(runcurr)

    # check for invariants
    if len(runstack) >= 3:
        invariants()

    if debug: 
        print("| SCANNING PHASE FINISHED |")
        print("|        Runstack:        |")
        for r in reversed(runstack):
            print(r)

    if not test:
        file_info.write("after scanning phase, stack contents are\n")

        for r in reversed(runstack):
            file_info.write(str(r) + "\n")

        file_info.write("bottom-up merges\n")

    # bottom-up merge phase

    helpstack = []

    # until single run remains
    while(len(runstack) + len(helpstack) > 1):
        # merge runstack, push to helpstack
        while (len(runstack) >= 2):
            run2 = runstack.pop()
            run1 = runstack.pop()
            if not test:
                file_info.write("merging " + str(run1) + " " + str(run2) + "\n")
            mergedRun = merge(run1,run2)
            helpstack.append(mergedRun)
        
        # move all runs back to runstack
        while (len(helpstack) >= 1):
            run = helpstack.pop()
            runstack.append(run)

    if not test:
        file_info.write("total number of runs found = " + str(totalruns) + "\n")
        file_info.write("total number of merges performed = " + str(totalmerges) + "\n")

if test:
    doTest()
else:
    init()