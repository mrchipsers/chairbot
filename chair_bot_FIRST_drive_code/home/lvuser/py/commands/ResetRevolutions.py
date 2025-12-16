from wpilib.command import InstantCommand

import subsystems

class ResetRevolutions(InstantCommand):
    '''
    Resets the revolutions of the drive wheels
    '''

    def __init__(self):
        super().__init__('ResetRevolutions')
        self.requires(subsystems.drivetrain)

    def initialize(self):
        global subsystems

        subsystems.drivetrain.resetRevolutionCounter()