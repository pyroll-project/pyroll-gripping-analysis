from pyroll.core import RollPass, Profile

if not hasattr(RollPass.InProfile.plugin_manager.hook, "intersections"):
    @RollPass.InProfile.hookspec
    def intersections(roll_pass: RollPass, profile: Profile):
        """Intersection points between incoming profile and groove"""
