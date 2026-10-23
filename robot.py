import wpilib
from modules.drive import Drivetrain
from modules.pcm import CannonController

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = Drivetrain()
        self.cannon = CannonController(pcm_id=0)
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        left = -self.joystick.getRawAxis(1)  
        right = self.joystick.getRawAxis(5)
        self.drive.tank_drive(left, right)

        right_trigger_value = self.joystick.getRawAxis(3)
        should_compressor_run = right_trigger_value > 0.5
        self.cannon.set_compressor_state(should_compressor_run)

        # Goes from left to right: 3 = leftmost barrel, 2 = middle barrel, 1 = rightmost barrel
        target_barrel = 0
        if self.joystick.getRawButton(1):    target_barrel = 3 
        elif self.joystick.getRawButton(2):  target_barrel = 2
        elif self.joystick.getRawButton(3):  target_barrel = 1

        self.cannon.update(current_target_barrel=target_barrel)


if __name__ == "__main__":
    wpilib.run(MyRobot)
