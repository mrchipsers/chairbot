from pyfrc.physics import drivetrains

class PhysicsEngine:
    '''
    Simulates a 4-wheel robot
    '''

    def __init__(self, physics_controller):
        self.physics_controller = physics_controller

    def update_sim(self, hal_data, now, dt):
        front_left_motor = hal_data['CAN'][0]['value']
        front_right_motor = hal_data['CAN'][1]['value']
        rear_left_motor = hal_data['CAN'][2]['value']
        rear_right_motor = hal_data['CAN'][3]['value']

        speed, rotation = drivetrains.four_motor_drivetrain(rear_left_motor, rear_right_motor, 
                                                            front_left_motor, front_right_motor)
        self.physics_controller.drive(speed, rotation, dt)