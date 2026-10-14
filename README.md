# That Paper Plane Launcher

I wanted a sturdier paper-plane launcher that I could print in PLA. The slider kept breaking, and an extra guide underneath added friction, so this has involved thicker parts and a few things being taken back off.

I'm using a Bambu Lab P1S with a 0.4 mm nozzle and PLA or PLA Matte. The fasteners are printed too; you only need to add elastic bands.

## Print the launcher

[Download the complete launcher](print/Launcher_P1S.3mf). It has all eleven parts arranged on two plates.

If you need a single part, grab it below. These are Bambu Studio projects with the same orientation and settings as the full launcher. You need one of each for a complete set.

| Individual part | Function |
| --- | --- |
| [Base](print/parts/Base_P1S.3mf) | Body half with the connection posts |
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

Open the project in Bambu Studio, select your filament, and slice. The slider stands upright on its flat end. The body halves print with their outside faces on the bed. The slider is reinforced and has no underside guide; the body posts sit flush with the cover, and the small opening underneath is closed.

I'm still treating this as a prototype. The geometry and clearances have been checked over the documented motion ranges, and the files have been sliced. Physical strength and reliability still need testing. See the [printing and assembly notes](docs/printing.md) and [validation details](docs/validation.md).

## Changing the model

To rebuild the files, use Python 3.12:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/build.py
.venv/bin/python src/verify.py
.venv/bin/python src/verify_motion.py
```

The build puts the full project and all eleven individual print projects in `build/`. It also exports individual STL/3MF meshes, a GLB of the assembled launcher, and the verification results.

The model uses mesh-based CSG: Python code adds and removes material from the saved meshes. The underlying parts live in `src/data/assembly_seed.3mf`, with the latest body edits in `src/model.py` and its parameters. Print placement is in `src/build.py`; printer settings are in `src/data/`. The [maintenance instructions](docs/maintenance.md) cover what to check when changing a part.

`print/` holds the current downloads, `src/` the build sources, and `validation/` the results and file hashes. Old experiments and temporary files stay out of the repository.

## Provenance

This started from a `Launcher.3mf` file. Its original author and license aren't recorded in this project, so no license has been assigned to the inherited design. See [provenance](docs/provenance.md).
