from pyroll.gripping_condition.pillar_element import Pillar

from pyroll.core import RollPass
from pyroll.ui import Reporter

from . import rollpass_hookimpls
from . import rollpass_hookspecs
from . import rollpass_roll_hookimpls
from . import rollpass_roll_hookspecs
from . import rollpass_in_profile_hookimpls
from . import rollpass_in_profile_hookspecs

from . import reporter_impls

RollPass.plugin_manager.add_hookspecs(rollpass_hookspecs)
RollPass.Roll.plugin_manager.add_hookspecs(rollpass_roll_hookspecs)

try:
    RollPass.InProfile.plugin_manager.add_hookspecs(rollpass_in_profile_hookspecs)
except:
    ValueError

RollPass.plugin_manager.register(rollpass_hookimpls)
RollPass.Roll.plugin_manager.register(rollpass_roll_hookimpls)
RollPass.InProfile.plugin_manager.register(rollpass_in_profile_hookimpls)

Reporter.plugin_manager.register(reporter_impls)
