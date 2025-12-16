from wpilib.command import Command

import OI
import subsystems
import Utils

class Climb(Command):
    '''
    Activates the climber subsystem
    '''

    def __init__(self):
        super().__init__('Climb')

        self.requires(subsystems.climber)

    def execute(self):
        subsystems.climber.climb()

    def stop(self):
        subsystems.drivetrain.stop() # .hold()?