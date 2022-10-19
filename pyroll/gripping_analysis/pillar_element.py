from dataclasses import dataclass

import numpy as np
from scipy import interpolate
from shapely.geometry import LineString, Polygon


@dataclass
class Pillar:
    """Class representing a pilar element with is used for discretization of the roll pass."""
    upper_groove_contour: LineString
    lower_groove_contour: LineString
    upper_profile_contour: LineString
    lower_profile_contour: LineString
    pillar_body: Polygon

    def __post_init__(self):
        self.center = (self.pillar_body.bounds[0] + self.pillar_body.bounds[2]) / 2
        self.pillar_discretization_points = np.linspace(self.pillar_body.bounds[0], self.pillar_body.bounds[2], num=25)
        self.line_strings_list = list((self.upper_groove_contour, self.upper_profile_contour, self.lower_groove_contour, self.lower_profile_contour))
        self.line_string_interpolations = self.interpolation_from_linestring()
        self.height_reductions_array = self.calculate_reduction_array()
        self.mean_height_reduction = np.mean(self.height_reductions_array)

    def interpolation_from_linestring(self):
        return [interpolate.interp1d(*line_string.xy) for line_string in self.line_strings_list]

    def calculate_reduction_array(self):
        equidistant_line_string_y_coordinates = [interpolations(self.pillar_discretization_points) for interpolations in self.line_string_interpolations]
        upper_reduction_array = np.abs(equidistant_line_string_y_coordinates[1] - equidistant_line_string_y_coordinates[0])
        lower_reduction_array = np.abs(equidistant_line_string_y_coordinates[3] - equidistant_line_string_y_coordinates[2])

        return upper_reduction_array + lower_reduction_array
