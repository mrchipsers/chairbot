from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand
import wpilib
from commands.SetDistance import SetDistance
from commands.SetGyroAngle import SetGyroAngle
import subsystems

class AutoTest(CommandGroup):
    '''
    '''

    def __init__(self):
        super().__init__('Auto Test')

        self.addSequential(SetDistance(500))

        self.addSequential(WaitCommand(timeout=0.05))
        self.addSequential(SetGyroAngle(90))

        self.addSequential(WaitCommand(timeout=0.05))
        self.addSequential(SetGyroAngle(90))

        self.addSequential(WaitCommand(timeout=0.05))
        self.addSequential(SetDistance(500))