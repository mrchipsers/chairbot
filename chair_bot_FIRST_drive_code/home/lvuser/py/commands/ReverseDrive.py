from wpilib.command import Command

import OI
import subsystems
import Utils

class ReverseDrive(Command):
    '''
    Drives the robot backwards along what the joystick says, but smooths out
    the input from the joystick
    '''

    def __init__(self):
        super().__init__('Reverse Drive')

        self.requires(subsystems.drivetrain)

    def execute(self):
        # Get the values from the joystick
        joySpeed = OI.getJoySpeed()
        joyTurn = OI.getJoyTurn()

        # Put the values through the sigmoid function
        # to smooth them out
        speedSmoothing = OI.getSpeedSmoothing
        turnSmoothing = OI.getTurnSmoothing()

        sigJoySpeed = 2*Utils.sigmoid(joySpeed, a=speedSmoothing)-1
        sigJoyTurn = 2*Utils.sigmoid(joyTurn, a=turnSmoothing)-1

        s1Speed = 2*Utils.sigmoid(1, a=speedSmoothing)-1
        sn1Speed = 2*Utils.sigmoid(-1, a=speedSmoothing)-1

        s1Turn = 2*Utils.sigmoid(1, a=turnSmoothing)-1
        sn1Turn = 2*Utils.sigmoid(-1, a=turnSmoothing)-1

        # Make sure out speed goes from -1 to 1
        speed = Utils.remap(sigJoySpeed, sn1Speed, s1Speed, -1, 1)
        turn = Utils.remap(sigJoyTurn, sn1Turn, s1Turn, -1, 1)

        # Drive backwards
        subsystems.drivetrain.drive(-speed, turn)

    def stop(self):
        subsystems.drivetrain.stop()