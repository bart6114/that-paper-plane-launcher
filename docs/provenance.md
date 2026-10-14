# Provenance and scope

Initial repository snapshot: 14 October 2026.

The design originated in a user-supplied `Launcher.3mf`, then underwent successive mesh-CSG revisions for stronger joints, band retention, automatic catch behavior, slider reinforcement, and printing. The original design's author, source URL, and license were not available in the retained project context. No new license is assigned to the inherited geometry.

The retained seed is the accepted reinforced, no-guide assembly before the flush-post/underside-wall change. The current source reconstructs that body change and the latest upright print layout. The original slicer project is not a runtime dependency: its required printer defaults were extracted to JSON, and clean 3MF package templates are included separately.

This repository intentionally contains only the maintained revision. Old output directories, personal photographs/screenshots, conversation history, environment files, local file paths, and unused intermediate models are excluded.

There is no native CAD master or fully parameterized historical reconstruction. `assembly_seed.3mf` is the preserved mesh master, `model.py` is the editable CSG layer, and `accepted_assembly.3mf` is a regression reference.
