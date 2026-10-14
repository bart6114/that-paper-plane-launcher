# That Paper Plane Launcher

An elastic-powered, printed paper-plane launcher, developed for a **Bambu Lab P1S with a 0.4 mm nozzle**, using **PLA or PLA Matte** and elastic bands. No metal fasteners are required.

## Print files

- [Complete two-plate project](print/Launcher_P1S.3mf)
- [Slider only](print/Slider_Only_P1S.3mf)
- [Base only](print/Base_Only_P1S.3mf)

Open these in Bambu Studio, select the actual filament, and slice. They contain models and saved print settings, not printer-ready G-code.

The current revision has a reinforced slider **standing upright on its flat end, without a 45° tilt**; no underside slider guide; flush body connection posts; a closed underside opening; and the existing reinforced front anchor and printed retaining keys/pins. The slider keeps ten walls and a removable brim. The body halves lie exterior-face down.

This remains a prototype. Geometry, scoped motion clearances, and slicing have been checked digitally; printed strength, fatigue, surface friction, and complete hand clearance have not been validated. Earlier prints suffered slider breakage and guide friction. See [validation](docs/validation.md) and [print/assembly notes](docs/printing.md).

## Build and maintain

Requires Python 3.12. From a fresh clone:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/build.py
.venv/bin/python src/verify.py
.venv/bin/python src/verify_motion.py
```

Outputs go to ignored `build/`: full and replacement projects, individual STL/3MF parts, the assembled inspection GLB, and verification results.

The model is **mesh-based CSG**, not a native CAD feature tree or STEP solid. `src/data/assembly_seed.3mf` preserves all eleven parts before the latest body changes. `src/model.py` applies those changes, with dimensions in `src/data/model_parameters.json`. Existing part geometry can be edited with the helpers in `src/geometry.py`. `src/build.py` controls print placement, while `src/print_package.py` writes the Bambu projects. See [maintenance](docs/maintenance.md) before updating the accepted geometry or print files.

## Repository contents

| Path | Purpose |
| --- | --- |
| `print/` | Current checked full and replacement projects |
| `src/` | Editable model operations, build, and verification code |
| `src/data/` | Model seed, accepted geometry baseline, printer settings, package templates |
| `validation/` | Current verification and slicer reports, artifact hashes |
| `docs/` | Printing, maintenance, provenance, and limits of the checks |

Temporary renders, G-code, virtual environments, failed experiments, and superseded model packages are omitted. Individual STL exports and the assembly preview can be regenerated.

## Provenance

This model was developed from a user-supplied `Launcher.3mf`. Its original author and license were not recorded in the project. No license for that underlying design is asserted here; see [provenance](docs/provenance.md).
