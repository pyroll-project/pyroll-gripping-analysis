import matplotlib.pyplot as plt

from shapely.geometry import LineString

from pyroll.core import RollPass
from pyroll.ui import Reporter
from pyroll.utils import for_units


def plot_pass_groove_contour(ax: plt.Axes, roll_pass: RollPass):
    ax.plot(*roll_pass.upper_contour_line.xy, color="k")
    ax.plot(*roll_pass.lower_contour_line.xy, color="k")


def plot_in_profile(ax: plt.Axes, roll_pass: RollPass):
    ax.fill(*roll_pass.in_profile.cross_section.exterior.xy, alpha=0.5, color="red")


def plot_points_of_max_height_reduction(ax: plt.Axes, roll_pass: RollPass):
    linestring_for_intersections = [LineString([(max_height_reduction_point, 0), (max_height_reduction_point, 1000)]) for max_height_reduction_point
                                    in roll_pass.point_of_max_height_reduction]

    gripping_points_profile = [linestring.intersection(roll_pass.in_profile.upper_contour_line) for linestring in linestring_for_intersections]
    gripping_points_groove = [linestring.intersection(roll_pass.upper_contour_line) for linestring in linestring_for_intersections]

    for point in [*gripping_points_groove, *gripping_points_profile]:
        ax.scatter(*point.xy, color="orange")


@Reporter.hookimpl
@for_units(RollPass)
def unit_plot(unit: RollPass):
    """Plot roll pass contour and its profiles"""
    fig: plt.Figure = plt.figure(constrained_layout=True, figsize=(4, 4))
    ax: plt.Axes = fig.subplots()
    ax.set_aspect("equal", "datalim")
    ax.grid(lw=0.5)
    plt.title("Gripping Analysis")
    plot_pass_groove_contour(ax, unit)
    plot_in_profile(ax, unit)
    plot_points_of_max_height_reduction(ax, unit)

    return fig


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        #gripping_angle=f"{*unit.roll.gripping_angle,:.4e}",
        #max_height_reduction=f"{*unit.max_height_reduction,:.4e}",
        #z_coordinate_of_max_height_reduction=f"{*unit.point_of_max_height_reduction,:.4e}"
    )
