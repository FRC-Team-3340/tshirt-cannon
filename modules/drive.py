import phoenix5
from wpilib import SmartDashboard

def _deadband(value: float, threshold: float = 0.1) -> float: 
    return value if abs(value) > threshold else 0.0


def _scale(scale: float, value: float) -> float:
    return scale * value


class Drivetrain:
    def __init__(self):
        self._right1 = phoenix5.WPI_TalonSRX(1)
        self._right2 = phoenix5.WPI_TalonSRX(4)
        self._left1  = phoenix5.WPI_TalonSRX(2)
        self._left2  = phoenix5.WPI_TalonSRX(3)

    def tank_drive(self, left_raw: float, right_raw: float) -> float:
        left  = _scale(0.35, _deadband(left_raw))
        right = _scale(0.35, _deadband(right_raw))

        

        self._set_left(left)
        self._set_right(right)

        return left, right

    def stop(self) -> None:
        self._set_left(0)
        self._set_right(0)

    # helpers

    def _set_left(self, power: float) -> None:
        self._left1.set(phoenix5.ControlMode.PercentOutput, power)
        self._left2.set(phoenix5.ControlMode.PercentOutput, power)

    def _set_right(self, power: float) -> None:
        self._right1.set(phoenix5.ControlMode.PercentOutput, power)
        self._right2.set(phoenix5.ControlMode.PercentOutput, power)