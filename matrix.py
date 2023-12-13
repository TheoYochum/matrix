from fractions import *
from decimal import Decimal
import math
import copy

variables = {}
header = ""

def main():
  global header
  print("\033[2J", end="")
  move_cursor(1,1)
  variables['A'] = [[Fraction(2), Fraction(7)], [Fraction(1), Fraction(9)]]
  while True:
    header = ""
    print("What would you like to do?")
    command = input().lower()
    match command:
      case "list":
        list_variables()
      case "new matrix":
        read_matrix()
      case "new vector":
        read_vector()
      case "rref":
        RREF()
      case "inverse":
        call_inverse()
      case "determinant":
        call_det()
      case "laplace":
        call_laplace_det()
      case "det inverse":
        call_det_inverse()
      case "help":
        help()
      case "exit":
        return
      case _:
        help()
      
def list_variables():
  items = variables.items()
  for item in items:
    print(f"Name: {item[0]}")
    print(f"Value:\n{to_string(item[1])}")

def get_variable():
  name = input()
  out = copy.deepcopy(variables[name])
  return out

def save_variable(variable):
  print("Would you like to save this variable? y/n")
  answer = input().lower()
  if (not (answer == 'y' or answer == 'yes')):
    return
  print("Give it a name")
  name = input()
  variables[name] = variable

def to_string(item):
  out = ""
  if (type(item) == list):
    if (type(item[0]) == list):
      return print_matrix(item)
    else:
      return "Vector"
  return item

def move_cursor(y, x):
    print(f"\033[{y};{x}f", end="")

def parse_input(value):
  if (value.count('.') == 1):
    try:
      return Fraction(Decimal(value))
    except:
      return "Invalid"
  elif (value.count('/') == 1):
    try:
      return Fraction(value)
    except:
      return "Invalid"
  else:
    try:
      return Fraction(value)
    except:
      return "Invalid"
    

def read_matrix():
  global header
  print("\033[2J", end="")
  move_cursor(0,0)
  print("Name the matrix: ", end="")
  name = input()
  header += "Name the matrix " + name + "\n"
  print("What size is your matrix in the form nxm: ", end="")
  size = input()
  while (size.count('x') != 1):
    print("Invalid input, try again")
    size = input()
  header += "What size is your matrix in the form nxm: " + size + "\n"
  size = size.split('x')
  rows = int(size[0])
  cols = int(size[1])
  matrix = [] * cols
  for col in range(cols):
    matrix.append([])
    for row in range(rows):
      matrix[col].append(None)
  i = 0
  header += "Enter the values"
  width = 1
  while (i < rows * cols):
    header_height = header.count('\n')
    print("\033[2J", end="")
    move_cursor(1,1)
    print(header)
    print(print_matrix(matrix, i=i))
    move_cursor(header_height + 2 + i // cols, (i % cols) * (width + 2) + 3)
    value = input()
    value = parse_input(value)
    if (value == "Invalid"):
      if (not "Invalid" in header):
        header += "\nInvalid input"
      continue
    if ("Invalid" in header):
      header = header[:header.index("Invalid") - 1]
    matrix[i % cols][i // cols] = value
    if (len(str(value)) > width):
      width = len(str(value))
      if (width % 2 == 0):
        width += 1
    i += 1
  print("\033[2J", end="")
  move_cursor(1,1)
  print(header)
  print(print_matrix(matrix))
  variables[name] = matrix

def print_matrix(matrix, i=-1):
  out = ""
  cols = len(matrix)
  rows = len(matrix[0])
  width = 1
  for row in range(rows):
    for col in range(cols):
      if (not matrix[col][row] == None and len(str(matrix[col][row])) > width):
        width = len(str(matrix[col][row]))
        if (width % 2 == 0):
          width += 1
  for row in range(rows):
    if (rows == 1):
      out += "["
    elif (row == 0):
      out += "⎡"
    elif (row == rows - 1):
      out += "⎣"
    else:
      out += "⎢"
    for col in range(cols):
      string = ""
      if (i // cols == row and i % cols == col):
        string = " " * width
      elif (matrix[col][row] == None):
        string = "_" * width
      else:
        string = str(matrix[col][row])
        if (len(string) % 2 == 0):
          string = " " + string
      out += (" " * ((width - len(string)) // 2 + 1)) + string + (" " * ((width - len(string)) // 2 + 1))
    if (rows == 1):
      out += "]\n"
    elif (row == 0):
      out += "⎤\n"
    elif (row == rows - 1):
      out += "⎦\n"
    else:
      out += "⎥\n"
  return out

def read_vector():
  global header
  print("\033[2J", end="")
  move_cursor(0,0)
  print("Name the vector: ", end="")
  name = input()
  header += "Name the vector " + name + "\n"
  print("How many entries: ", end="")
  size = input()
  while (True):
    try:
      size = int(size)
      break
    except:
      print("Invalid input, try again")
      size = input()
  header += "How many entries: " + str(size) + "\n"
  vector = []
  for entry in range(size):
    vector.append(None)
  i = 0
  header += "Enter the values"
  width = 1
  while (i < size):
    header_height = header.count('\n')
    print("\033[2J", end="")
    move_cursor(1,1)
    print(header)
    print(print_vector(vector, i=i))
    move_cursor(header_height + 2 + i, 3)
    value = input()
    value = parse_input(value)
    if (value == "Invalid"):
      if (not "Invalid" in header):
        header += "\nInvalid input"
      continue
    if ("Invalid" in header):
      header = header[:header.index("Invalid") - 1]
    vector[i] = value
    if (len(str(value)) > width):
      width = len(str(value))
      if (width % 2 == 0):
        width += 1
    i += 1
  print("\033[2J", end="")
  move_cursor(1,1)
  print(header)
  print(print_vector(vector))
  variables[name] = vector

def print_vector(vector, i=-1):
  out = ""
  size = len(vector)
  width = 1
  for entry in range(size):
    if (not vector[entry] == None and len(str(vector[entry])) > width):
      width = len(str(vector[entry]))
      if (width % 2 == 0):
        width += 1
  for entry in range(size):
    if (size == 1):
      out += "["
    elif (entry == 0):
      out += "⎡"
    elif (entry == size - 1):
      out += "⎣"
    else:
      out += "⎢"
    string = ""
    if (i == entry):
      string = " " * width
    elif (vector[entry] == None):
      string = "_" * width
    else:
      string = str(vector[entry])
      if (len(string) % 2 == 0):
        string = " " + string
    out += (" " * ((width - len(string)) // 2 + 1)) + string + (" " * ((width - len(string)) // 2 + 1))
    if (size == 1):
      out += "]\n"
    elif (entry == 0):
      out += "⎤\n"
    elif (entry == size - 1):
      out += "⎦\n"
    else:
      out += "⎥\n"
  return out


def row_swap(matrix, r1, r2):
  temp = []
  cols = len(matrix)
  for col in range(cols):
    temp.append(matrix[col][r1])
  for col in range(cols):
    matrix[col][r1] = matrix[col][r2]
    matrix[col][r2] = temp[col]
  return matrix

def scalar_multiplication(matrix, r1, scalar):
  cols = len(matrix)
  for col in range(cols):
    matrix[col][r1] = matrix[col][r1] * Fraction(scalar)
  return matrix

def row_sum(matrix, r1, r2, scalar):
  cols = len(matrix)
  for col in range(cols):
    matrix[col][r2] = matrix[col][r2] + matrix[col][r1] * Fraction(scalar)
  return matrix

def call_RREF():
  print("Enter the matrix name: ")
  matrix = get_variable()
  matrix = RREF(matrix)
  print(print_matrix(matrix))
  save_variable(matrix)

def RREF(matrix):
  cols = len(matrix)
  rows = len(matrix[0])
  pivots = []
  col = 0
  row = 0
  while (col < cols and row < rows):
    if (matrix[col][row] != 1):
      if (matrix[col][row] != 0):
        matrix = scalar_multiplication(matrix, row, (1/matrix[col][row]))
        pivots.append([col,row])
      else:
        for newrow in range(row, rows):
          if matrix[col][newrow] != 0:
            row_swap(matrix, row, newrow)
            if (matrix [col][row] != 1):
              matrix = scalar_multiplication(matrix, row, (1/matrix[col][row]))
            pivots.append([col,row])
            break
      if (matrix[col][row] == 0):
        col += 1
        continue
    else:
      pivots.append([col,row])
    for newrow in range(row + 1, rows):
      if (matrix[col][newrow] != 0):
        matrix = row_sum(matrix, row, newrow, matrix[col][newrow] * -1)
    row += 1
    col += 1
  
  for pivot in pivots:
    col = pivot[0]
    row = pivot[1]
    for newrow in range(row - 1, -1, -1):
      if (matrix[col][newrow] != 0):
        matrix = row_sum(matrix, row, newrow, matrix[col][newrow] * -1)
  return matrix

def call_identity():
  print("How big is n (nxn): ")
  size = input()
  matrix = identity(size)
  print(print_matrix(matrix))
  save_variable(matrix)

def identity(n):
  matrix = []
  for col in range(n):
    matrix.append([])
    for row in range(n):
      if (row == col):
        matrix[col].append(Fraction(1))
      else:
        matrix[col].append(Fraction(0))
  return matrix

def call_augment():
  print("Enter the first matrix's name: ")
  matrix1 = get_variable()
  print("Enter the secon matrix's name: ")
  matrix2 = get_variable()
  matrix = augment(matrix1, matrix2)
  print(print_matrix(matrix))
  save_variable(matrix)

def augment(matrix1, matrix2):
  matrix = []
  for col in range(len(matrix1)):
    matrix.append([])
    for row in range(len(matrix1[0])):
      matrix[col].append(matrix1[col][row])
  if (type(matrix2) == list and type(matrix2[0]) == list):
    for col in range(len(matrix2)):
      matrix.append([])
      for row in range(len(matrix2[0])):
        matrix[len(matrix1) + col].append(matrix2[col][row])
  else:
    matrix.append([])
    for entry in range(len(matrix2)):
      matrix[-1].append(matrix2[entry])
  return matrix

def call_inverse():
  print("Enter the matrix name: ")
  matrix = get_variable()
  matrix = inverse(matrix)
  print(print_matrix(matrix))
  save_variable(matrix)

def inverse(matrix):
  if (len(matrix) != len(matrix[0])):
    print("Not a square matrix")
    return
  det = Fraction(laplace_det(matrix))
  if (det == 0):
    print("Matrix is not invertible")
    return
  augmented = augment(matrix, identity(len(matrix)))
  reduced = RREF(augmented)
  out = []
  for col in range(len(matrix)):
    out.append([])
    for row in range(len(matrix[0])):
      out[col].append(reduced[len(matrix) + col][row])
  return out

def call_det():
  print("Enter the matrix name: ")
  matrix = get_variable()
  det = determinant(matrix)
  print(det)
  save_variable(det)

def determinant(matrix):
  cols = len(matrix)
  rows = len(matrix[0])
  pivots = []
  col = 0
  row = 0
  det = 1
  while (col < cols and row < rows):
    if (matrix[col][row] != 1):
      if (matrix[col][row] != 0):
        det *= 1/matrix[col][row]
        matrix = scalar_multiplication(matrix, row, (1/matrix[col][row]))
        pivots.append([col,row])
      else:
        for newrow in range(row, rows):
          if matrix[col][newrow] != 0:
            row_swap(matrix, row, newrow)
            if (matrix [col][row] != 1):
              det *= 1/matrix[col][row]
              matrix = scalar_multiplication(matrix, row, (1/matrix[col][row]))
            pivots.append([col,row])
            break
      if (matrix[col][row] == 0):
        col += 1
        continue
    else:
      pivots.append([col,row])
    for newrow in range(row + 1, rows):
      if (matrix[col][newrow] != 0):
        matrix = row_sum(matrix, row, newrow, matrix[col][newrow] * -1)
    row += 1
    col += 1
  
  for pivot in pivots:
    col = pivot[0]
    row = pivot[1]
    for newrow in range(row - 1, -1, -1):
      if (matrix[col][newrow] != 0):
        matrix = row_sum(matrix, row, newrow, matrix[col][newrow] * -1)
  if (len(pivots) != len(matrix)):
    return 0
  return 1/det

def call_laplace_det():
  print("Enter the matrix name: ")
  matrix = get_variable()
  det = laplace_det(matrix)
  print(det)
  save_variable(det)

def laplace_det(matrix):
  return laplace_det_recurse(matrix, [])

def laplace_det_recurse(matrix, exclude):
  height = len(exclude)
  cols = len(matrix)
  rows = len(matrix[0])
  if (cols != rows):
    print("Not a square matrix")
    return
  if (height == cols - 1):
    for col in range(cols):
      if (not col in exclude):
        return matrix[col][height]
  det = 0
  sign = 1
  for col in range(cols):
    if (not col in exclude):
      new_exclude = copy.copy(exclude)
      new_exclude.append(col)
      det += sign * matrix[col][height] * laplace_det_recurse(matrix, new_exclude)
      sign *= -1
  return det

def call_transpose():
  print("Enter the matrix name: ")
  matrix = get_variable()
  matrix = transpose(matrix)
  print(print_matrix(matrix))
  save_variable(matrix)

def transpose(matrix):
  cols = len(matrix)
  rows = len(matrix[0])
  out = []
  for col in range(rows):
    out.append([])
    for row in range(cols):
      out[col].append(matrix[row][col])
  return out

def call_cofactor():
  print("Enter the matrix name: ")
  matrix = get_variable()
  matrix = cofactor(matrix)
  print(print_matrix(matrix))
  save_variable(matrix)

def cofactor(matrix):
  cols = len(matrix)
  rows = len(matrix[0])
  out = []
  for col in range(cols):
    out.append([])
    for row in range(rows):
      out[col].append(cofactor_helper(matrix, col, row))
  return out

def cofactor_helper(matrix, col_index, row_index):
  cols = len(matrix)
  rows = len(matrix[0])
  out = []
  col_offset = 0
  if (col_index % 2 == 0 ^ row_index % 2):
    sign = 1
  else:
    sign = -1
  for col in range(cols):
    if (col != col_index):
      out.append([])
      for row in range(rows):
        if (row != row_index):
          out[col + col_offset].append(matrix[col][row])
    else:
      col_offset = -1
  return laplace_det(out) * sign

def call_adjoint():
  print("Enter the matrix name: ")
  matrix = get_variable()
  matrix = adjoint(matrix)
  print(print_matrix(matrix))
  save_variable(matrix)

def adjoint(matrix):
  return transpose(cofactor(matrix))

def call_det_inverse():
  print("Enter the matrix name: ")
  matrix = get_variable()
  det = det_inverse(matrix)
  print(print_matrix(det))
  save_variable(det)

def det_inverse(matrix):
  matrix = copy.deepcopy(matrix)
  det = Fraction(laplace_det(matrix))
  if (det == 0):
    print("Matrix is not invertible")
    return
  matrix = adjoint(matrix)
  cols = len(matrix)
  rows = len(matrix[0])
  for col in range(cols):
    for row in range(rows):
      matrix[col][row] = matrix[col][row] / det
  return matrix

def help():
  out = '''Commands:
List - Lists all the variables
New Matrix - Prompts the user to create a new matrix
New Vector - Prompts the user to create a new vector
RREF - Converts a matrix to reduced row echelon form
'''
  print(out)

main()