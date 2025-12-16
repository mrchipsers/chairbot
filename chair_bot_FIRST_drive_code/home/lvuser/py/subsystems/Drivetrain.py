import time
import wpilib
import ctre
from wpilib.command.subsystem import Subsystem
from wpilib.drive.differentialdrive import DifferentialDrive

from commands.SmoothFollowJoystick import SmoothFollowJoystick
import RobotMap
import subsystems

class Drivetrain(Subsystem):
    '''
    This is the drivetrain subsystem
    '''

    def __init__(self):
        '''Instantiates the drivetrain object.'''

        super().__init__('Drivetrain')
        self.frontLeftMotor =  ctre.wpi_talonsrx.WPI_TalonSRX(RobotMap.drivetrain.frontLeftMotor)
        self.frontRightMotor =  ctre.wpi_talonsrx.WPI_TalonSRX(RobotMap.drivetrain.frontRightMotor)
        self.rearLeftMotor =  ctre.wpi_talonsrx.WPI_TalonSRX(RobotMap.drivetrain.rearLeftMotor)
        self.rearRightMotor =  ctre.wpi_talonsrx.WPI_TalonSRX(RobotMap.drivetrain.rearRightMotor)

        self.frontLeftMotor.setInverted(True)
        self.rearLeftMotor.setInverted(True)
        self.frontRightMotor.setInverted(True)
        self.rearRightMotor.setInverted(True)
        
        self.leftMotors = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.rightMotors = wpilib.SpeedControllerGroup(self.frontRightMotor, self.rearRightMotor)

        self.drivetrain = DifferentialDrive(self.leftMotors, self.rightMotors)

        self.lastMoveValue = 0
        self.lastRotateValue = 0

        self.gyro = wpilib.ADXRS450_Gyro()
        self.setpoint = 0
        self.angleAcc = 0
        self.anglePreviousTime = time.time()

        self.rangeFinder = wpilib.AnalogInput(0)

        self.didResetRevos = True
        self.startTime = 0
        self.revoVelos = []

        self.gyro.calibrate()

    def drive(self, moveValue, rotateValue):
        '''Arcade drive'''

        # Limit the speed of the robot if it's rekting our battery
        if (wpilib.RobotController.getBatteryVoltage()) < 7:
            if abs(moveValue) > 0:
                moveValue = 0 if moveValue > 0 else -0
            if abs(rotateValue) > 0:
                rotateValue = 0 if rotateValue > 0 else -0

        self.drivetrain.arcadeDrive(moveValue, rotateValue)
        self.lastMoveValue = moveValue
        self.lastRotateValue = rotateValue
        
    def setSetpoint(self, setpoint):
        self.setpoint = setpoint

    def getError(self):
        return self.getAngle() - self.setpoint

    def stop(self):
        self.drive(0, 0)

    def initDefaultCommand(self):
        self.setDefaultCommand(SmoothFollowJoystick())

    def getSpeed(self):
        return self.lastMoveValue

    def getRotate(self):
        return self.lastRotateValue

    def getAngle(self):
        return self.angleAcc
        # return self.gyro.getAngle()

    def resetGyro(self):
        self.anglePreviousTime = time.time()
        self.angleAcc = 0
        self.gyro.reset()

    def getRotationRate(self):
        return self.gyro.getRate()

    def getRangeFinderDistance(self):
        # return self.rangeFinder.getVoltage()
        voltage = self.rangeFinder.getAverageVoltage()
        voltage -= 0.28
        distance = 100 * 1.3168135 * voltage # Refer to https://www.maxbotix.com/documents/XL-MaxSonar-EZ_Datasheet.pdf
        return distance

    def _getRevPerSec(self):
        return self.rearLeftMotor.getPulseWidthVelocity()/409.6

    def updateAngleAcc(self):
        # Integrate the rotations per second
        dt = time.time() - self.anglePreviousTime

        y = self.gyro.getRate()
        # Ignore rates less than 0.5
        if abs(y) < 0.5:
            y = 0

        self.angleAcc += y*dt
        self.anglePreviousTime = time.time()

    def updateRevolutionCounter(self):
        if self.didResetRevos:
            self.didResetRevos = False
            self.startTime = time.time()
            self.revoVelos = [(0, self._getRevPerSec())]
            return
        
        self.revoVelos.append((time.time() - self.startTime, self._getRevPerSec()))

    def resetRevolutionCounter(self):
        self.didResetRevos = True

    def getRevolutions(self):
        # Integrate the revoVelos list
        # The first index of the revoVelos list is a time
        # The second index is the revs per sec
        # Integrate to get total revolutions over a certain period
        integral = 0
        for i in range(len(self.revoVelos) - 1):
            dt = self.revoVelos[i+1][0] - self.revoVelos[i][0]
            y = self.revoVelos[i][1]
            integral += dt*y
        return integral

    def update(self):
        self.updateRevolutionCounter()
        self.updateAngleAcc()

    def log(self):
        wpilib.SmartDashboard.putNumber('Speed Output', self.getSpeed())
        wpilib.SmartDashboard.putNumber('Rotate Output', self.getRotate())
        wpilib.SmartDashboard.putNumber('Absolute Angle', self.getAngle())
        wpilib.SmartDashboard.putNumber('Angle', self.getAngle() % 360)
        wpilib.SmartDashboard.putNumber('Gyro Error', self.getError())
        wpilib.SmartDashboard.putNumber('Gyro Rotation Rate', self.gyro.getRate())
        wpilib.SmartDashboard.putNumber('Gyro Setpoint', self.setpoint)
        wpilib.SmartDashboard.putNumber('Ranger Finder Distance', self.getRangeFinderDistance())
        wpilib.SmartDashboard.putNumber('Encoder Rev Per Sec', self._getRevPerSec())
        wpilib.SmartDashboard.putNumber('Total Revolutions', self.getRevolutions())
        wpilib.SmartDashboard.putNumber('Encoder Temp', self.rearLeftMotor.getTemperature())

    def saveOutput(self):
        return 'move: {0}\nturn: {1}\nangle: {2}\n'.format(self.getSpeed(), self.getRotate(), self.getAngle())

    def playFromRecording(self, recording):
        '''
        This plays back a certain recording, but only using
        the values that are useful for the drivetrain
        '''
        
        lines = recording.split('\n')

        for l in lines:
            if l.startswith('move'):
                moveValue = float(l.rstrip()[len('move: '):])
            elif l.startswith('turn'):
                turnValue = float(l.rstrip()[len('turn: '):])
            elif l.startswith('angle'):
                # TODO: Implement turning from recording
                print('TODO: Implement turning from recording')

        self.drive(moveValue, turnValue)