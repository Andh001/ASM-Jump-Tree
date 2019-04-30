#################################################
# This is string processing project	
#
# The main aim of this project is to visualize
# the flow of ASM instruction.
#
# ASM instructions can be get from Olly debugger
#
# This code will generate the OUTPUT.gv file 
# it can be viewed by Graphviz
# Download Link : https://graphviz.gitlab.io/download/
#
#################################################

INPUT_FILE_NAME = "Input.txt"
OUTPUT_FILE_NAME = "OUTPUT.gv"

from copy import deepcopy
import pdb
def ReadFile(filename):
  with open(filename, "rb") as F:
    return F.read()

a = ReadFile(INPUT_FILE_NAME).replace(";","").replace(">", "")
a = a.replace("\r", "")

g = a.split("\n")

while len(g[-1]) < 2:
  del g[-1]
  
MIN = int(g[0][:8], 16)
MAX = int(g[-1][:8], 16)

i = 0
# to delete the rough data..
while i < len(g):
  if len(g[i]) < 9:
    del g[i]
    i -= 1
  i += 1

def GetIndexConstant():
  # This function will return the actual index of instructions..
  global g
  #pdb.set_trace()
  for i in g:
    if "MOV" in i:
      return i.index("MOV")
  return 13 # it is string position of actual Instruction

k = GetIndexConstant()

addr = []
def GetJMPConstant(inst):
  # this function will return the jump constant present in instruction
  global addr
  inst = inst.replace("SHORT", "")
  inst = inst.replace("FAR", "")
  a = inst.split(" ")
  #import re
  #return re.findall("\w{8}", inst)[:-1]
  # if '.' in inst:
  #   for i in a[::-1]:
  #     i = i.replace(".", "")
  a = a[::-1]
  for i in a:
    try:
      u = int(i, 16)
      return i
    except:
      u=0
  a = a[::-1]
  # for i in a[::-1]:
  #   if "." in i:
  #     #ki = i[::-1]
  #     ki = i.index(".")
  #     i = i[ki+1:]
  #     return i
  #     #if i in addr:
  #     #  return i
  # if "POPESI" == "".join(x for x in a[1:]):
  #   if isLast:
  #     return ""
  # else:
  return "".join(x for x in a[1:])

def isJmp(inst):
  # return type is int
  # this function will return the jump constant if there is an existance of jump in instruction

  # to avoid the unused spaces...
  inst = inst[k:]

  # if there is a jump
  if inst[0] == "J" or inst[1] == "J":
    # return jump constant
    return GetJMPConstant(inst)
  return False

for i in g:
  addr += [i[:8]]

jump = [[]]
# in this array
# we will store the jumps in the format of [[parent, child], [], [], ...]

def searchNode(start, node):
  if node:
    if node.start == start:
      return node
    a =  searchNode(start, node.left)
    if a:
      return a
    a = searchNode(start, node.right)
    if a:
      return a
  return None

class Insts:

  def __init__(self, buff):
    global TTT,MIN,MAX,ty
    # There is need to create the child nodes..
    # Because many nodes can have same child node!!!
    # Before insertion we must check..
    # if that node is exists then we will return that node..
    if type(buff) == str:
      self.start = buff
      self.buff = []
      self.jumpL = ""
      self.jumpR = ""
      self.isInitialized = 0
      self.right = None
      self.left = None
    else:
      self.start = buff[0][:8]
      self.jumpL = ""
      self.jumpR = ""
      self.buff = buff[:-1]
      self.right = None
      self.left = None
      self.isInitialized = 1

      # Strings are initialized..
      # There is need to check the existance of child nodes..
      if isLast:
        return None
      if len(buff) > 1:
        self.jumpR = GetJMPConstant(buff[-2])
        self.jumpL = buff[-1][:8]

        # Checking right node existance..
        # if node is exists
        # then we will attach that node right here..
        global NODS
        for jj in range(ty):
          u = jj
          jj = NODS[jj]
          self.right = searchNode(self.jumpR, jj)
          if self.right:
            break
          jj = u

        if "JMP" not in buff[-2]:
          for jj in range(ty):
            u = jj
            jj = NODS[jj]
            self.left = searchNode(self.jumpL, jj)
            if self.left:
              break
            jj = u
        else:
          self.jumpL = ""
        if not self.right:
          self.right = Insts(self.jumpR)
        if not self.left and "JMP" not in buff[-2]:
          self.left = Insts(self.jumpL)
    if MIN <= int(self.start, 16) and int(self.start, 16) <= MAX:
      self.isPerfect = 1
    else:
      self.isPerfect = 0
    self.tid = 0

  def __or__(self, other):
	# OR operator is overloaded..!
    self.buff = deepcopy(other.buff)
    self.isInitialized = other.isInitialized
    self.jumpL = other.jumpL
    self.jumpR = other.jumpR
    self.right = other.right
    self.left = other.left
    self.start = other.start
    return self

TTT = 0
NODS = [0 for i in range(10)]
ty = 0
SPECIAL = []

PERFECTS = []


def AttachNode(root, nod):
  if root:
    c = 0
    if root.jumpL == nod.start and root.left.isInitialized == 0:
      root.left = nod
      c += 1
    if root.jumpR == nod.start and root.right.isInitialized == 0:
      root.right = nod
      c += 1
    return c + AttachNode(root.left, nod) +  AttachNode(root.right, nod)
  return 0



class Tree:
  def __init__(self):
    self.head = None

  def GetNode(self, buff, head):
    if head:
      if head.jumpL == buff.start or head.jumpR == buff.start:
        return head
      else:
        a = self.GetNode(buff, head.right)
        if a:
          return a
        a = self.GetNode(buff, head.left)
        if a:
          return a
    return None

  def searchNode(self, start, node):
    if node:
      if node.start == start:
        return node
      a =  self.searchNode(start, node.left)
      if a:
        return a
      a = self.searchNode(start, node.right)
      if a:
        return a
    return None

  def AddNode(self, buff):
    global NODS, ty
    if isLast:
      yy = 0
    child = Insts(buff)
    #NODS[ty] = child
    #ty+=1
    if self.head == None:
      self.head = child
      NODS[ty] = child
      ty += 1
      return 1
    else:
      parent = 0
      for jj in range(ty):
        u = jj
        jj = NODS[jj]
        parent += AttachNode(jj, child)
        jj = u
      if not parent:
        NODS[ty] = child
        ty += 1
        return 1
    return 0

isLast = 0

def BUILDT(index):
  global TTT
  # $3 This is out main tree building function it Working Demo function..
  buffer = []
  TTT = Tree()
  # 1. first split it into jumps..
  # 2. name each node into its first address
  f = 0
  skip = 0
  for line in g:
    if "00421D2B" in line:
      #pdb.set_trace()
      iiii = 0
    if skip == 0:
      try:
        JumpConstant = isJmp(line)
      except:
        JumpConstant = False
    buffer += [line]

    if f == 1:
      f = 0
      JumpConstant = False
      if TTT.AddNode(buffer):
        print "===================="
        for qw in buffer[:-1]:
          print qw
      else:
        print "Error while Adding ",buffer
      buffer = [buffer[-1]]
      if isJmp(line):
        JumpConstant = True
        skip = 1
      else:
        skip = 0

    if JumpConstant != False:
      f += 1
  global isLast
  isLast = 1
  TTT.AddNode(buffer)
  return TTT

A = 0
lim = 500

searchN = []
isChenged = 0

def searchNode(start, node):
  global lim, searchN
  if lim == 500:
    searchN = []
  if node and lim:
    lim -= 1
    if node.start not in searchN:
      searchN += [node.start]
    else:
      return searchNode(start, node.right)
    if node.start == start:
      return node
    a =  searchNode(start, node.left)
    if a:
      return a
    a = searchNode(start, node.right)
    if a:
      return a
  return None

wid = []

LOP = []

gg = 0

HH = []
exit = 0
def c(a,b):
  global HH
  if a+b not in HH:
    HH += [a+b] # storing the node relationship in global array as string.. a is parent, b is child
    if b == "":
      global exit
      b = "exit_"+str(exit)
      exit += 1
    return "\""+a+"\"->"+"\""+b+"\""
  return ""

OOPP = ""
opo = []
def printS(node):
  global lim,OOPP,opo
  if node and lim:
    lim -= 1
    str = "\n".join(x for x in node.buff)
    #if str in opo:
    if opo.count(str) == 2:
      return
    else:
      opo += [str]
    if node.start == "010A29F1":
      hh123 = 0;
    if node.left:
      left = "\n".join(x for x in node.left.buff)
      a = c(str, left)+"\n"
      if a != "\n":
        OOPP += a
      else:
        print node.start+"|"+node.left.start
    if node.right != None:
      right = "\n".join(x for x in node.right.buff)
      b = c(str, right)+"\n"
      if b != "\n":
        OOPP += b
      else:
        print node.start+"|"+node.right.start
    printS(node.right)
    printS(node.left)

a = BUILDT(0)
A = a
jj = []

def GetAdrNod(root, jmp, WW):
  if root:
    if root.start in WW:
      return None
    WW += [root.start]
    try:
      if int(root.start, 16) <= jmp and jmp <= int(root.buff[-1][:8], 16):
        return root
    except:
      return None
    wl = deepcopy(WW)
    l = GetAdrNod(root.left, jmp, wl)
    if l:
      return l
    wr = deepcopy(WW)
    r = GetAdrNod(root.right, jmp, wr)
    if r:
      return r
  return None

def ArrangePerfect(nod, WW):
  # This functions is not working..
  # this code is not modifying code in proper format..

  global jj,NODS, ty
  RT = 0
  LF = 0
  # If node having isPerfect 1 then it is perfect node..
  if nod:
    if nod.start in WW:
      return
    else:
      WW += [nod.start]
    #if nod.start not in jj:
    #  jj += [nod.start]
    #else:
    #  return
    if nod.left:
      wl = deepcopy(WW)
      ArrangePerfect(nod.left, wl)
    if nod.right:
      wr = deepcopy(WW)
      ArrangePerfect(nod.right, wr)

    # Now we have that perfect node..
    # first check the left node..
    if nod.left:
      if nod.left.isInitialized == 0:
        # Getting the actual node..
        for par in range(ty):
          u = par
          par = GetAdrNod(NODS[u], int(nod.jumpL, 16), [])
          if par:
            if nod.jumpL == par.start:
              nod.left = par
            else:
              newchild = Insts("0")
              newchild.buff = deepcopy(par.buff)
              newchild.jumpL = deepcopy(par.jumpL)
              newchild.jumpR = deepcopy(par.jumpR)
              newchild.right = par.right
              newchild.left = par.left
              ptr = par.buff
              while nod.jumpL not in ptr[-1][:10]:
                del ptr[-1]
              del ptr[-1]
              ptr = newchild.buff
              while nod.jumpL not in ptr[0][:10]:
                del ptr[0]
              newchild.start = newchild.buff[0][:8]
              del nod.left

              nod.left = newchild
              par.left = newchild

              par.right = None
              par.jumpR = ""

              nod.isPerfect = 0
            LF = 1
            break
          par = u

    if nod.right:
      if nod.right.isInitialized == 0:
        # Getting the actual node..

        for par in range(ty):
          u = par
          par = GetAdrNod(NODS[u], int(nod.jumpR, 16), []) # ok par is pointing to correct node..
          if par:
            if nod.jumpR == par.start:
              nod.right = par
            else:
              newchild = Insts("0")#deepcopy(par)
              newchild.buff = deepcopy(par.buff)
              newchild.jumpL = deepcopy(par.jumpL)
              newchild.jumpR = deepcopy(par.jumpR)
              newchild.right = par.right
              newchild.left = par.left
              ptr = par.buff
              while nod.jumpR not in ptr[-1][:10]:
                del ptr[-1]
              del ptr[-1]
              ptr = newchild.buff
              while nod.jumpR not in ptr[0][:10]:
                del ptr[0]
              newchild.start = newchild.buff[0][:8]
              del nod.right

              nod.right = newchild
              par.left = newchild
              par.jumpL = newchild.start

              par.right = None
              par.jumpR = ""

              #par.right = newchild
              nod.isPerfect = 0
            RT = 1
            break
          par = u
    return RT | LF


cq = 1
for kqq in range(ty):
  cq = ArrangePerfect(NODS[kqq], [])

trs = 1
tr_ids = []

stxs = []

print "-------------------------" # just for debugging..
lim = 500
#print(a.head)
with open(OUTPUT_FILE_NAME, "wb") as W:
   for uu in range(ty):
     printS(NODS[uu])
   W.write('''digraph example{
 node [fontcolor=Blue,shape=rectangle]''')
   W.write(OOPP+"}")

######################################  
# This code is not in proper format. #
# I will update this code later..!   #
##############paradon me##############
