from pyroll.core import Roll, Profile, RollPass, SwedishOvalGroove
from pyroll.freiberg_flow_stress import FreibergFlowStressCoefficients

# initial profile
in_profile = Profile.round(
    radius=24e-3,
    temperature=1200 + 273.15,
    strain=0,
    material="BST 500",
    freiberg_flow_stress_coefficients=FreibergFlowStressCoefficients(
        a=4877.12 * 1e6,
        m1=-0.00273339,
        m2=0.302309,
        m3=-0.0407581,
        m4=0.000222222,
        m5=-0.000383134,
        m6=0,
        m7=-0.492672,
        m8=0.0000175044,
        m9=-0.0611783,
        baseStrain=0.1,
        baseStrainRate=0.1
    ),
    density=7.5e3,
    thermal_capacity=690,
)

# pass sequence
sequence = [
    RollPass(
        label="K 02/001 - 1",
        roll=Roll(
            groove=SwedishOvalGroove(
                r1=6e-3,
                r2=26e-3,
                ground_width=38e-3,
                usable_width=60e-3,
                depth=7.25e-3
            ),
            nominal_radius=321e-3 / 2,
        ),
        velocity=1,
        gap=13.5e-3
    )
]