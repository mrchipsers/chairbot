from wpilib.command import Command

import OI
import subsystems
import Utils

class HoldClimb(Command):
    '''
    Holds a climb
    '''

    def __init__(self):
        super().__init__('Hold Climb')

        self.requires(subsystems.climber)

    def execute(self):
        subsystems.climber.hold()

    def stop(self):
        subsystems.drivetrain.stop()