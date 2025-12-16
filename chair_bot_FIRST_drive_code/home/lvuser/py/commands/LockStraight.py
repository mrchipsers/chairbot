from wpilib.command import Command

import OI
import subsystems
import Utils

class LockStraight(Command):
    '''
    Drives the robot straight with a speed according
    to what the joystick says.
    '''

    def __init__(self):
        super().__init__('Lock Straight')

        self.requires(subsystems.drivetrain)

    def initialize(self):
        subsystems.drivetrain.resetGyro()

    def execute(self):
        # Get the values from the joystick
        joySpeed = OI.getJoySpeed()

        # Put the values through the sigmoid function
        # to smooth them out
        speedSmoothing = OI.getSpeedSmoothing()

        sigJoySpeed = 2*Utils.sigmoid(joySpeed, a=speedSmoothing)-1

        s1Speed = 2*Utils.sigmoid(1, a=speedSmoothing)-1
        sn1Speed = 2*Utils.sigmoid(-1, a=speedSmoothing)-1

        # Make sure out speed goes from -1 to 1
        speed = Utils.remap(sigJoySpeed, sn1Speed, s1Speed, -1, 1)

        # Turn opposite to the angle
        a = subsystems.drivetrain.getAngle()%360
        turn = Utils.remap(abs(a), 0, 360, 0, 1)
        if a > 0:
            turn *= -1

        # Drive
        subsystems.drivetrain.drive(speed, turn)

    def stop(self):
        subsystems.drivetrain.stop()