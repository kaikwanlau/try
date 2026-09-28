# Reproduce the paper

Use this route to work from the released meshes and measurement workbooks. For new specimens, start with the [biologist’s guide](START_HERE.md).

## Environment and inputs

Use Python 3.12 and install `requirements.txt` in a virtual environment as described in the [installation guide](START_HERE.md#1-download-and-install). Run the commands below **from the repository root**.

The supplied data comprise 100 finch/relative meshes, 42 honeycreeper meshes, 9 cardueline-relative meshes, 2 rodent meshes and 4 human crania. The three workbooks live in `data/`. These are the files from the supplied revision bundle; this documentation refresh does not revise their measurements.

The numerical dependencies are pinned to the supplied study environment. Keep the Python and package versions with any new output. The full requirements file leaves some visualization packages with minimum versions; it is not a complete environment lockfile.

## Choose the computation

| Goal | Command | Main output |
| :--- | :--- | :--- |
| Fit finch orbital spheres | `python 2_fitting/fit_sphere.py` | `2_fitting/output/fit_sphere/measurement_sphere_fitting_ALL.xlsx` |
| Fit finch neurocranial ellipsoids | `python 2_fitting/fit_ellipsoid.py` | `2_fitting/output/fit_ellipsoid/measurement_ellipsoid_fitting_ALL.xlsx` |
| Compute dimension/orbit correlations | `python 3_statistics/correlation.py` | Console summaries and saved scatter plot |
| Compute combined parameter correlations | `python 3_statistics/correlation_combined.py` | Console tables |
| Fit the curvature regression on training data | `python 3_statistics/modelling.py` | Model summary and `3_statistics/output/modelling/modelling_results.png` |
| Inspect both orbital fits | `python 4_two_orbits/two_orbit.py` | CSV and inspection images in `4_two_orbits/output/two_orbit/` |
| Redraw selected paper figures | `python 5_figures/figure.py --only 4,9,S2` | PDFs in `5_figures/output/figure/figures/` |
| Refit and run encoded numerical checks | `python 6_verification/verify_all.py` | `6_verification/output/verify_all/` |

The interactive fitting scripts show a window for each successful specimen. Close it to continue. Statistics read the released workbooks, not the most recent fitting outputs; generating a new fit workbook does not silently replace the analysis inputs.

`modelling.py` fits and plots the training data. Its in-sample regression summary is not the held-out test evaluation. Use the verification workflow to inspect the paper’s separate training/test results.

## Numerical verification

```bash
python 6_verification/verify_all.py
```

Read the console and `report.md`. The principal outputs include:

| Output | Contents |
| :--- | :--- |
| `report.md`, `values.csv` | Encoded reported values alongside recomputed values |
| `SI_tables.html` | Tables and numerical comparisons in a browser |
| `measurements.xlsx`, `measurements.csv` | Recomputed finch measurements and diagnostics |
| `Dataset_other_taxa.xlsx` | Recomputed values for the generalization data |
| `tables/` | Reproduced table exports |
| `SI_tables.tex`, optional `SI_tables.pdf` | TeX source and a PDF when LaTeX is installed |

The verifier compares against values **written into the script**. It does not read the newest manuscript automatically. A passing report means agreement with those encoded values; changes to the manuscript must be checked against them separately.

The verifier can install missing Python dependencies automatically; run it inside the project environment. With `USE_TESTED_VERSIONS = True`, it can change installed package versions. With `QUICK_RUN = True`, it uses stored workbook values instead of refitting the meshes, so that mode is not independent mesh-to-table verification.

The workflow starts from the prepared meshes; it does not rerun the original remeshing and anatomical alignment. Some comments in the supplied verifier still refer to three rodents; this release contains two. The dataset inventory is the authority for which files are actually present.

## Figures and media

```bash
python 5_figures/figure.py
python 5_figures/figure.py --eps
python 5_figures/figure.py --refit
```

The figure script caches its measurements. Use `--refit` after changing input meshes or fitting settings. A full figure build may take substantially longer than the one-skull example.

Some source panels are not bundled: the original photograph, one raw mesh and two earlier-remeshing meshes. Until those inputs are supplied, the figure script intentionally leaves those panels as labelled blanks. See [figure inputs](../data/figure_inputs/README.md); a completed command does not guarantee every panel is populated.

To regenerate the original short animation:

```bash
python 5_figures/demo_animation.py
```

This needs PyVista and ffmpeg for the MP4 and optimized GIF. Results go to `5_figures/output/demo_animation/`. Copy the regenerated GIF to the repository root only after checking it.

## Interpretation and scope

The geometric extraction and the statistical prediction are distinct steps. Retain the study’s preparation assumptions, mesh units, orientation and version information when comparing measurements. The empirical curvature model is bounded by its training domain; fit transfer to another taxon does not establish prediction transfer.

[Back to overview](../README.md) · [Script reference](REFERENCE.md)
