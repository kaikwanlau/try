# Reproduce the paper

This guide describes the commands for reproducing the analyses from the prepared meshes and measurement workbooks. For new specimens, see the [biologist’s guide](START_HERE.md).

## Environment and inputs

Use Python 3.12 and install `requirements.txt` in a virtual environment as described in the [installation guide](START_HERE.md#1-download-and-install). Run the commands below **from the repository root**.

The main dataset contains 100 skulls of Darwin’s finches and their relatives. The additional 42 honeycreeper skulls and 9 cardueline-relative skulls are used in the applicability analysis in SI Section S4. Two rodent skulls and four human crania provide exploratory examples of the method’s scope and limitations. See [data sources and scope](../data/README.md) for the fitting outcomes. The three measurement workbooks are in `data/`.

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

The workflow starts from the prepared meshes; it does not rerun the original remeshing and anatomical alignment. The original raw scan used in Fig. 1(b) is currently unavailable. Its absence does not prevent fitting the released prepared meshes or running the statistical analyses.

## Figures and media

```bash
python 5_figures/figure.py
python 5_figures/figure.py --eps
python 5_figures/figure.py --refit
```

The figure script caches its measurements. Use `--refit` after changing input meshes or fitting settings. A full figure build may take substantially longer than the one-skull example.

Exact regeneration of every figure panel is not supported by the current inputs. The raw scan for Fig. 1(b) is currently unavailable; the photograph for Fig. 1(a) and two earlier-remeshing meshes for Fig. S1 are also not included. The figure script leaves affected panels as labelled blanks and continues with the available inputs. See [figure inputs and availability](../data/figure_inputs/README.md).

Use the released prepared meshes for the analysis workflow. Substituting those meshes into the missing raw-scan or earlier-remeshing panels would misrepresent the processing stages being compared.

To regenerate the original short animation:

```bash
python 5_figures/demo_animation.py
```

This needs PyVista and ffmpeg for the MP4 and optimized GIF. Results go to `5_figures/output/demo_animation/`. Copy the regenerated GIF to the repository root only after checking it.

## Interpretation and scope

The geometric extraction and the statistical prediction are distinct steps. Retain the study’s preparation assumptions, mesh units, orientation and version information when comparing measurements. The empirical curvature model is bounded by its training domain; fit transfer to another taxon does not establish prediction transfer.

[Back to overview](../README.md) · [Script reference](REFERENCE.md)
