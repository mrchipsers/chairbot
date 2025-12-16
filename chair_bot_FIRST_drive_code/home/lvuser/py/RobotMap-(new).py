'''
By storing port numbers here, we can easily change the "wiring" of the robot
from a single location. Instantiate a PortsList for each subsystem and assign
port numbers as needed.
'''

# Pretty neat trick https://stackoverflow.com/a/23689767/6026013
class dotdict(dict):
    '''dot.notation access to dictionary attributes'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Button mapping for the joystick
buttons = {
    'brake'            : 1,
    'lockStraight'     : 2,
    'reverseDrive'     : 5,
    'climb'            : 6,
    'stopClimb'        : 4,
    'drop'             : 8,
    'preciseDrive'     : 7,
    'fast'             : 10,
    'playCenterAuto'   : 11,
    'setGyro45'        : 8,
    'resetRevolutions' : 3
}
buttons = dotdict(buttons)

# Drivetrain motor assignment
drivetrain = {
    'frontLeftMotor'  : 2,
    'frontRightMotor' : 1,
    'rearLeftMotor'   : 4,
    'rearRightMotor'  : 3
}
drivetrain = dotdict(drivetrain)

# Elevator motor assignment
elevator = {
    'motor' : 0,
    'pos0'  : 0,
    'pos1'  : 1,
    'pos2'  : 2,
    'pos3'  : 3,
    'pos4'  : 4,
}
elevator = dotdict(elevator)

# Default parameters assignment
defaults = {
    'speedSensitivity'   : 0.75,
    'turningSensitivity' : 0.4
}
defaults = dotdict(defaults)
