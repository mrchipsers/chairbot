from wpilib.command import Command

import OI
import subsystems
import Utils

class Drop(Command):
    '''
    Drop command
    '''

    def __init__(self):
        super().__init__('Drop')

        self.requires(subsystems.climber)

    def execute(self):
        subsystems.climber.drop()

    def stop(self):
        subsystems.drivetrain.stop()