from wpilib.command import Command
import wpilib
import subsystems
from math import pi
import time

class SetDistance(Command):
    '''
    Moves the robot a certain distance
    '''

    def __init__(self, target_distance):
        super().__init__('SetDistance')

        self.requires(subsystems.drivetrain)
        self.targetDistance = -target_distance
        self.errorCounter = 0
        self.prevAdjust = 0
        self.startTime = 0
        wpilib.SmartDashboard.putBoolean('In PID Mode', False)    

    def getError(self):
        return self.targetDistance - subsystems.drivetrain.getRevolutions()*pi*15.24

    def initialize(self):
        subsystems.drivetrain.resetRevolutionCounter()
        subsystems.drivetrain.resetGyro()
        self.startTime = time.time()
        wpilib.SmartDashboard.putBoolean('In PID Mode', True)
        
    def execute(self):
        error = self.getError()

        propK = 0.4/50

        adjust = propK * error

        # Magic
        if abs(adjust - self.prevAdjust) < 0.1:
            adjust = self.prevAdjust + (0.11 if adjust > 0 else -0.11)

        if abs(adjust) <= 0.31:
            adjust = 0.31 if adjust > 0 else -0.31

        if abs(adjust) >= 0.7:
            adjust = 0.7 if adjust > 0 else -0.7

        turnAdjust = (subsystems.drivetrain.getAngle()%360) * 0.2
        if abs(turnAdjust) >= 0.5:
            turnAdjust = 0
        if abs(adjust) <= 0.3:
            turnAdjust = 0

        if abs(self.getError()) <= 5:
            self.errorCounter += 1
        else:
            self.errorCounter = 0

        # Don't take over 1.5 seconds
        # if (time.time() - self.startTime) > 2:
        #     self.shouldEndCount = 101
        #     self.stop()

        wpilib.SmartDashboard.putBoolean('In PID Mode', True)    
        wpilib.SmartDashboard.putNumber('Distance Error', error)    
        wpilib.SmartDashboard.putNumber('PID Adjust', adjust)    

        wpilib.SmartDashboard.putNumber('Turn Adjust', turnAdjust)            

        subsystems.drivetrain.drive(adjust, turnAdjust)

    def stop(self):
        subsystems.drivetrain.stop()
        wpilib.SmartDashboard.putBoolean('In PID Mode', False)        

    def isFinished(self):
        if self.errorCounter >= 3:
            self.stop()
            return True
        return False