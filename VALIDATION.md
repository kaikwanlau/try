# Validation of this repository refresh

Prepared 29 September 2026. Scope: the new presentation, documentation and one-skull entry point. This is not a new audit of all paper results.

| Check | Result |
| :--- | :--- |
| Original scientific Python files compared with supplied repository ZIP | Identical |
| All supplied STL meshes and three XLSX workbooks compared with the ZIP | Identical |
| Existing license | Preserved; Apache 2.0 |
| Main two workbooks compared with the live repository snapshot | Identical |
| Mesh inventory | 100 finch/relative, 42 honeycreeper, 9 cardueline-relative, 2 rodent, 4 human |
| README animation | 188 frames; full animated version used |
| Python syntax and citation YAML | Parsed successfully |
| One-skull CLI, default example | Successful fit, CSV, JSON and inspection image |
| CLI run with explicit input/output from a different working directory | Successful |
| Missing-input and protected data-output errors | Correctly rejected |
| Wrapper result compared with direct call to existing fitter | Same result for the example |
| Example dimensions and radius compared with `data/Dataset.xlsx` | Agreement within 0.00001 mm |
| Local HTML links and fragment targets | Checked; no missing targets |
| Browser method selection, OS commands and Copy feedback | Checked |
| Tutorial chapter button at 4:20 | Seeks to 260 seconds; media duration 429.1 seconds; no media error |
| JavaScript runtime errors during browser checks | None |
| 390-pixel phone layouts for the landing page and principal guides | No horizontal page overflow |
| Desktop and phone screenshots | Visually inspected |

The test environment used Python 3.12.14, NumPy 2.2.6, SciPy 1.13.1, pandas 2.3.3, trimesh 4.8.3, rtree 1.4.1, networkx 3.6 and Matplotlib 3.10.8. The existing study environment used Python 3.12; the patch version is recorded here rather than assumed identical.

For `G.DifficilisA.stl`, the orbital result was:

| Quantity | Value |
| :--- | ---: |
| Length x, mm | 27.6419734955 |
| Width y, mm | 15.4335451126 |
| Height z, mm | 15.2090973854 |
| Orbit radius, mm | 3.5631448892 |
| Orbit curvature, mm⁻¹ | 0.2806509505 |
| Inliers | 128 |
| RMS/radius, % | 3.6689474925 |

The radius differs from the released workbook by approximately 7.9 × 10⁻⁹ mm. This confirms the example path under the recorded environment, not general correctness for every specimen or taxon.

The full 100-specimen verification, MATLAB remeshing, complete figure build and native Windows/macOS execution were not rerun for this documentation update. Remote publishing remains pending GitHub access. Browser checks used local Chromium; the static guides require no external fonts or JavaScript libraries.
