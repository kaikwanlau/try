# Repository refresh — 29 September 2026

## The idea

Use a short, visual project overview as the front door, then give readers two clear routes: **measure their own skulls** or **reproduce the study**. The one-skull example connects the story to a concrete result: a measurement table and an image the reader can inspect.

The README remains native GitHub Markdown. The complementary visual guide in `docs/index.html` supports a richer layout, playable videos, method selection, tutorial chapter shortcuts and copyable operating-system-specific commands. It works offline and is ready for optional GitHub Pages publishing.

## Included changes

- Rewritten README using the current paper title and the actual Apache 2.0 license, with concise audience-based navigation.
- The animated GIF from the repository bundle (188 frames), plus the supplied short MP4 and tutorial. The separately uploaded GIF had only one frame and was not used.
- A biologist’s guide covering installation, mesh units and orientation, one-specimen and batch workflows, exact output paths, diagnostics and troubleshooting.
- A separate reproduction guide and script reference, keeping detailed technical material out of the project introduction.
- A responsive visual guide with scientific frames taken directly from the supplied videos, plus static HTML versions of the written guides.
- `quickstart.py`, a small entry point that calls the existing headless orbital fitter. It adds CSV, image and provenance output; it does not replace the fitting algorithm.
- `CITATION.cff` and preserved source-data attribution.

The original scientific Python files, all 157 supplied meshes, the three measurement workbooks and `LICENSE` are preserved byte-for-byte from `skull-morphology-github.zip`. The requirements change is a comment clarification; the original full dependency list is unchanged. The manuscript and reviewer correspondence are not included in this public repository package.

## Corrections and clarifications

1. The live repository examined at commit `0367f93a9aa597a021a7065ba09d45fddcc481fe` used the earlier paper title and displayed an MIT badge, while its license file is Apache 2.0. The refreshed README and citation metadata agree with the license file and current preprint title.
2. Around 4:20, the supplied tutorial describes ≥40 inliers and RMS/radius ≤0.10 as an acceptance rule. The guides clarify that this is the SI Section S4 diagnostic screen, not an automatic row filter in `fit_sphere_batch.py`, and that visual anatomical inspection is still needed. The original video has been retained without alteration.
3. “Same code on other skulls” does not mean identical settings for every taxon. The human examples use different search-band and radius limits; the batch script has a Peromyscus override.
4. Reproduction starts from prepared meshes. The MATLAB remeshing dependency and several figure source panels are external. The numerical verifier compares against values encoded in the script, not the current LaTeX text.

## Applying the refresh to GitHub

This is a prepared update package. No remote commit or public deployment was made during its preparation.

Use an existing authenticated checkout of `kaikwanlau/skull-morphology`, or clone it. Create a review branch, then copy the **contents** of this package’s `skull-morphology/` folder into the repository root. Do not place that folder inside the repository as an extra level.

```bash
git switch -c docs/visual-research-guide
```

After copying, inspect the diff and open `docs/index.html`. Stage the intended files explicitly:

```bash
git add README.md CITATION.cff UPDATE_NOTES.md VALIDATION.md
git add .gitignore paths.py quickstart.py requirements.txt requirements-quickstart.txt
git add docs tools data 1_remeshing 2_fitting 3_statistics 4_two_orbits 5_figures 6_verification
git diff --cached --stat
git commit -m "Add visual project guide and one-skull quickstart"
git push -u origin docs/visual-research-guide
```

Open a pull request from that branch to `main`. Copying the package over the existing checkout does not delete legacy top-level scripts or `dataset/`; the refreshed documentation points to the numbered folders and `data/`. Keeping or retiring those old paths can be reviewed separately. Use Git/GitHub Desktop for the media files if browser uploads are inconvenient.

## Optional visual project page

After merging, use **Settings → Pages → Deploy from a branch → main → /docs → Save** to publish the visual guide. See [GitHub’s publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

No extra build step is needed: the generated HTML and `.nojekyll` file are included. Once GitHub shows a successful deployment, add its actual URL to the repository’s About section and the README. No live site URL is asserted by this package.

Edit `docs/START_HERE.md`, `docs/REPRODUCE.md` and `docs/REFERENCE.md` for future guide changes, then regenerate their HTML:

```bash
python -m pip install Markdown==3.8.2
python tools/build_docs.py
```

The landing page, CSS and JavaScript can be edited directly. Keep the original media source files so the scientific illustrations remain traceable.
