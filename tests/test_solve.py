import logging
from pathlib import Path

from pyroll.basic import solve
from pyroll.ui import Reporter, Exporter
from input_imf_continuous_rolling_plant import in_profile, sequence


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.basic
    import pyroll.gripping_condition

    solve(sequence, in_profile)

    report = Reporter()
    export = Exporter()

    export_file = tmp_path / "export.csv"
    report_file = tmp_path / "report.html"

    rendered = report.render(sequence)
    exported = export.export(sequence, "csv")
    print()

    export_file.write_bytes(exported)
    report_file.write_text(rendered)
    print(report_file)
    print(export_file)

    print("\nLog:")
    print(caplog.text)
