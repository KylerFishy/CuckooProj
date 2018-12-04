import math
from timeit import default_timer as timer
from random import randint
import pickle
import os


class Cuckoo():

    # Constructor
    def __init__(self, T):
        self.CONSTANT_VAR = T
        self.numKeys = 0
        self.table1 = [None] * (self.CONSTANT_VAR)
        self.table2 = [None] * (self.CONSTANT_VAR)
        self.table3 = [None] * (self.CONSTANT_VAR)
        self.rehashNeeded = False
        self.MAX_RECURSION_DEPTH = 500

    # hash func 1 to go from table1->table2
    def hashF1(self, inVal):
        return inVal % self.CONSTANT_VAR # h1 = x % CONST

    # hash func 2 to go from table2->table3
    def hashF2(self, inVal):
        return math.floor(inVal) % (self.CONSTANT_VAR-1) # h2 = floor(x/CONST) % CONST

    # hash func 2 to go from table3->table1
    def hashF3(self, inVal):
        return math.floor(inVal) % (self.CONSTANT_VAR-2) # h2 = floor(x/CONST) % CONST

    # inserts x into hash slot in table 1 (regardless of whether or not slot was empty)
    # if it was not empty, the value already in the slot gets insertT2() called on it
    def insertT1(self, x, depth):
        t1Val = self.table1[self.hashF1(x)] # use hashf1 on x to find T1 slot and get its value
        if t1Val == None: # if the slot was empty, put x in the slot, we are done
            self.table1[self.hashF1(x)] = x
        else: # if the slot was not empty, put x in anyways but then call insertT2 on the value
            # that was previously in the slot (after making sure we have not recursed too far)
            self.table1[self.hashF1(x)] = x
            if depth > self.numKeys+100 or depth > self.MAX_RECURSION_DEPTH:
                print("Cycle present, rehash needed! depth =", depth)
                return
            self.insertT2(t1Val, depth+1)

    # inserts x into hash slot in table 2 (regardless of whether or not slot was empty)
    # if it was not empty, the value already in the slot gets insertT1() called on it
    def insertT2(self, x, depth):
        t2Val = self.table2[self.hashF2(x)] # use hashf2 on x to find T2 slot and get its value
        if t2Val == None: # if the slot was empty, put x in the slot, we are done
            self.table2[self.hashF2(x)] = x
        else: # if the slot was not empty, put x in anyways but then call insertT1 on the value
            # that was previously in the slot (after making sure we have not recursed too far)
            self.table2[self.hashF2(x)] = x
            if depth > self.numKeys+100 or depth > self.MAX_RECURSION_DEPTH:
                print("Cycle present, rehash needed! depth =", depth)
                return
            self.insertT3(t2Val, depth+1)

    # inserts x into hash slot in table 2 (regardless of whether or not slot was empty)
    # if it was not empty, the value already in the slot gets insertT1() called on it
    def insertT3(self, x, depth):
        t3Val = self.table3[self.hashF3(x)] # use hashf2 on x to find T2 slot and get its value
        if t3Val == None: # if the slot was empty, put x in the slot, we are done
            self.table3[self.hashF3(x)] = x
        else: # if the slot was not empty, put x in anyways but then call insertT2 on the value
            # that was previously in the slot (after making sure we have not recursed too far)
            self.table3[self.hashF3(x)] = x
            if depth > self.numKeys+100 or depth > self.MAX_RECURSION_DEPTH:
                print("Cycle present, rehash needed! depth =", depth)
                return
            self.insertT1(t3Val, depth+1)

    # tries to insert a key into the data structure. First checks if value is already
    # in the tables, and if not, then it calls insertT1 on key.
    def insert(self, x):# show the tables

        if not self.find(x):
            self.insertT1(x, 0)
            self.numKeys += 1 # keep track of how many keys are in the table

    # deletes a key from the data structure if it was present
    def delete(self, x):
        if self.table1[self.hashF1(x)] == x:
            self.table1[self.hashF1(x)] = None
            print("deleted", x)
        elif self.table2[self.hashF2(x)] == x:
            self.table2[self.hashF2(x)] = None
            print("deleted", x)
        elif self.table3[self.hashF3(x)] == x:
            self.table3[self.hashF3(x)] = None
            print("deleted", x)
        else:
            print(x, "not found in table")

    # returns true if the key is in the data structure, false if not
    def find(self, x):
        if self.table1[self.hashF1(x)] == x:
            return True
        elif self.table2[self.hashF2(x)] == x:
            return True
        elif self.table3[self.hashF3(x)] == x:
            return True
        return False

    # shows the contents of the tables
    def printTables(self):
        print("table 1:\n", self.table1)
        print("table 2:\n", self.table2)
        print("table 3:\n", self.table3)




# ========= TESTING =========

# set this to the name of the .txt file with the keys (without the extension)
file = "keys2"

# read the file and store in the list "keys"
with open(file + ".txt") as f:
    content = f.readlines()
content = [int(x.strip()) for x in content]
keys = content
print("number of keys being inserted: " + str(len(keys)) + "\n")

# create a Cuckoo instance and pass the number of keys as T (table size)
x = Cuckoo(round(len(keys)))

# insert keys one by one
start = timer()
for key in keys:
    x.insert(key)
end = timer()
print("time taken: " + str(round(end - start, 7)) + ' seconds \n')

# show the tables
#x.printTables()
print(x.numKeys, "keys in the table")


filename = 'hashTable'
outfile = open(filename,'wb')
pickle.dump(x, outfile)
outfile.close()

print("approx. number bytes for object:", os.path.getsize("hashTable"))
