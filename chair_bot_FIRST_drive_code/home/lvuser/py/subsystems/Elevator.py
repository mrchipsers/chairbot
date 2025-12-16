import wpilib
from wpilib.command.subsystem import Subsystem
import RobotMap

class Elevator(Subsystem):
    '''
    This is the elevator subsystem. This is the thing responsible for climbing the rope.
    '''

    def __init__(self):
        '''Instantiates the Elevator object.'''

        super().__init__('Elevator')
        self.limitSwitches = [wpilib.DigitalInput(RobotMap.elevator.pos0),
                              wpilib.DigitalInput(RobotMap.elevator.pos1),
                              wpilib.DigitalInput(RobotMap.elevator.pos2),
                              wpilib.DigitalInput(RobotMap.elevator.pos3),
                              wpilib.DigitalInput(RobotMap.elevator.pos4)]

        self.motor = wpilib.VictorSP(RobotMap.elevator.motor)
        self.lastMotorValue = 0
        self.lastStates = [0, 0, 0, 0, 0]
        self.pos = 0
        self.dir = 'stopped'

    def update(self):
        self.poll()

    def poll(self):
        newStates = [x.get() for x in self.limitSwitches]
        changed = [i for x, i in enumerate(newStates) if x]
        if changed:
            self.pos = changed[0]

    def inPosition(self):
        return self.limitSwitches[self.pos].get()

    def _set(self, pwm):
        self.motor.set(pwm)
        self.lastMotorValue = pwm

    def hold(self):
        #########################################
        #           ~~~~~~~~~~~~~~~~~~~         #
        #           ~ SUPER IMPORTANT ~         #
        #           ~~~~~~~~~~~~~~~~~~~         #
        # Don't forget that when you want the   #
        # winch to go, you need to raise the    #
        # elevator by a tad so as to not break  #
        # everything and get people mad at you  #
        #########################################
        self._set(0.2)

    def up(self):
        self._set(0.5)
        self.dir = 'up'

    def down(self):
        self._set(0.05)
        self.dir = 'down'

    def stop(self):
        self._set(0)
        self.dir = 'stopped'

    def log(self):
        wpilib.SmartDashboard.putNumber('Elevator Position', self.pos)
        wpilib.SmartDashboard.putBoolean('Elevator Locked In position', self.inPosition())
        wpilib.SmartDashboard.putString('Elevator Direction', self.dir)
        wpilib.SmartDashboard.putNumber('Elevator PWM', self.lastMotorValue)

    def saveOutput(self):
        return ''

    def playFromRecording(self, recording):
        '''
        This plays back a certain recording, but only using
        the values that are useful for the elevator
        '''
        pass