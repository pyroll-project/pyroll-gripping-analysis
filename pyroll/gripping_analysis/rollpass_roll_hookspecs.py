from pyroll.core import RollPass, Roll


@RollPass.Roll.hookspec
def gripping_angle(roll_pass: RollPass, roll: Roll):
    """Angle under whom the in profile ist gripped."""

