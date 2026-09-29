# Figure inputs and availability

The fitting and statistical analyses use the prepared meshes and measurement workbooks in `data/`. The files below are separate inputs for the photograph, raw-scan illustration and comparison with earlier remeshing results.

**The original raw scan used in Fig. 1(b) is currently unavailable.** That panel cannot be regenerated from this release. The photograph and two earlier-remeshing meshes are also absent from the release; their status is listed separately below.

| Expected file | Used for | Current availability |
| :--- | :--- | :--- |
| `photo/C.pallidus.png` | Fig. 1(a), photograph of *Camarhynchus pallidus* (Wikimedia Commons, CC BY 4.0) | Not included |
| `raw_meshes/P2.InornataA.stl` | Fig. 1(b), original raw scan of *Pinaroloxias inornata* | Currently unavailable |
| `prior_remeshing/C.PallidusA.stl` | Fig. S1, earlier-remeshing comparison for *Camarhynchus pallidus* | Not included |
| `prior_remeshing/C.flaveolaA.stl` | Fig. S1, earlier-remeshing comparison for *Coereba flaveola* | Not included |

`5_figures/figure.py` leaves the affected panels as labelled blanks and continues with the available inputs. A completed figure command therefore does not mean that every panel of the paper has been reproduced.

The prepared meshes remain available for fitting, measurements and statistical analyses. They represent a later processing stage and must not be substituted for the original raw scan or the earlier-remeshing comparison meshes.

If the original figure inputs are recovered, place them at the paths above and rerun the figure script. No changes to the fitting code are needed.
