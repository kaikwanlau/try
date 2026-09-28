# Robust parametric estimation of avian cranial morphology

**From a 3D skull to interpretable geometric measurements.**

Measure skull dimensions, fit an orbital sphere, and describe the neurocranium with an ellipsoid. A Python workflow for prepared skull meshes, with data and analyses accompanying the methods paper by **Kaikwan Lau and Gary P. T. Choi**.

[Read the paper](https://arxiv.org/abs/2511.06426) · [Start with one skull](docs/START_HERE.md) · [Use your own data](docs/START_HERE.md#use-your-own-skulls) · [Reproduce the paper](docs/REPRODUCE.md)

<p align="center"><a href="docs/assets/demo.mp4"><img src="demo.gif" width="800" alt="A real skull mesh progresses through a bounding box, curvature-based orbit selection, a fitted sphere and a braincase ellipsoid." /></a></p>

<p align="center"><sub>18.8-second method overview · <a href="docs/assets/demo.mp4">MP4 version</a> · <a href="docs/assets/tutorial.mp4">7:09 guided tutorial</a></sub></p>

## Two ways in

| I want to… | Start here |
| :--- | :--- |
| Understand what the method measures | Watch the animation above, then read the three outputs below. |
| Measure skulls without learning the whole codebase | **[Biologist’s guide](docs/START_HERE.md)** — one example, then your own STL files. |
| Reproduce the study | **[Reproduction guide](docs/REPRODUCE.md)** — datasets, figures, statistics and numerical checks. |

Prefer a visual guide? After downloading the repository, open **`docs/index.html`** in your browser. It includes both videos, a step-by-step method explorer and tutorial chapters; it also works offline.

## Three geometric outputs

| Skull size | Orbit | Neurocranium |
| :--- | :--- | :--- |
| Axis-aligned length, width and height | A sphere fitted to a connected concave surface patch | An axis-aligned ellipsoid fitted to a connected convex patch |
| `length_x`, `width_y`, `height_z` | Radius `r` and curvature `1/r` | Semi-axis lengths `a`, `b`, `c` |
| Mesh coordinates need the intended anatomical orientation | A numerical fit still needs anatomical inspection | Semi-axes describe the fitted geometry, not direct brain measurements |

The method contribution is the geometric measurement workflow. The finch data provide biological validation; the additional taxa explore transfer to other skull shapes. Preparation, orientation and suitable parameter choices remain part of the workflow.

## Start with one skull

Download and unzip this repository using **Code → Download ZIP**, or clone it. With **Python 3.12**, open a terminal in the repository folder and create a virtual environment:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\activate.bat` in Windows Command Prompt. On macOS/Linux, use `python3` for the first command if `python` is unavailable.

```bash
python -m pip install -r requirements-quickstart.txt
python quickstart.py
```

This fits the orbit of the supplied **`G.DifficilisA.stl`** specimen using the existing headless fitting code. It writes a measurement CSV, a three-view inspection image and a record of the settings and software versions to **`output/quickstart/`**. No MATLAB or interactive 3D window is needed for this example.

For the full workflow, install `requirements.txt` and follow the [biologist’s guide](docs/START_HERE.md). The orbital example does not perform the ellipsoid fit or the paper’s full analysis.

## Data and code, together

The release contains **100 finch and relative skulls**, **51 additional bird skulls**, **2 rodent skulls** and **4 human crania**. See [data sources and scope](data/README.md) before reuse.

| Folder | Purpose |
| :--- | :--- |
| [`data/`](data/) | Prepared meshes and the three released measurement workbooks |
| [`1_remeshing/`](1_remeshing/) | Raw-mesh preparation; requires external MATLAB remeshing code |
| [`2_fitting/`](2_fitting/) | Dimensions, orbital spheres and neurocranial ellipsoids |
| [`3_statistics/`](3_statistics/) | Correlations and the curvature regression model |
| [`4_two_orbits/`](4_two_orbits/) | Bilateral fits and diagnostic outputs |
| [`5_figures/`](5_figures/) | Paper figures and the overview animation |
| [`6_verification/`](6_verification/) | Refit meshes and compare against encoded manuscript values |

`paths.py` centralizes the supplied data paths. Generated results go into `output/` folders; remeshing uses its own working folders. The [script reference](docs/REFERENCE.md) lists the exact inputs and outputs.

## Before interpreting a fit

- Use prepared triangular STL meshes in **millimetres**, with **beak at −x, posterior at +x, and dorsal direction +z** for the bird workflow. The fitting scripts do not establish anatomical orientation for arbitrary inputs.
- The default orbital search band and radius limits were selected for the finch dataset. Other taxa may need different settings; the supplied human examples already use different limits.
- Inspect the selected points and fitted surface. The SI Section S4 screen of **at least 40 inliers and RMS/radius ≤ 0.10** flags fits for review; it is not an automatic acceptance filter in `fit_sphere_batch.py`, nor proof that a fit is anatomically correct.
- The regression is an empirical model within the study’s sampled size range. Do not treat it as a universal predictor across taxa.

## Cite this work

Kaikwan Lau and Gary P. T. Choi. *[Robust Parametric Estimation of Avian Cranial Morphology](https://arxiv.org/abs/2511.06426).* arXiv:2511.06426 (2025).

```bibtex
@article{lau2025robust,
  author = {Lau, Kaikwan and Choi, Gary P. T.},
  title = {Robust Parametric Estimation of Avian Cranial Morphology},
  journal = {arXiv preprint arXiv:2511.06426},
  year = {2025},
  eprint = {2511.06426},
  archivePrefix = {arXiv},
  primaryClass = {q-bio.QM}
}
```

Code license: **[Apache License 2.0](LICENSE)**. See the original data sources for their attribution and reuse terms. Publication metadata is kept as a preprint until a journal citation is available.

[Report an issue](https://github.com/kaikwanlau/skull-morphology/issues) · [Script reference](docs/REFERENCE.md) · [Update notes](UPDATE_NOTES.md)
