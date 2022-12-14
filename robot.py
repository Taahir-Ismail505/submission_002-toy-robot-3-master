
replay = False
replayHistory = []
replaySilent = False

valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint','replay','silent','reversed','replay reversed','replay silent','reversed silent','replay reversed silent' , ' replay silent reversed']

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

#TODO: WE NEED TO DECIDE IF WE WANT TO PRE_POPULATE A SOLUTION HERE, OR GET STUDENT TO BUILD ON THEIR PREVIOUS SOLUTION.

def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name.upper()
###############################################################################################
def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """
    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)
    
    return command.lower()
###############################################################################################
def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command,
    as well as the argument(s) for the command
    :return: (command, argument)
    """
    
    args = command.split()
    arg2 = args[1:]

    if len(args) >= 3:
        arg = args[1:]
        ranges = args[3:]
    if 'reversed' in arg2 and 'silent' in arg2 or 'REVERSED' in arg2 and 'SILENT' in arg2 :
            return " ".join(arg2), '' 

    elif 'silent' in args or 'SILENT' in args :
        if len(args) > 2 :
            command = args[2]
            nom = args[1]
            return command , nom
        else :
            return args[1] ,''

    elif 'reversed'  in args or 'REVERSED' in args :
        if len(args) > 2 :
            command = args[2]
            nom = args[1]
            return command , nom
        else:
            return args[1], ''
    
    elif  'off' in args  : 
        return args[0], ''

    elif len(args) > 1:
        split = args[1]  
        splitted = split.split('-')
        if 'replay' in args and len(splitted) > 1:
            no1 = splitted[0]
            no2 = splitted[1]
            if no1.isdigit():
                if no2.isdigit():
                    return args[0],args[1]      
                else:
                    return " ".join(split),''
        return args[0],args[1]
    
    elif len(args) == 1:
        return args[0], ''

###############################################################################################
def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """    
    (command_name, arg1) = split_command_input(command)
    
    return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1) or '-' in arg1)
    
def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False
############################################################################################### 
def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula"""

def show_position(robot_name):
    return ' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').'

def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """
    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positeions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y
    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps
    
    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False
#######################################################################################
def do_replay(robot_name, arg) :
    global replay
    global replayHistory
    History = replayHistory
    return True ,show_position(robot_name)

###############################################################################################
def do_replayreversed_silent(robot_name,arg):
    '''
    from the user input it comes here
    the replay item is split and if the 1st word is a valid command
    and the 2nd item is a int
    then itll will proceed to get updated
    '''
    global replaySilent
    global replay
    replay =True
    replaySilent = True

    if arg != '' :
        replay = True
        replayNum = int(arg)
        count = 0 
        for i in range(len(replayHistory)-1,-1,-1):
            split =replayHistory[i].split()
            firstInstr = split[0]
            secNUM = int(split[1])
            if count == replayNum :
                replay = False 
                break
            count += 1
            if firstInstr == 'forward':
                do_forward(robot_name, secNUM)
            elif firstInstr== 'back':
                do_back(robot_name, secNUM)
            elif firstInstr == 'left':
                do_left_turn(robot_name)
            elif firstInstr == 'right':
                do_right_turn(robot_name)
            elif firstInstr == 'sprint':
                do_sprint(robot_name, secNUM)
        print(" > "+ robot_name + " replayed "+arg +" commands reversed silently." )
        return True,(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').') 
    else :
        for i in range(len(replayHistory)-1,-1,-1):
            split =replayHistory[i].split()
            firstInstr = split[0]
            secNUM = int(split[1])
        
            if i == len(replayHistory):
                replaySilent = False
            elif firstInstr == 'forward':
                do_forward(robot_name, secNUM)
            elif firstInstr== 'back':
                do_back(robot_name, secNUM)
            elif firstInstr == 'left':
                do_left_turn(robot_name)
            elif firstInstr == 'right':
                do_right_turn(robot_name)
            elif firstInstr == 'sprint':
                do_sprint(robot_name, secNUM)
        
        print(" > "+ robot_name + " replayed "+str(len(replayHistory)) +" commands in reverse silently." )
        return True , print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')

#########################################################################################################
def do_replay_silent(robot_name , arg):
    '''
    from the user input it comes here
    the replay item is split and if the 1st word is a valid command
    and the 2nd item is a int
    then itll will proceed to get updated
    '''
    global replaySilent
    global replay
    replay =True
    replaySilent = True

    if arg != '':
        replay = True
        replayNum = int(arg)
        count = 0 
        for i in range(len(replayHistory)-1,-1,-1):
            split =replayHistory[i].split()
            firstInstr = split[0]
            secNUM = int(split[1])
            if count == replayNum :
                replay = False 
                break
            count += 1
            if firstInstr == 'forward':
                do_forward(robot_name, secNUM)
            elif firstInstr== 'back':
                do_back(robot_name, secNUM)
            elif firstInstr == 'left':
                do_left_turn(robot_name)
            elif firstInstr == 'right':
                do_right_turn(robot_name)
            elif firstInstr == 'sprint':
                do_sprint(robot_name, secNUM)
        print(" > "+ robot_name + " replayed "+arg +" commands silently.")
        return True,print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    else:
        for i in range(len(replayHistory)):
            split =replayHistory[i].split()
            firstInstr = split[0]
            secNUM = int(split[1])
            if i == len(replayHistory):
                replaySilent = False
            elif firstInstr == 'forward':
                do_forward(robot_name, secNUM)
            elif firstInstr== 'back':
                do_back(robot_name, secNUM)
            elif firstInstr == 'left':
                do_left_turn(robot_name)
            elif firstInstr == 'right':
                do_right_turn(robot_name)
            elif firstInstr == 'sprint':
                do_sprint(robot_name, secNUM)

        print(" > "+ robot_name + " replayed "+str(len(replayHistory)) +" commands silently.")
        return True,print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')

##############################################################################################
    
def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'
#######################################################################################

def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    global replaySilent
    
    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index
    
    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0
    
    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index
    
    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3
    
    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """
    
    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)

#######################################################################################
def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """
    global replayHistory
    global replay
    global replaySilent
    (command_name, arg) = split_command_input(command)
    '''
    if the replay is true then nothing will append to the list
    and if its false the program will act as normal
    '''

    if command_name == 'off':
        return False
    elif command_name == 'help':
        (do_next, command_output) = do_help()
        print(command_output)
    elif command_name == 'forward':
        if replay == False :
            replayHistory.append(command)
            (do_next, command_output) = do_forward(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
        else :
            (do_next, command_output) = do_forward(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').') 
            
    elif command_name == 'back':
        if replay == False : 
            replayHistory.append(command)  
            (do_next, command_output) = do_back(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')          
        else:
            (do_next, command_output) = do_back(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    
    elif command_name == 'right':
        if replay == False : 
            replayHistory.append(command)  
            (do_next, command_output) = do_right_turn(robot_name)
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
        else:
            (do_next, command_output) = do_right_turn(robot_name)
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    
    elif command_name == 'left':
        if replay == False :
            replayHistory.append(command)
            (do_next, command_output) = do_left_turn(robot_name)
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
        else:
            (do_next, command_output) = do_left_turn(robot_name)  
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    elif command_name == 'sprint':
        if replay == False :
            replayHistory.append(command)
            (do_next, command_output) = do_sprint(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
        else:
            (do_next, command_output) = do_sprint(robot_name, int(arg))
            print(command_output)
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    
    ####################################################################################################
    elif command_name == 'reversed silent':
        (do_next,command_output) = do_replayreversed_silent(robot_name, arg)

    elif command_name == 'replay':
        '''
        when this function is called replay becomes true
        and runs through the list
        what ever the value of i is becomes the command input/user input
        '''

        if len(arg) > 1 :
            splitted = arg.split("-")
            NoFrom = int(splitted[0])
            NoTo = int(splitted[1])
            replay = True
            replayGAP = NoFrom+1 - NoTo
            startingNo = NoFrom -1
            count = 0 
            for i in range(NoFrom-1):
                if count == replayGAP :
                    replay = False 
                    (do_next,command_output) = do_replay(robot_name, arg)
                    break
                count += 1
                command = replayHistory[i]
                handle_command(robot_name, command)
            (do_next,command_output) = do_replay(robot_name, arg)
            print(" > "+ robot_name + " replayed "+str(startingNo)+" commands." )
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')

        elif arg != '':
            replay = True
            replayNum = int(arg)
            count = 0 
            for i in range(len(replayHistory)-1,-1,-1):
                if count == replayNum :
                    replay = False 
                    (do_next,command_output) = do_replay(robot_name, arg)
                    break
                count += 1
                command = replayHistory[i]
                handle_command(robot_name, command)
            (do_next,command_output) = do_replay(robot_name, arg)
            print(" > "+ robot_name + " replayed "+arg +" commands." )
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')

        else :
            replay = True
            for  i in range(len(replayHistory)):
                command = replayHistory[i]
                handle_command(robot_name, command)
                if i == len(replayHistory)-1:
                    replay = False  
            (do_next,command_output) = do_replay(robot_name, arg)
            print(" > "+ robot_name + " replayed "+str(len(replayHistory)) +" commands." )
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    
    elif 'reversed' in command_name  :
        '''
        when this function is called replay becomes true
        and runs through the list
        what ever the value of i is becomes the command input/user input
        this is the same a replay but this loops backwards
        '''
        
        if arg != '':
            replay = True
            replayNum = int(arg)
            count = 0 
            for i in range(replayNum-1,-1,-1):
                if count == replayNum :
                    replay = False 
                    (do_next,command_output) = do_replay(robot_name, arg)
                    break
                count += 1
                command = replayHistory[i]
                handle_command(robot_name, command)
            (do_next,command_output) = do_replay(robot_name, arg)
            print(" > "+ robot_name + " replayed "+arg +" commands in reverse." )
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
        else:
            replay = True
            for  i in range(len(replayHistory)-1,-1,-1):
                if i == len(replayHistory):
                    replay = False
                command = replayHistory[i]
                handle_command(robot_name, command)
            (do_next,command_output) = do_replay(robot_name, arg)
            print(" > "+ robot_name + " replayed "+str(len(replayHistory)) +" commands in reverse." )
            print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')
    
    elif 'silent' in command_name  :
        (do_next,command_output) = do_replay_silent(robot_name, arg) 

    return do_next
#####################################################################################################
def robot_start():
    """This is the entry point for starting my robot"""
    
    global position_x, position_y, current_direction_index,replayHistory,replaySilent,replay
    replayHistory = []
    replay = False
    replaySilent= False

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")
    
    position_x = 0
    position_y = 0
    current_direction_index = 0
    
    command = get_command(robot_name)
    while handle_command(robot_name, command):
        command = get_command(robot_name)
    
    output(robot_name, "Shutting down..")
if __name__ == "__main__":
    robot_start()

