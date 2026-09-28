# 1_remeshing/dataset_CT/

Drop raw scan meshes here (.stl, .ply, .obj or .off). `remesh_in_pycharm.py` (or
`remesh_human_head_in_pycharm.py` for human crania) remeshes each one into `dataset_remeshed/`,
fits the orbit sphere and writes the fits and pictures to `results/`.

When a remeshed skull is final, copy it into the matching folder of `data/`, where every other
step reads it.
