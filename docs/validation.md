# Validation snapshot

Evidence level: **E1 CAD verified, with scoped motion and slicer checks**. This is not a physically validated mechanism.

## Passed

- Reproducible build from the files in this repository; no dependency on the original workspace.
- Eleven connected, closed, positive-volume assembly meshes. Per-part STL/3MF exports reopen successfully, without degenerate or duplicate faces.
- Exact geometry equality with the accepted assembly baseline. Print placement changes do not change the actual model geometry.
- P1S bed bounds and at least 8 mm XY bounding-box separation between objects.
- All four integral post ends meet Z=8.3, matching the cover exterior. Three extend 0.7 mm and one extends 2 mm.
- The former 15 mm underside opening is closed by a 2 mm wall. Added material is confined to the intended features within recorded mesh round-trip tolerance.
- Slider travel X=-101 to 105 mm against eight fixed parts, sampled at no more than 0.1 mm: minimum gap about 0.212 mm. A 0.05 mm half-step bound and assumed 0.10 mm combined surface error leave about 0.062 mm margin.
- Released catch at -5.8° with axial play of 0/±0.25 mm and opposing slider offsets of ±0.3 mm: positive bounded clearance and no housing penetration.
- Trigger -20 to 60° and catch -15 to 10° against new body material, sampled at 0.1°. Minimum gaps about 3.858 and 3.358 mm; positive margins after half-step radius bounds and 0.10 mm assumed surface error.
- Exact final full project sliced successfully with Bambu Studio 02.08.02.61, P1S 0.4 mm, 0.20 mm layers. No slicer warnings. Both body halves require no support in the saved layout.

All eleven individual print projects retain the component geometry and orientation from the full project, centered on separate plates. Each exact downloadable project was sliced successfully without warnings. The full project is unchanged from its checked slice. Individual slice results are recorded in `validation/slice-individual.json`.

## Not established

- Actual PLA/PLA Matte strength, layer adhesion, fatigue, friction, or wear.
- Physical fit, flushness, automatic catch reliability, or release performance of this complete revision.
- Full hand/grip-envelope clearance.
- A new full-assembly dynamics run for the latest shell/print-orientation edits. Earlier rigid-body simulations are not presented as current physical proof.
- A measured manufacturing tolerance distribution: 0.10 mm combined surface error is an assumption.

The upright slider puts layers across the long arm. It follows the requested print orientation; reinforcement and ten walls do not establish a quantified strength guarantee.

`motion.json`, `geometry.json`, and `layout.json` contain detailed results. Local reruns write to `build/checks/`; refresh the committed reports only after reviewing them. `SHA256SUMS.json` identifies the maintained files.
