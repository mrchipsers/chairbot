from wpilib.command import Command

import subsystems

class Brake(Command):
    '''
    Brakes
    '''

    def __init__(self):
        super().__init__('Brake')

        self.requires(subsystems.drivetrain)

    def execute(self):
        subsystems.drivetrain.stop()

    def stop(self):
        subsystems.drivetrain.stop()