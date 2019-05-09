import copy

def take_input():
    """Accepts the size of the chess board"""
    i=open("input2.txt","r")
    global size
    size=int(i.readline().rstrip())
    global police
    police=int(i.readline().rstrip())
    police=2
    global scooter
    scooter=int(i.readline().rstrip())
    occur=[0]*size
    for s in range(size):
        occur[s]=[0]*size

    for row in occur:
        print(row)
            
    print("Size=",size)
    print("Police=",police)
    print("Scooters=",scooter)
    for j in range(scooter):
        k=0
        while k<12:
            column,row=i.readline().rstrip().split(',')
            column=int(column)
            row=int(row)
            occur[row][column]=occur[row][column]+1
            k=k+1
    
        
    

    for row in occur:
        print(row)

    
    
def get_board(size):
    """Returns an n by n board"""
    board = [0]*size
    for ix in range(size):
        board[ix] = [0]*size
    return board

def print_solutions(solutions, size):
    """Prints all the solutions in user friendly way"""
    print("\n")
    for sol in solutions:
        for row in sol:
            print(row)
        print()
            
def is_safe(board, row, col, size):
    """Check if it's safe to place a queen at board[x][y]"""

    #check row on left side
    for iy in range(col):
        if board[row][iy] == 1:
            return False
    
    ix, iy = row, col
    while ix >= 0 and iy >= 0:
        if board[ix][iy] == 1:
            return False
        ix-=1
        iy-=1
    
    jx, jy = row,col
    while jx < size and jy >= 0:
        if board[jx][jy] == 1:
            return False
        jx+=1
        jy-=1
    
    return True

def solve(board, col, size, police):
    """Use backtracking to find all solutions"""
    #base case
    if col >= size:
        return
    #print("Policeman=",police)
  #  for k in range(size):
    for i in range(size):
        if police>0:
            if is_safe(board, i, col, size):
                board[i][col] = 1
                police=police-1
                if (col == size-1 and police==0):
                    add_solution(board)
                    board[i][col] = 0
                    police=police+1
                    if i<size-1:
                        continue
                    #return
                if (police==0):
                    add_solution(board)
                    board[i][col]=0
                    police=police+1
                    if(i==size-1):
                        solve(board, col+1, size, police)
                    else:
                        continue

                else:
                    solve(board, col+1, size, police)
                #backtrack
                board[i][col] = 0
                police=police+1
                #print("Police",police)
            elif(police>=1):
                solve(board, col+1, size, police)
                
            
def add_solution(board):
    """Saves the board state to the global variable 'solutions'"""
    global solutions
    saved_board = copy.deepcopy(board)
    solutions.append(saved_board)

take_input()

board = get_board(size)
solutions = []

solve(board, 0, size, police)

print_solutions(solutions, size)

print("Total solutions = {}".format(len(solutions)))
