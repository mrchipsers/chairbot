from wpilib.command import InstantCommand

import subsystems

class Record(InstantCommand):
    '''
    Starts/stop recording all output from all subsystems and saves
    it all to a specified file
    '''

    def __init__(self, filePath):
        super().__init__('Record')
        self.filePath = filePath
        print('Record.__init__()')

    def initialize(self):
        global subsystems
        
        # Invert the state
        subsystems.shouldRecord = not subsystems.shouldRecord

        # If it was in recording mode, save the output
        if subsystems.shouldRecord:
            print('Recording started')
            subsystems.writeOutput(self.filePath)

        else:
            print('Recording ended')