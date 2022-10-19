import math

import numpy as np
from pyroll.core import RollPass
from shapely.ops import clip_by_rect
from .pillar_element import Pillar


@RollPass.hookimpl
def first_ekelund_friction_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def second_ekelund_friction_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def third_ekelund_friction_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def ekelund_friction_coefficient(roll_pass: RollPass):
    return roll_pass.first_ekelund_friction_coefficient * roll_pass.second_ekelund_friction_coefficient * roll_pass.third_ekelund_friction_coefficient * (
            1.05 - 0.0005 * roll_pass.in_profile.temperature)


@RollPass.hookimpl
def coulomb_friction_coefficient(roll_pass: RollPass):
    return roll_pass.ekelund_friction_coefficient


@RollPass.hookimpl
def upper_left_intersection_point(roll_pass: RollPass):
    for point in roll_pass.in_profile.intersections.geoms:
        if point.x < 0 < point.y:
            return point


@RollPass.hookimpl
def upper_right_intersection_point(roll_pass: RollPass):
    for point in roll_pass.in_profile.intersections.geoms:
        if point.x > 0 and point.y > 0:
            return point


@RollPass.hookimpl
def lower_right_intersection_point(roll_pass: RollPass):
    for point in roll_pass.in_profile.intersections.geoms:
        if point.x > 0 > point.y:
            return point


@RollPass.hookimpl
def lower_left_intersection_point(roll_pass: RollPass):
    for point in roll_pass.in_profile.intersections.geoms:
        if point.x < 0 and point.y < 0:
            return point


@RollPass.hookimpl
def number_of_pillar_elements(roll_pass: RollPass):
    return 101


@RollPass.hookimpl
def pillar_width(roll_pass: RollPass):
    distance = roll_pass.upper_left_intersection_point.distance(roll_pass.upper_right_intersection_point)
    return distance / roll_pass.number_of_pillar_elements


@RollPass.hookimpl
def pillar_elements(roll_pass: RollPass):
    elements = []
    for i in range(roll_pass.number_of_pillar_elements):
        left_pillar_boundary = roll_pass.upper_left_intersection_point.x + i * roll_pass.pillar_width
        right_pillar_boundary = roll_pass.upper_left_intersection_point.x + (i + 1) * roll_pass.pillar_width

        pillar_body = clip_by_rect(roll_pass.in_profile.cross_section, left_pillar_boundary, -math.inf,
                                   right_pillar_boundary, math.inf)
        upper_groove_contour = clip_by_rect(roll_pass.upper_contour_line, left_pillar_boundary, -math.inf,
                                            right_pillar_boundary, math.inf)
        lower_groove_contour = clip_by_rect(roll_pass.lower_contour_line, left_pillar_boundary, -math.inf,
                                            right_pillar_boundary, math.inf)
        upper_profile_contour = clip_by_rect(roll_pass.in_profile.upper_contour_line, left_pillar_boundary, -math.inf,
                                             right_pillar_boundary, math.inf)
        lower_profile_contour = clip_by_rect(roll_pass.in_profile.lower_contour_line, left_pillar_boundary, -math.inf,
                                             right_pillar_boundary, math.inf)

        pillar = Pillar(pillar_body=pillar_body, upper_groove_contour=upper_groove_contour,
                        lower_groove_contour=lower_groove_contour,
                        lower_profile_contour=lower_profile_contour, upper_profile_contour=upper_profile_contour)

        elements.append(pillar)

    return elements


@RollPass.hookimpl
def max_height_reduction(roll_pass: RollPass):
    reductions = [pillar.max_height_reduction for pillar in roll_pass.pillar_elements]

    max_reduction = []
    for red in reductions:
        if red == np.max(reductions):
            max_reduction.append(red)

    return max_reduction


@RollPass.hookimpl
def point_of_max_height_reduction(roll_pass: RollPass):
    reductions = [pillar.max_height_reduction for pillar in roll_pass.pillar_elements]
    pillar_index_for_max_height_reduction = np.flatnonzero(reductions == np.max(reductions))

    if isinstance(pillar_index_for_max_height_reduction, np.ndarray):
        coordinates_for_height_reduction = [roll_pass.pillar_elements[index].center for index in
                                            pillar_index_for_max_height_reduction]
        return coordinates_for_height_reduction

    return [roll_pass.pillar_elements[pillar_index_for_max_height_reduction].center]
