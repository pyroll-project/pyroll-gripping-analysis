import numpy as np
import logging
from pyroll.core import RollPass, Roll


@RollPass.Roll.hookimpl
def gripping_angle(roll_pass: RollPass, roll: Roll):
    max_reduction = roll_pass.max_height_reduction
    max_reduction_points = roll_pass.point_of_max_height_reduction
    angles = [np.arccos(
        1 - reduction / (roll_pass.roll.nominal_radius - roll_pass.roll.groove.local_depth(point))) for reduction, point in
        [*max_reduction, *max_reduction_points]]

    return angles

@RollPass.Roll.hookimpl
def gripping_evaluation(roll_pass: RollPass, roll: Roll):
    log = logging.getLogger(__name__)

    for gripping_angle in roll_pass.roll.gripping_angle:
        if np.tan(gripping_angle) <= roll_pass.coulomb_friction_coefficient:
            log.warning(f"Profile for roll-pass {roll_pass.label} passed gripping condition.")