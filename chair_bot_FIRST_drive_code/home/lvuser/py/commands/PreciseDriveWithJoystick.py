from wpilib.command import Command

import OI
import subsystems
import Utils

class PreciseDriveWithJoystick(Command):
    '''
    Drives the robot like the smooth follow joystick, but with less sensitivity
    '''
    
    def __init__(self):
        super().__init__('Precise Follow Joystick')

        self.requires(subsystems.drivetrain)
    
    def execute(self):
        # Get the values from the joystick
        joySpeed = OI.getJoySpeed()
        joyTurn = OI.getJoyTurn()

        # Put the values through the sigmoid function to smooth it out
        speedSmoothing = OI.getSpeedSmoothing() * 0.01
        turnSmoothing = OI.getTurnSmoothing() * 0.01

        sigJoySpeed = 2*Utils.sigmoid(joySpeed, a=speedSmoothing)-1
        sigJoyTurn = 2*Utils.sigmoid(joyTurn, a=turnSmoothing)-1

        s1Speed = 2*Utils.sigmoid(1, a=speedSmoothing)-1
        sn1Speed = 2*Utils.sigmoid(-1, a=speedSmoothing)-1

        s1Turn = 2*Utils.sigmoid(1, a=turnSmoothing)-1
        sn1Turn = 2*Utils.sigmoid(-1, a=turnSmoothing)-1

        # Make sure out speed goes from -1 to 1
        speed = Utils.remap(sigJoySpeed, sn1Speed, s1Speed, -0.4, 0.4)
        turn = -Utils.remap(sigJoyTurn, sn1Turn, s1Turn, -0.4, 0.4)

        # Drive
        subsystems.drivetrain.drive(speed, turn)