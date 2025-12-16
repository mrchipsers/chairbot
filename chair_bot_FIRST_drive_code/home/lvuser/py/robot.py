#!/usr/bin/env python3

from commands.NoAuto import NoAuto
from commands.LeftSwitchAuto import LeftSwitchAuto
# from commands.LeftSwitchAuto import CenterSwitchAuto
# from commands.RightSwitchAuto import RightSwitchAuto
import wpilib
from wpilib.command import Scheduler
from commandbased import CommandBasedRobot
import subsystems
import OI
from networktables import NetworkTables, NetworkTablesInstance

class Robot(CommandBasedRobot):
    '''
    The CommandBasedRobot base class implements almost everything you need for
    a working robot program. All you need to do is set up the subsystems and
    commands. You do not need to override the "periodic" functions, as they
    will automatically call the scheduler. You may override the "init" functions
    if you want to do anything special when the mode changes.
    '''

    def robotInit(self):
        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''

        subsystems.init()
        NetworkTables.initialize()

        table = NetworkTables.getTable("Smartdashboard")

        self.autoChooser = wpilib.SendableChooser()
        self.autoChooser.addDefault('No Auto', NoAuto())
        self.autoChooser.addObject('Left Switch Auto', LeftSwitchAuto())
        # self.autoChooser.addObject('Center Switch Auto', CenterSwitchAuto())
        # self.autoChooser.addObject('Right Switch Auto', RightSwitchAuto())
        wpilib.SmartDashboard.putData('Auto Mode', self.autoChooser)
        self.autonomousCommand = None

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''
        OI.init()

        # Initialize the camera server
        wpilib.CameraServer.launch('vision.py:main')

    def autonomousInit(self):
        '''
        You should call start on your autonomous program here. You can
        instantiate the program here if you like, or in robotInit as in this
        example. You can also use a SendableChooser to have the autonomous
        program chosen from the SmartDashboard.
        '''
        self.autonomousCommand = self.autoChooser.getSelected()
        self.autonomousCommand.start()

    def autonomousPeriodic(self):
        '''This function is called periodically during autonomous.'''
        Scheduler.getInstance().run()
        subsystems.update()

    def teleopInit(self):
        '''This function is called at the beginning of operator control.'''
        # This ensures that the autonomous stops running when
        # teleop starts running.
        if self.autonomousCommand is not None:
            print('[ROBOT] Cancelling the autonomous command...')
            self.autonomousCommand.cancel()        

    def teleopPeriodic(self):
        '''This function is called periodically during operator control.'''
        Scheduler.getInstance().run()
        self.log()
        subsystems.update()        

    def disabledInit(self):
        '''This function is called once when the robot is disabled.'''
        subsystems.stop()
        self.log()

    def disabledPeriodic(self):
        '''This function is called periodically while disabled.'''
        self.log()
        subsystems.update()        

    def log(self):
        '''Logs all the information from the subsystems and
        from the OI to the SmartDashboard.'''
        subsystems.log()
        OI.log()

if __name__ == '__main__':
    wpilib.run(Robot)
    # wpilib.run(Robot, physics_enabled=True)