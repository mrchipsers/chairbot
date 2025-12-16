from commands.Brake import Brake
# from commands.SetGyroAngle import SetGyroAngle
# from commands.SetDistance import SetDistance
# from commands.AutoTest import AutoTest
from commands.fast import fast  # You imported this, so let's use it
from commands.ResetRevolutions import ResetRevolutions
from commands.PreciseDriveWithJoystick import PreciseDriveWithJoystick
from commands.Record import Record
from commands.PlayBack import PlayBack
from subsystems import Drivetrain
import wpilib
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton

import RobotMap

from networktables import NetworkTables, NetworkTablesInstance

joystick = None

def init():
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    global joystick

    global table
    table = NetworkTables.getTable("Smartdashboard")

    table.getNumber('Speed Sensitivity', RobotMap.defaults.turningSensitivity)
    table.getNumber('Turning Sensitivity', RobotMap.defaults.turningSensitivity)

    joystick = Joystick(0)

    brakeButton = JoystickButton(joystick, RobotMap.buttons.brake)
    brakeButton.whileHeld(Brake())

    # setGyro45Button = JoystickButton(joystick, RobotMap.buttons.setGyro45)
    # setGyro45Button.whenPressed(SetGyroAngle(90))

    # setDistance100 = JoystickButton(joystick, 10)
    # setDistance100.whenPressed(SetDistance(100))

    # autoTestButton = JoystickButton(joystick, 12)
    # autoTestButton.whenPressed(AutoTest())

    fastButton = JoystickButton(joystick, 10)
    fastButton.whileHeld(fast())

    resetRevolutionsButton = JoystickButton(joystick, RobotMap.buttons.resetRevolutions)
    resetRevolutionsButton.whenPressed(ResetRevolutions())

    preciseDriveButton = JoystickButton(joystick, RobotMap.buttons.preciseDrive)
    preciseDriveButton.whileHeld(PreciseDriveWithJoystick())

def getJoyTurn():
    joyX = joystick.getX()
    joyZ = joystick.getZ()
    return (joyX if abs(joyX) > abs(joyZ) else joyZ)

def getJoySpeed():
    joyY = joystick.getY()
    joyY2 = joyY * 2
    
    return (joyY2 if fastButton.get() else joyY)


def getSpeedSmoothing():
    return table.getNumber('Speed Sensitivity', RobotMap.defaults.turningSensitivity)

def getTurnSmoothing():
    return table.getNumber('Turning Sensitivity', RobotMap.defaults.turningSensitivity)

def log():
    table.putNumber('Speed Input', getJoySpeed())
    table.putNumber('Rotate Input', getJoyTurn())
