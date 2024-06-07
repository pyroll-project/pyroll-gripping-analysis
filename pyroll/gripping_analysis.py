import sys
import scipy
import shapely
import numpy as np

from pyroll.core import RollPass, PassSequence, Unit
from pyroll.core.hooks import Hook, root_hooks

VERSION = "2.0.2"
GRIPPING_ELEMENT_COUNT = 15

RollPass.gripping_elements = Hook[np.ndarray]()
"""Array of z-coordinates of the gripping elements centers from core to side."""

RollPass.gripping_elements_heights = Hook[np.ndarray]()
"""Heights of the gripping elements."""

RollPass.bite_angles = Hook[np.ndarray]()
"""Angles of bite."""

RollPass.mean_bite_angle = Hook[float]()
"""Mean bite angle of the roll pass."""

RollPass.passed_gripping_condition = Hook[bool]()
"""Array of entry points of the gripping elements."""


@RollPass.gripping_elements
def gripping_elements(self: RollPass):
    inter_width = self.usable_cross_section.boundary.intersection(self.in_profile.cross_section.boundary).bounds[3]
    dw = inter_width / 2 / (GRIPPING_ELEMENT_COUNT - 0.5)
    return np.arange(0, inter_width / 2, dw)


@RollPass.gripping_elements_heights
def gripping_elements_heights(self: RollPass):
    element_heights = np.array(
        [
            shapely.intersection(
                self.in_profile.cross_section,
                shapely.LineString([(e, self.in_profile.cross_section.bounds[1]),
                                    (e, self.in_profile.cross_section.bounds[3])])
            ).length
            for e in self.gripping_elements
        ]
    )

    return element_heights


@RollPass.bite_angles
def bite_angles(self: RollPass):
    if not self.roll.has_set_or_cached("contact_length"):
        return None

    entry_points_sol = [
        scipy.optimize.root_scalar(lambda x: height - self.gap - 2 * self.roll.surface_interpolation(x, center),
                                   x0=-self.roll.contact_length * 0.75, x1=-self.roll.contact_length * 1.25)
        for center, height in zip(self.gripping_elements, self.gripping_elements_heights)
    ]

    entry_points = np.concatenate([entry_point.root for entry_point in entry_points_sol]).flatten()

    local_roll_radii = np.concatenate(
        [self.roll.max_radius - self.roll.surface_interpolation(0, center) for center in self.gripping_elements],
        axis=0).flatten()

    bite_angles = [-np.arcsin(entry_point / local_radius) for entry_point, local_radius in
                   zip(entry_points, local_roll_radii)]

    return bite_angles


@RollPass.mean_bite_angle
def mean_bite_angle(self: RollPass):
    return np.mean(self.bite_angles)


@RollPass.passed_gripping_condition
def passed_gripping_condition(self: RollPass):
    results = []
    for bite_angle in self.bite_angles:
        if np.tan(bite_angle) > self.coulomb_friction_coefficient:
            results.append(True)
        else:
            results.append(False)

    if all(True for res in results):
        return True
    else:
        return False


root_hooks.add(RollPass.passed_gripping_condition)
root_hooks.add(RollPass.bite_angles)
root_hooks.add(RollPass.mean_bite_angle)

try:
    from pyroll.report.pluggy import hookimpl, plugin_manager
    from pyroll.report.utils import create_sequence_plot


    @hookimpl(specname="unit_plot")
    def mean_bite_angles_plot(unit: Unit):
        if isinstance(unit, PassSequence):
            if any(isinstance(subunit, RollPass) for subunit in unit):
                fig, ax = create_sequence_plot(unit)
                ax.set_ylabel(r"Mean Bite Angle $\alpha_0$")
                ax.set_title("Mean Bite Angle")

                units = list(unit)
                if len(units) > 0:
                    x, y = np.transpose(
                        [
                            (index, np.rad2deg(unit.mean_bite_angle))
                            for index, unit in enumerate(units)
                            if isinstance(unit, RollPass)
                        ]
                    )

                ax.bar(x=x, height=y, width=0.8)

                return fig


    plugin_manager.register(sys.modules[__name__])

except ImportError:
    pass  # report not installed
