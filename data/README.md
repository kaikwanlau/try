# data/

The only place the meshes are kept. The scripts find these folders through `paths.py` in the
project folder; nothing needs to be copied next to a script.

| Folder or file | Contents |
|---|---|
| `DF_and_their_relatives/` | 100 remeshed skulls of Darwin's finches and their relatives |
| `Honeycreepers_watertight/` | 42 skulls of Hawaiian honeycreepers (SI Section S4) |
| `HC_Relatives_watertight/` | 9 skulls of their cardueline relatives (SI Section S4) |
| `Peromyscus/` | 2 rodent skulls |
| `Human_cranium/` | 4 human crania |
| `Dataset.xlsx` | all measurements of the 100 finch specimens |
| `Dataset_training.xlsx` | the 50 training specimens of Eq. (8) |
| `Dataset_other_taxa.xlsx` | the per-specimen values of SI Section S4 |
| `figure_inputs/` | inputs used only by `5_figures/figure.py` |

The scripts only read from this folder; their results go into `output/` next to each script.

## Sources and scope

The bird scans were acquired and processed in the work of Tokita et al. (2017), Al-Mosleh et al. (2021) and Mosleh et al. (2023), and were remeshed for this study. The honeycreeper and cardueline collections come from the Tokita et al. dataset. See the accompanying paper for the specimen lists and preparation method.

The two rodent examples are *Peromyscus gossypinus* and *P. simulus* from the openVertebrate project. The four human examples are drawn from TotalSegmentator (s1397), the Arothron example skull, BodyParts3D and a NiiVue sample head CT. Their preparation and fitting settings are described in the paper; they are not all processed with identical bird defaults.

| Reference | Source described |
| :--- | :--- |
| Tokita et al. (2017), *Cranial shape evolution in adaptive radiations of birds: comparative morphometrics of Darwin’s finches and Hawaiian honeycreepers* | Bird cranial scans |
| Al-Mosleh et al. (2021), *Geometry and dynamics link form, function, and evolution of finch beaks* | Earlier finch processing |
| Mosleh et al. (2023), *Beak morphometry and morphogenesis across avian radiations* | Earlier avian processing |
| openVertebrate; TotalSegmentator; Arothron; BodyParts3D; NiiVue sample images | Additional mammalian examples |

Preserve the original source attributions and check the terms attached to each source dataset before redistribution. The code’s Apache 2.0 license should not be treated as a new license grant for all third-party scans. The source article and Supporting Information contain the fuller provenance references.

## Using the tables

The statistics scripts read the released workbooks in this folder. The fitting scripts write new workbooks under their output folders; those do not automatically replace the released tables. Keep your own inputs in a separate folder and retain the measurement version used in an analysis.

Folder names and specimen filenames are preserved from the supplied release, including their original spelling and capitalization. Use the paper’s specimen lists for taxonomic interpretation. The presence of a mesh in the collection does not establish that a fit is reliable.
