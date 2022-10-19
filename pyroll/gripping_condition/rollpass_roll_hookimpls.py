import numpy as np
import logging
from pyroll.core import RollPass, Roll

log = logging.getLogger(__name__)


@RollPass.Roll.hookimpl
def gripping_angle(roll_pass: RollPass, roll: Roll):
    max_reduction = roll_pass.max_height_reduction
    max_reduction_points = roll_pass.point_of_max_height_reduction

    radii_max_reduction_points = [roll_pass.roll.nominal_radius - roll_pass.roll.groove.local_depth(point) for point in max_reduction_points]
    contact_lengths_max_reduction_points = [np.sqrt(radius * reduction - reduction ** 2 / 4) for (reduction, radius) in zip(max_reduction, radii_max_reduction_points)]

    angles = [np.arcsin(contact_length / radius) for (contact_length, radius)
              in zip(contact_lengths_max_reduction_points, radii_max_reduction_points)]

    log.info(f"For roll pass {roll_pass.label} {len(angles)} gripping positions where found.")

    return angles


@RollPass.Roll.hookimpl
def gripping_evaluation(roll_pass: RollPass, roll: Roll):
    res = []
    for gripping_angle in roll_pass.roll.gripping_angle:
        if np.tan(gripping_angle) <= roll_pass.coulomb_friction_coefficient:
            res.append(True)
        else:
            res.append(False)

    if all(item is True for item in res):
        log.info(f"Profile for {roll_pass.label} passed geometric gripping condition!")
        return 'Passed'
    elif all(item is False for item in res):
        log.warning(f"Profile for {roll_pass.label} did not pass geometric gripping condition!")
        return 'Failed'
    else:
        log.warning(f"Profile for {roll_pass.label} partially passed geometric gripping condition!")
        return 'Partially'
