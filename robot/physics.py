#
# See the notes for the other physics sample
#


from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
import math


class PhysicsEngine(object):
    '''
       Simulates a 4-wheel robot using Tank Drive joystick control
    '''


    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller

        # Change these parameters to fit your robot!

        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            50*units.lbs,                      # robot mass
            12.75,                              # drivetrain gear ratio
            2,                                  # motors per side
            18*units.inch,                      # robot wheelbase
            21.4*units.inch,     # robot width
            28.25*units.inch,     # robot length
            6*units.inch                        # wheel diameter
        )

        self.kEncoder = 360 / (6 * math.pi)

        self.l_distance = 0
        self.r_distance = 0

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        lr_motor = hal_data['pwm'][8]['value']
        rr_motor = hal_data['pwm'][6]['value']

        # Not needed because front and rear should be in sync
        # lf_motor = hal_data['pwm'][3]['value']
        # rf_motor = hal_data['pwm'][4]['value']

        x, y, angle = self.drivetrain.get_distance(rr_motor, lr_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)

        # Update encoders
        self.l_distance += self.drivetrain.l_velocity * tm_diff
        self.r_distance += self.drivetrain.r_velocity * tm_diff

        hal_data['encoder'][0]['count'] = int(self.l_distance * self.kEncoder)
        hal_data['encoder'][1]['count'] = int(self.r_distance * self.kEncoder)
