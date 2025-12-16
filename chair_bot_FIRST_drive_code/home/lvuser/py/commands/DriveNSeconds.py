from wpilib.command import TimedCommand

import subsystems

class DriveNSeconds(TimedCommand):
    '''
    Drives the robot with a `moveValue` and `turnValue` for
    `duration` seconds. It stops at the end of the `duration`
    seconds.
    '''

    def __init__(self, moveValue, turnValue, duration):
        super().__init__('Record', duration)

        self.requires(subsystems.drivetrain)
        
        self.moveValue = moveValue
        self.turnValue = turnValue

    def initialize(self):
        subsystems.drivetrain.drive(self.moveValue, self.turnValue)

    def end(self):
        subsystems.drivetrain.stop()