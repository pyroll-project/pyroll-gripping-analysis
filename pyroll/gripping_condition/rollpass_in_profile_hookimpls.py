from shapely.ops import unary_union
from pyroll.core import RollPass, Profile


@RollPass.InProfile.hookimpl
def intersections(roll_pass: RollPass, profile: Profile):
    upper_intersections = roll_pass.in_profile.upper_contour_line.intersection(roll_pass.upper_contour_line)
    lower_intersections = roll_pass.in_profile.lower_contour_line.intersection(roll_pass.lower_contour_line)

    return unary_union([upper_intersections, lower_intersections])
