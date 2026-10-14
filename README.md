# That Paper Plane Launcher

An elastic-powered, printed paper-plane launcher for a **Bambu Lab P1S with a 0.4 mm nozzle**, using **PLA or PLA Matte** and elastic bands. All fasteners are printed.

## Print the launcher

**[Download the complete launcher](print/Launcher_P1S.3mf)** — all eleven parts arranged on two plates.

To print a single component, choose any part below. Each download is a Bambu Studio project with the same orientation and settings used in the complete launcher. A complete launcher uses one of each.

| Individual part | Function |
| --- | --- |
| [Base](print/parts/Base_P1S.3mf) | Body half with the integral connection posts |
| [Cover](print/parts/Cover_P1S.3mf) | Other body half |
| [Trigger](print/parts/Finger_Trigger_P1S.3mf) | Trigger |
| [Catch](print/parts/Retrofit_Sear_P1S.3mf) | Catch |
| [Slider](print/parts/Retrofit_Slider_P1S.3mf) | Slider |
| [Front band holder](print/parts/Front_Anchor_P1S.3mf) | Front elastic-band holder |
| [Rear key](print/parts/Rear_Key_P1S.3mf) | Rear joining key |
| [Grip key](print/parts/Grip_Key_P1S.3mf) | Grip joining key |
| [Front pin](print/parts/Front_Lock_Pin_Lower_P1S.3mf) | Front retaining pin |
| [Rear pin](print/parts/Rear_Keeper_Pin_P1S.3mf) | Rear retaining pin |
| [Grip pin](print/parts/Grip_Keeper_Pin_P1S.3mf) | Grip retaining pin |

Open the project in Bambu Studio, select your filament, and slice. The slider stands upright on its flat end; the body halves lie exterior-face down. The current model includes the reinforced slider without an underside guide, flush body connection posts, and the closed underside opening.

See [printing and assembly notes](docs/printing.md). This remains a prototype: digital geometry, scoped clearances, and slicing are checked; physical strength and reliability remain unverified. [Validation details](docs/validation.md).

## Build and maintain

Requires Python 3.12:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/build.py
.venv/bin/python src/verify.py
.venv/bin/python src/verify_motion.py
```

The build generates the complete project, all eleven individual print projects, individual STL/3MF meshes, an assembled inspection GLB, and verification results under `build/`.

The editable model uses mesh-based CSG. `src/data/assembly_seed.3mf` preserves the underlying parts; `src/model.py` and its parameters define the latest body edits. Print placement is in `src/build.py`, and printer settings are in `src/data/`. [Maintenance instructions](docs/maintenance.md).

`print/` contains the current downloadable projects, `src/` the build sources, and `validation/` the checked results and hashes. Older revisions and temporary files are excluded.

## Provenance

Developed from a user-supplied `Launcher.3mf`. Its original author and license were not recorded; no license for the inherited design is asserted here. [Provenance](docs/provenance.md).
