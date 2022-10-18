from pyroll.core import RollPass

if not hasattr(RollPass.plugin_manager.hook, "upper_left_intersection_point"):
    @RollPass.hookspec
    def upper_left_intersection_point(roll_pass: RollPass):
        """Upper left intersection point between incoming profile and groove"""

if not hasattr(RollPass.plugin_manager.hook, "upper_right_intersection_point"):
    @RollPass.hookspec
    def upper_right_intersection_point(roll_pass: RollPass):
        """Upper right intersection point between incoming profile and groove"""

if not hasattr(RollPass.plugin_manager.hook, "lower_right_intersection_point"):
    @RollPass.hookspec
    def lower_right_intersection_point(roll_pass: RollPass):
        """Lower right intersection point between incoming profile and groove"""

if not hasattr(RollPass.plugin_manager.hook, "lower_left_intersection_point"):
    @RollPass.hookspec
    def lower_left_intersection_point(roll_pass: RollPass):
        """Lower left intersection point between incoming profile and groove"""


@RollPass.hookspec
def coulomb_friction_coefficient(roll_pass: RollPass):
    """Friction coefficient of Coulombs friction model"""


@RollPass.hookspec
def number_of_pillar_elements(roll_pass: RollPass):
    """Number of pillar elements for disretization of the roll pass in width direction"""


@RollPass.hookspec
def pillar_elements(roll_pass: RollPass):
    """Pillar elements discretizing the roll pass in width direction"""


@RollPass.hookspec
def pillar_width(roll_pass: RollPass):
    """Width of the pillar elements"""


@RollPass.hookspec
def point_of_max_height_reduction(roll_pass: RollPass):
    """Point where the maximum height reduction occurs"""


@RollPass.hookspec
def max_height_reduction(roll_pass: RollPass):
    """Value of the maximal height reduction for a roll pass"""
