# Maintaining the model

## Model and coordinate system

All dimensions are millimetres. Negative X is the launch direction, Y is up in the assembled launcher, and Z runs across the two body halves. Print placement is separate from assembly coordinates.

The seed contains eleven named, separate closed meshes. `model.py` extends the three integral pivot posts from Z=7.6 to 8.3 and the grip post from Z=6.3 to 8.3. It also restores the interrupted 2 mm underside wall. The outer cover plane is Z=8.3. Post cross-sections and receiving bores are retained.

`accepted_assembly.3mf` is the current assembled geometry regression baseline. It is independent of print orientation. The seed and baseline intentionally differ by the body edits; neither is a printable plate layout.

The slider's reinforcement and other historical changes are already baked into the seed. They can be edited through mesh Boolean operations, but this repository does not reconstruct the entire historical design parametrically. There is no hidden dependency on the original chat workspace.

## Changes

1. Edit `model.py`, its dimensions, or the relevant seed mesh intentionally. Avoid repeatedly transforming print-oriented meshes to change assembly geometry.
2. Run `src/build.py` and inspect `build/Assembly_Inspection.glb` plus the generated projects.
3. Run `src/verify_motion.py`. Check whether its declared motion domains still cover the change. Add checks for newly affected regions; do not just relax a failing clearance threshold.
4. Run `src/verify.py`. This checks exact equality with the accepted assembly. For an intentional geometry change, inspect the difference and replace `src/data/accepted_assembly.3mf` with the reviewed `build/checks/assembly_geometry.3mf`, then rerun it. This is an explicit baseline update, not evidence that the new shape works.
5. Slice the exact generated full and all individual-part projects with the intended printer/material settings. Record the Bambu Studio version, warnings, support use, and time/material estimates. The CLI can use `--slice 0 --outputdir ...`; check `result.json`, not just the process exit status.
6. Copy the accepted complete project to `print/Launcher_P1S.3mf` and every project from `build/individual/` to `print/parts/`; copy current reports to `validation/`. Keep the individual set exactly aligned with the eleven assembly bodies, without omissions or stale files. Refresh `validation/SHA256SUMS.json` with `scripts/hash_artifacts.py`. Commit model, source, exports, and evidence together.

The verification output is generated locally under `build/checks/`. Existing reports under `validation/` are snapshots of the committed revision, not live results.

## Keep these decisions unless intentionally revisited

- Slider upright on its flat front end, no 45° tilt.
- No central or exterior underside slider guide: the user reported friction and a worse launch.
- Retain the thick slider spine and lower reinforcement. The catch-side lower slope provides release clearance; making the whole underside square previously collided with the catch.
- Retain the trigger pocket and catch-return band routing.
- Keep the paper-plane exit path clear through the front anchor.
- Keep connection posts flush with the cover exterior and the small underside opening closed.
- All fasteners remain printed; no metal hardware.

## Print orientation tradeoff

The upright orientation puts layer interfaces across the slider's long arm. Ten walls and the thicker geometry are retained, but the physical strength of this orientation is not proven. Do not describe rigid collision checks as strength or friction tests.

## Dependencies

`requirements.txt` pins the packages used for this initial repository build. Python-FCL is required only by `verify_motion.py`; it uses the actual triangle meshes for distance checks. Builds use trimesh and manifold3d. Bambu Studio is a separate local application and is not bundled.
