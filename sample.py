import gui

"""
2048 Game
Please read the comments to help clear up any confusion about what the purpose of the various variables are

Before submitting ensure to edit this comment block to include the ID numbers of both group members
Group Member:
Group Member:
"""

# Values to represent the directions the tiles could move
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4

helper = {"count": 0, "Right": RIGHT, "Up": UP, "Left": LEFT, "Down": DOWN}
controls = ["<Right>", "<Left>", "<Up>", "<Down>"]
transition_value = 20


#Problem 1
grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
'''grid[x] gives the rows, grid[x][y] gives the item in the row and column '''

#Problem 2
def empty_slots():
    '''returns all the empty slots on the grid'''
    return [(x,y)  for x in range(0,4) for y in range(0,4) if grid[x][y] ==0]

             
#Problem 3
import random
def random_position():
    '''returns a random empty slot as a tuple containing the row and column'''
    x = random.randint(0,3)
    y = random.randint(0,3)
    if (x,y) in empty_slots():
       return (x,y)
    else:
        return random_position()


#Problem 4
def add_random_number(board):
    '''places a random NumberTile on a random empty position on the board'''
    pos = random_position()
    numtile = gui.random_number()
    grid[pos[0]][pos[1]]=numtile.value
    helper["count"]+=1
    gui.put(board,"Tile number %d " % (helper['count']) ,numtile,pos[0],pos[1])
    return (pos[0],pos[1])


#Problem 5
def find_identifier(board,row,column):
    '''returns the key of a tile on the board given a location'''
    for k,v in board.numbers.iteritems(): 
        if v == (row,column):
            return k


#Problem 6
        
def update_grid(row,column,direction):
    '''updates the grid variable given a slot and the direction of the move in one direction'''

    if direction == UP:
        if row == 0 : 
            return (row,column)
        elif grid[row-1][column] !=0 and grid[row-1][column] != grid[row][column]:
            return (row, column)
        elif grid[row-1][column] ==0:
            grid[row-1][column]= grid[row][column]
            grid[row][column]=0
            return (row-1, column)
        elif grid[row-1][column] == grid[row][column]:
            grid[row-1][column] += grid[row][column]
            grid[row][column] = 0
            return (row-1, column)
               
    if direction == DOWN:
        if row == 3 : 
            return (row,column)
        elif grid[row+1][column] !=0 and grid[row+1][column] != grid[row][column]:
            return (row, column)
        elif grid[row+1][column] ==0:
            grid[row+1][column]= grid[row][column]
            grid[row][column]=0
            return (row+1, column)
        elif grid[row+1][column] == grid[row][column]:
            grid[row+1][column] += grid[row][column]
            grid[row][column] = 0
            return (row+1, column)
  
    if direction == RIGHT:
        if column == 3 : 
            return (row,column)
        elif grid[row][column+1] !=0 and grid[row][column+1] != grid[row][column]:
            return (row, column)
        elif grid[row][column+1] ==0:
            grid[row][column+1]= grid[row][column]
            grid[row][column]=0
            return (row, column+1)
        elif grid[row][column+1] == grid[row][column]:
            grid[row][column+1] += grid[row][column]
            grid[row][column] = 0
            return (row, column+1)

    if direction == LEFT:
        if column == 0 : 
            return (row,column)
        elif grid[row][column-1] !=0 and grid[row][column-1] != grid[row][column]:
            return (row, column)
        elif grid[row][column-1] ==0:
            grid[row][column-1]= grid[row][column]
            grid[row][column]=0
            return (row, column-1)
        elif grid[row][column-1] == grid[row][column]:
            grid[row][column-1] += grid[row][column]
            grid[row][column] = 0
            return (row, column-1)


#Problem 7
'''animates the movement of the tile on the GUI'''
'''def animate_movement(board,key, hdist, vdist, direction):
      
    if direction == UP:
        if vdist < transition_value:
            gui.move_tile(board,key,0,-1*vdist)
            return True
        else:
            gui.move_tile(board,key,0,-1*transition_value)
            return animate_movement(board,key,0,vdist-transition_value, direction)

    if direction == DOWN:
        if vdist < transition_value:
            gui.move_tile(board,key,0,vdist)
            return True
        else:
            gui.move_tile(board,key,0,transition_value)
            return animate_movement(board,key,0,vdist-transition_value, direction)
    
    if direction == RIGHT:
        if vdist < transition_value:
            gui.move_tile(board,key,hdist,0)
            return True
        else:
            gui.move_tile(board,key,transition_value,0)
            return animate_movement(board,key,hdist-transition_value,0, direction)

    if direction == LEFT:
        if vdist < transition_value:
            gui.move_tile(board,key,-1*hdist,0)
            return True
        else:
            gui.move_tile(board,key,-1*transition_value,0)
            return animate_movement(board,key,hdist-transition_value,0, direction)

    return False
'''



#Problem 19
def animate_movement(board,key, hdist, vdist, direction):
    '''updated version of the function that considers whether 2 tiles were merged'''

    def moving(hdist, vdist):
        if direction == UP:
            if vdist < transition_value:
                gui.move_tile(board,key,0,-1*vdist)
                return True
            else:
                gui.move_tile(board,key,0,-1*transition_value)
                return animate_movement(board,key,0,vdist-transition_value, direction)            
       
        if direction == DOWN:
            if vdist < transition_value:
                gui.move_tile(board,key,0,vdist)
                return True
            else:
                gui.move_tile(board,key,0,transition_value)
                return animate_movement(board,key,0,vdist-transition_value, direction)
            
        if direction == RIGHT:
            if vdist < transition_value:
                gui.move_tile(board,key,hdist,0)
                return True
            else:
                gui.move_tile(board,key,transition_value,0)
                return animate_movement(board,key,hdist-transition_value,0, direction)


        if direction == LEFT:
            if vdist < transition_value:
                gui.move_tile(board,key,-1*hdist,0)
                return True
            else:
                gui.move_tile(board,key,0,-1*transition_value)
                return animate_movement(board,key,hdist-transition_value,0, direction)
            

    if moving(hdist,vdist):
        if merge(board, key):
            return False
        else:
            return True
    else:
        return False


#Problem 8          
def move(board,key,direction):
    '''moves a tile by one slots in the given direction until unable to do so'''
    if gui.move_number(board,key,direction,update_grid,animate_movement):
        return move(board,key,direction)


#Problem 9
def move_all_down(board):
    '''moves all the tiles on the board upwards'''
    for column in range (0,4):
        for row in range(3,-1,-1):
            if grid[row][column]!= 0:
                key = find_identifier(board, row, column)
                move(board,key,DOWN)

#Problem 10        
def move_all_up(board):
    '''moves all the tiles on the board downwards'''
    for column in range (0,4):
        for row in range(0,4):
            if grid[row][column]!= 0:
                key = find_identifier(board, row, column)
                move(board,key,UP)

#Problem 11
def move_all_right(board):
    '''moves all the tiles on the board to the right'''
    for row in range (0,4):
        for column in range(3,-1,-1):
            if grid[row][column]!= 0:
                key = find_identifier(board, row, column)
                move(board,key,RIGHT)

#Problem 12
def move_all_left(board):
    '''moves all the tiles on the board to the right'''    
    for row in range (0,4):
        for column in range(0,4):
            if grid[row][column]!= 0:
                key = find_identifier(board, row, column)
                move(board,key,LEFT)


#Problem 13
def move_all(board, event):
    '''moves all the tiles on the board in the direction corresponding to the given event'''
    if event.keysym == "Right":
        move_all_right(board)
    elif event.keysym == "Left":
        move_all_left(board)
    elif event.keysym== "Up":
        move_all_up(board)
    elif event.keysym == "Down":
        move_all_down(board)


#Problem 14 (moves all the tiles on the board in the appropriate direction and adds a random number to the board)
'''
import copy
def keyboard_callback(event, frame, board ):
    grid0 = copy.deepcopy(grid)
    move_all(board,event)
    if grid0!=grid:
        return add_random_number(board)
'''

#Problem 21
import copy
def keyboard_callback(event, frame, board ):
    '''updated version of the function which checks if the game is over'''
    grid0 = copy.deepcopy(grid)
    unbind(frame)
    if is_game_over(board):
        return
    else:
        bind(frame,board)
        move_all(board,event)
        if grid0!=grid:
            add_random_number(board)
    

#Problem 15
def bind(frame,board):
    '''binds all the strings in the 'controls' list to the 'keyboard_callback' function'''
    map(lambda x: frame.bind(x, lambda event: keyboard_callback(event,frame,board)),controls)

#Problem 16
def unbind(frame):
    '''unbinds all the strings in the 'controls' list from the 'keyboard_callback' function'''    
    map(lambda x: frame.unbind(x), controls)


#Problem 18    
def merge(board,key):
    '''merges two tiles if they are in the same position on the grid'''
    (r,c) = gui.find_position(board,key)
    dup = [k for k,v in board.numbers.iteritems() if v == (r,c)]
    if len(dup)==2:
        for k in dup:
            gui.remove_number(board,k)
            del board.numbers[k]
        board.score += grid[r][c]
        gui.update_score(board)
        helper["count"]+=1
        numtile = gui.find_number(grid[r][c])
        gui.put(board,"Tile number %d " % (helper['count']) ,numtile,r,c)
        return True
    else:
        return False


#Problem 20
def is_game_over(board):
    '''shows if the user won the game or not'''
    s = False
    for x in range(0,4):
        for y in range(0,4):
            if grid[x][y] ==2048:      
                gui.game_over(board, True)
                return True
    if len(empty_slots())==0:
        for r in range(0,3):
            for c in range(0,3):
                if grid[r][c]==grid[r+1][c] or grid[r][c]==grid[r][c+1]:
                    s = True
        for r in range(0,3):
            if grid[r][3] == grid[r+1][3]:
                s == True
        for c in range(0,3):
            if grid[3][c]==grid[r][c+1]:
                s == True
        if s == False:         
            gui.game_over(board, False)
            return True
        else:
            return False
        

if __name__ == '__main__':
    """Your Program will start here"""  
    # Finishing setting up your GameBoard here, answer to Question 17 should go here
    
    frame, board = gui.setup()

    #Problem 17
    add_random_number(board)
    add_random_number(board)
    bind(frame,board)
   
    gui.start(frame)
