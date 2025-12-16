from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand
import wpilib

class NoAuto(CommandGroup):
    '''
    Does nothing
    '''

    def __init__(self):
        super().__init__('No Auto')

        self.addSequential(WaitCommand(timeout=15))            