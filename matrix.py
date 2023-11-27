from fractions import *

matrices = {}

def move (y, x):
    print(f"\033[{y};{x}f")
    print(f"\033[{x}C")

def read():
  print("\033[2J")
  move(0,0)
  print("What size is your matrix? (nxn)")
  size = input()
  size = size.split('x')
  rows = int(size[0])
  cols = int(size[1])
  matrix = [[None] * rows] * cols
  i = 0
  while (i < rows * cols):
    print("\033[2J")
    move(0,0)
    for col in range(rows):
      for row in range(cols):
        if (i // cols == row and i % rows == col):
          print("     ", end="")
        elif (matrix[col][row] == None):
          print(f" ___ ", end="")
        else:
          print(f"{matrix[col][row]:5}", end="")
      print()
    move(1 + i // cols, 4)
    print(f"\033[{6}C")
    value = int(input())
    matrix[col][row] = value
    i += 1

read()
def display(matrix, cursor):
  for col in range(len(matrix)):
    for row in range(len(col)):
      print(f"{matrix[col][row]:5}", end="")
    print()
