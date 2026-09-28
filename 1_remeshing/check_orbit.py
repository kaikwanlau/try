#!/usr/bin/env python3
"""
check_orbit.py -- fit the orbit sphere on remeshed skulls and show the result. No arguments needed.

    project/
      remeshed/              <- copy the STL(s) from MATLAB here (name them <specimen>_p<para>.stl, e.g. T. cantansA_p60.stl)
      fit_sphere_logged.py
      check_orbit.py         <- run this
      results/               <- created automatically

    python check_orbit.py            fits every STL in remeshed/ that has not been fitted yet, opens the PNG(s)
    python check_orbit.py --all      re-fits everything in remeshed/
    python check_orbit.py --no-show  don't open the PNGs

Outputs (accumulating):
    results/accepted.xlsx      every accepted fit (all parameters tried)
    results/attempts.csv       every seed attempt
    results/failed.txt         every failed fit
    results/final.xlsx         one row per specimen (highest-numbered/latest parameter file present is NOT chosen
                               automatically - the row for each file is kept, so delete superseded files from remeshed/
                               or mark them in the 'keep' column when you are done)
    results/renders/<name>.png 3 views + 2 sections through the sphere centre
"""
import argparse, glob, os, platform, subprocess, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--folder', default=os.path.join(HERE, 'remeshed'))
ap.add_argument('--results', default=os.path.join(HERE, 'results'))
ap.add_argument('--all', action='store_true', help='re-fit every file, not only new ones')
ap.add_argument('--no-show', action='store_true')
ap.add_argument('--rule', default='relative'); ap.add_argument('--target', default='400'); ap.add_argument('--ball', default='2.0')
ap.add_argument('--view', default='png', choices=['png', 'window', 'both'], help='png: save+open picture; window: interactive pyvista window')
a = ap.parse_args()

fit_script = os.path.join(HERE, 'fit_sphere_logged.py')
render_dir = os.path.join(a.results, 'renders'); os.makedirs(render_dir, exist_ok=True)
prefix = os.path.join(a.results, '')          # results/accepted.xlsx etc.
P = lambda ext: os.path.join(a.results, ext)

files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(a.folder, '*.stl')))
if not files: sys.exit(f'no .stl files in {a.folder}')
done = set()
if not a.all:
    if os.path.exists(P('accepted.xlsx')): done |= set(pd.read_excel(P('accepted.xlsx')).filename)
    if os.path.exists(P('failed.txt')): done |= {l.split('\t')[0] for l in open(P('failed.txt')).read().splitlines() if l.strip()}
todo = [f for f in files if f not in done]
if not todo: sys.exit('nothing new to fit (use --all to re-fit everything)')

run = os.path.join(a.results, '_run')
fit_cmd = [sys.executable, fit_script, a.folder, run, '--rule', a.rule, '--target', a.target, '--ball', a.ball, '--render', render_dir, '--files', *todo]
if a.view in ('window', 'both'): fit_cmd.append('--interactive')
if a.view == 'window': a.no_show = True
r = subprocess.run(fit_cmd)
if r.returncode != 0: sys.exit('fitting failed')

# merge this run into the accumulated files (rows for re-fitted files are replaced)
for ext in ('accepted.xlsx', 'attempts.csv'):
    rd = pd.read_excel if ext.endswith('xlsx') else pd.read_csv
    new = rd(run + '_' + ext) if os.path.exists(run + '_' + ext) else pd.DataFrame()
    old = rd(P(ext)) if os.path.exists(P(ext)) else pd.DataFrame()
    if len(old): old = old[~old.filename.isin(todo)]
    both = pd.concat([old, new], ignore_index=True)
    (both.to_excel if ext.endswith('xlsx') else both.to_csv)(P(ext), index=False)
    if os.path.exists(run + '_' + ext): os.remove(run + '_' + ext)
old = [l for l in (open(P('failed.txt')).read().splitlines() if os.path.exists(P('failed.txt')) else []) if l.split('\t')[0] not in todo]
new = [l for l in (open(run + '_failed.txt').read().splitlines() if os.path.exists(run + '_failed.txt') else []) if l.strip()]
open(P('failed.txt'), 'w').write('\n'.join(old + new) + ('\n' if old + new else ''))
if os.path.exists(run + '_failed.txt'): os.remove(run + '_failed.txt')

# final table: one row per file currently in remeshed/
acc = pd.read_excel(P('accepted.xlsx')) if os.path.exists(P('accepted.xlsx')) else pd.DataFrame()
failed = {l.split('\t')[0]: (l.split('\t')[1] if '\t' in l else '') for l in open(P('failed.txt')).read().splitlines() if l.strip()}
rows = []
for f in files:
    r_ = acc[acc.filename == f] if len(acc) else acc
    if len(r_): rows.append({**r_.iloc[0].to_dict(), 'status': 'accepted'})
    elif f in failed: rows.append({'filename': f, 'status': 'failed', 'rejected_attempts': failed[f]})
    else: rows.append({'filename': f, 'status': 'not fitted'})
fin = pd.DataFrame(rows)
cols = ['filename', 'specimen', 'para', 'status'] + [c for c in fin.columns if c not in ('filename', 'specimen', 'para', 'status')]
fin = fin[[c for c in cols if c in fin.columns]]
fin.to_excel(P('final.xlsx'), index=False)

print('\n--- this run ---')
pngs = []
for f in todo:
    row = acc[acc.filename == f] if len(acc) else acc
    if len(row):
        x = row.iloc[0]; png = os.path.join(render_dir, f[:-4] + '.png')
        verdict = 'looks fine' if x.rms_over_radius <= 0.10 else 'CHECK: high residual (points spilled or flattened orbit)'
        print(f"{f:32s} ACCEPTED  r={x.sphere_radius:.2f} mm  r/L={x.r_over_L:.3f}  inliers={int(x.n_inliers)}  RMS/r={x.rms_over_radius:.3f}  seed {int(x.seed_attempt)}   {verdict}")
    else:
        png = os.path.join(render_dir, f[:-4] + '_FAILED.png')
        print(f"{f:32s} FAILED    (see results/failed.txt for what each seed gave)")
    if os.path.exists(png): pngs.append(png); print(f"{'':32s} picture: {png}")
print(f"--- total so far: {(fin.status=='accepted').sum()} accepted, {(fin.status=='failed').sum()} failed of {len(fin)} files in remeshed/ -> results/final.xlsx ---")
if pngs and not a.no_show:
    opener = {'Darwin': ['open'], 'Windows': ['cmd', '/c', 'start', '']}.get(platform.system(), ['xdg-open'])
    for png in pngs:
        try: subprocess.Popen(opener + [png])
        except Exception: pass