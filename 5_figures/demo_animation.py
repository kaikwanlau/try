#!/usr/bin/env python3
"""
demo_animation.py - the short animation shown at the top of the README (demo.gif), drawn from the meshes.

One skull goes through the pipeline of the paper, step by step:
  1. the bounding box of the skull (length, width, height),
  2. the most concave surface in the middle of the skull, where the orbit is searched for,
  3. the sphere fitted to the orbit patch,
  4. the ellipsoid fitted to the braincase,
and a last scene shows the same code on other skulls (Darwin's finches, Hawaiian honeycreepers, human crania).
The fits are those of the paper: they come from the code of figure.py (same algorithm and settings as the
fitting scripts in 2_fitting/).

HOW TO RUN
  Run it from its folder, 5_figures/ (press Run in PyCharm, or `python demo_animation.py`).
  Needs pyvista (see requirements.txt) and, for the GIF and the MP4, ffmpeg
  (macOS: `brew install ffmpeg`; without ffmpeg only the frames and a plainer GIF are written).
  Everything is written to output/demo_animation/: demo.gif (for the README), demo.mp4 (for slides)
  and frames/. To update the README, copy demo.gif into the project folder.
"""

# --- project paths: the meshes are read from data/ (see paths.py in the project folder) ---
import os
import sys
import shutil
import subprocess
from pathlib import Path

_THIS_FILE = globals().get("__file__", os.path.join(os.getcwd(), "demo_animation.py"))
HERE = Path(_THIS_FILE).resolve().parent
sys.path.insert(0, str(HERE.parents[0]))
sys.path.insert(0, str(HERE))
import paths

os.environ.setdefault("MPLBACKEND", "Agg")      # figure.py imports matplotlib; no window is needed here
import numpy as np
import trimesh
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

import figure as F      # the fitting code of the paper's figures: orbit sphere (run) and braincase ellipsoid

# =============================================================================
# SETTINGS
# =============================================================================
SKULL = "G.DifficilisA"                       # the skull that goes through the pipeline (Figs 13(a) and S2)
SKULL_NAME = ("Geospiza difficilis", "Darwin's finch")
OTHERS = [                                     # the last scene: (mesh, name, group); a human cranium by its name
    (paths.FINCHES / "G.MagnirostrisA.stl", "Geospiza magnirostris", "Darwin's finch"),
    (paths.HONEYCREEPERS / "H.wilsoniB_p60.stl", "Hemignathus wilsoni", "Hawaiian honeycreeper"),
    (paths.HONEYCREEPERS / "L. caeruleirostrisA_p60.stl", "Loxops caeruleirostris", "honeycreeper, damaged skull"),
    ("BodyParts3D", "Homo sapiens", "human cranium"),
]
WIDTH, HEIGHT = 800, 450        # size of the animation (pixels)
SUPERSAMPLE = 2                 # drawn at twice the size, then reduced: smooth edges and text
FPS = 25                        # frames per second of the MP4
GIF_FPS = 10                    # frames per second of the GIF (fewer frames, smaller file)
GIF_WIDTH = 720                 # width of demo.gif (pixels); smaller gives a smaller file
SKULL_FILL = 0.56               # fraction of the width taken by the skull seen from the side
VIEW_ANGLE = 20.0               # camera opening (degrees); small, so that the perspective stays mild

# scenes: (name, duration in seconds)
SCENES = [("skull", 2.0), ("box", 2.6), ("concave", 3.0), ("sphere", 3.4), ("ellipsoid", 3.4),
          ("others", 3.6), ("loop", 0.8)]

BONE = np.array([225, 222, 214]) / 255.0       # skull colour
CONCAVE = np.array([40, 110, 200]) / 255.0     # concave surface (mean curvature < 0)
DIMMED = np.array([240, 239, 236]) / 255.0     # outside the search band
BOX_RED = "#e3120b"                            # bounding box, as in Fig 1
SPHERE_BLUE = "#1d3fd6"                        # fitted sphere and ellipsoid wireframes, as in Figs 1 and 4
INLIER_RED = "#dc143c"                         # orbit patch (crimson, as in the fitting scripts)
SEED_GREEN = "#32cd32"                         # seed vertex
AXIS_COLOURS = ("#e3120b", "#1a9641", "#1d3fd6")
TEXT_DARK, TEXT_GREY, ACCENT = (34, 34, 34), (110, 110, 110), (29, 63, 214)

OUT = paths.output_dir(_THIS_FILE)             # output/demo_animation/ next to this file
FRAMES = OUT / "frames"


# =============================================================================
# SMALL HELPERS
# =============================================================================
def ease(t):
    """Smooth 0 -> 1 (cosine ease-in-out); t outside [0, 1] is clipped."""
    t = float(np.clip(t, 0.0, 1.0))
    return 0.5 - 0.5 * np.cos(np.pi * t)


def ramp(t, start, length):
    """0 before `start`, 1 after `start + length`, eased in between (times in seconds)."""
    return ease((t - start) / length) if length > 0 else float(t >= start)


def font(size, italic=False, bold=False):
    """A sans-serif font available on this computer (Arial, Helvetica, Liberation Sans or DejaVu Sans)."""
    prop = font_manager.FontProperties(family=["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
                                       style="italic" if italic else "normal", weight="bold" if bold else "normal")
    return ImageFont.truetype(font_manager.findfont(prop), size)


def pv_mesh(mesh):
    faces = np.hstack([np.full((len(mesh.faces), 1), 3), mesh.faces]).ravel()
    return pv.PolyData(np.asarray(mesh.vertices, float), faces)


def wire_sphere(n=30):
    """Unit sphere with n lines each way, as drawn by the fitting scripts (pyvista.Sphere, 30 x 30)."""
    return pv.Sphere(radius=1.0, theta_resolution=n, phi_resolution=n).extract_all_edges()


def camera_on(plotter, focal, direction, distance, up=(0.0, 0.0, 1.0)):
    d = np.asarray(direction, float); d /= np.linalg.norm(d)
    plotter.camera.focal_point = tuple(focal)
    plotter.camera.position = tuple(np.asarray(focal) + distance * d)
    plotter.camera.up = up
    plotter.camera.view_angle = VIEW_ANGLE


def distance_for(width_mm, fill, aspect):
    """Camera distance at which an object `width_mm` wide takes `fill` of the width of a picture whose
    width/height ratio is `aspect`."""
    return width_mm / (fill * 2 * np.tan(np.radians(VIEW_ANGLE / 2)) * aspect)


def lateral_direction(side, azimuth_deg, elevation_deg):
    """Towards the viewer, for a lateral view of the side y < 0 (side = -1) or y > 0 (side = +1),
    turned by `azimuth_deg` about the vertical and raised by `elevation_deg`."""
    a, e = np.radians(azimuth_deg), np.radians(elevation_deg)
    return np.array([np.cos(e) * np.sin(a), side * np.cos(e) * np.cos(a), np.sin(e)])


def screenshot(plotter):
    img = plotter.screenshot(return_img=True)
    return Image.fromarray(img).convert("RGB")


# =============================================================================
# THE MEASUREMENTS (the code of the paper)
# =============================================================================
def measure_skull(path):
    m = F.load_big(str(path))                       # largest component, as in the fitting scripts
    orbit = F.run(str(path))                        # orbit sphere: seed, inliers, centre, radius
    brain = F.fit_ellipsoid(str(path))              # braincase ellipsoid (with the SI correction)
    if orbit.get("status") != "ok" or brain.get("status") != "ok":
        raise RuntimeError(f"no fit on {path}")
    V = m.vertices
    H = trimesh.curvature.discrete_mean_curvature_measure(m, V, radius=2.0)   # as in the orbit search
    lo, hi = V[:, 0].min(), V[:, 0].max()
    band = (V[:, 0] > lo + 0.30 * (hi - lo)) & (V[:, 0] < lo + 0.70 * (hi - lo))
    return dict(mesh=m, orbit=orbit, brain=brain, curvature=H, band=band, bounds=m.bounds,
                band_x=(lo + 0.30 * (hi - lo), lo + 0.70 * (hi - lo)))


# =============================================================================
# THE PIPELINE SCENES (one skull)
# =============================================================================
class PipelineScene:
    def __init__(self, S):
        self.S = S
        W, H = WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE
        p = self.p = pv.Plotter(off_screen=True, window_size=(W, H))
        p.set_background("white")        # (no depth peeling: off screen, it hides the translucent skull)
        m, o, b = S["mesh"], S["orbit"], S["brain"]
        self.skull = pv_mesh(m)
        self.skull.point_data["colours"] = np.tile((BONE * 255).astype(np.uint8), (len(m.vertices), 1))
        self.skull_actor = p.add_mesh(self.skull, scalars="colours", rgb=True, smooth_shading=True,
                                      specular=0.25, specular_power=20, ambient=0.15)
        # bounding box
        (x0, y0, z0), (x1, y1, z1) = S["bounds"]
        self.box_actor = p.add_mesh(pv.Box((x0, x1, y0, y1, z0, z1)).extract_all_edges(), color=BOX_RED,
                                    line_width=2.2 * SUPERSAMPLE)
        # the search band: two planes across the skull at 30% and 70% of its length
        planes = pv.MultiBlock()
        for xb in S["band_x"]:
            planes.append(pv.Plane(center=(xb, (y0 + y1) / 2, (z0 + z1) / 2), direction=(1, 0, 0),
                                   i_size=(z1 - z0) * 1.15, j_size=(y1 - y0) * 1.15))
        self.band_actor = p.add_mesh(planes.combine(), color="#9ecae1", opacity=0.0, show_edges=False,
                                     lighting=False)
        # orbit: seed, patch (inliers) and the fitted sphere
        self.c = np.array([o["cx"], o["cy"], o["cz"]]); self.r = o["sphere_radius"]
        self.seed_actor = p.add_mesh(pv.Sphere(radius=0.45, center=o["_seed"]), color=SEED_GREEN,
                                     smooth_shading=True)
        self.inlier_actor = p.add_points(np.asarray(o["_inliers"], float), color=INLIER_RED,
                                         point_size=5.0 * SUPERSAMPLE, render_points_as_spheres=True)
        self.unit = wire_sphere(30)
        self.sphere = self.unit.copy()
        self.sphere_actor = p.add_mesh(self.sphere, color=SPHERE_BLUE, line_width=1.1 * SUPERSAMPLE)
        # braincase ellipsoid and its semi-axes
        self.ec, self.ea = np.asarray(b["center"], float), np.asarray(b["axes"], float)
        self.ellipsoid = self.unit.copy()
        self.ellipsoid_actor = p.add_mesh(self.ellipsoid, color=SPHERE_BLUE, line_width=1.1 * SUPERSAMPLE)
        self.axis_actors = []
        for k, col in enumerate(AXIS_COLOURS):
            d = np.zeros(3); d[k] = self.ea[k]
            self.axis_actors.append(p.add_mesh(pv.Line(self.ec - d, self.ec + d), color=col,
                                               line_width=3.0 * SUPERSAMPLE))
        # the camera looks at the middle of the skull, from the distance at which the skull fills
        # SKULL_FILL of the width; the view is raised a little to leave room for the caption below
        length = np.ptp(S["bounds"][:, 0])
        self.distance = distance_for(length, SKULL_FILL, WIDTH / HEIGHT)
        self.focal = np.asarray(S["bounds"]).mean(axis=0) - np.array([0, 0, 0.07 * length])
        self.side = -1.0 if self.c[1] < 0 else 1.0

    def frame(self, t, times):
        """The picture at time t (s) of the pipeline part; `times` gives the start of each scene."""
        S, p = self.S, self.p
        tb, tc, ts, te = times["box"], times["concave"], times["sphere"], times["ellipsoid"]
        # camera: turns from the front of the skull to the side of the orbit, then stays still (a still
        # camera also keeps the GIF small: only what changes is stored)
        az = -40.0 + 55.0 * ease(t / times["box"])
        camera_on(p, self.focal, lateral_direction(self.side, az, 14.0), self.distance)
        # skull colour: bone, the concave surface in blue during the orbit search, the rest dimmed
        k_conc = ramp(t, tc + 0.1, 0.7) * (1 - ramp(t, ts + 0.9, 0.7))
        concave = np.clip(-S["curvature"] / 4.0, 0, 1)[:, None]
        coloured = BONE * (1 - concave) + CONCAVE * concave
        coloured = np.where(S["band"][:, None], coloured, DIMMED)
        rgb = BONE * (1 - k_conc) + coloured * k_conc
        self.skull.point_data["colours"] = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
        self.skull_actor.prop.opacity = 1.0 - 0.45 * ramp(t, tb, 0.5) * (1 - ramp(t, tc, 0.5)) \
            - 0.5 * ramp(t, te + 0.2, 0.6)
        self.box_actor.prop.opacity = ramp(t, tb + 0.2, 0.6) * (1 - ramp(t, tc, 0.5))
        self.box_actor.SetVisibility(self.box_actor.prop.opacity > 0.01)
        self.band_actor.prop.opacity = 0.35 * ramp(t, tc + 0.3, 0.6) * (1 - ramp(t, ts + 0.9, 0.6))
        self.band_actor.SetVisibility(self.band_actor.prop.opacity > 0.01)
        # orbit: seed, then the patch, then the sphere growing from its centre
        self.seed_actor.SetVisibility(ts - 0.4 <= t < te + 0.3)
        k_in = ramp(t, ts + 0.3, 0.4) * (1 - ramp(t, te, 0.4))
        self.inlier_actor.prop.opacity = k_in
        self.inlier_actor.SetVisibility(k_in > 0.01)
        g = ramp(t, ts + 0.9, 1.0)
        self.sphere.points = self.c + self.unit.points * max(g, 1e-3) * self.r
        self.sphere_actor.SetVisibility(g > 0.01)
        self.sphere_actor.prop.opacity = 1.0 - 0.7 * ramp(t, te, 0.5)
        # braincase ellipsoid
        ge = ramp(t, te + 0.4, 1.0)
        self.ellipsoid.points = self.ec + self.unit.points * self.ea * max(ge, 1e-3)
        self.ellipsoid_actor.SetVisibility(ge > 0.01)
        for a in self.axis_actors:
            a.SetVisibility(ge > 0.99)
        p.render()
        return screenshot(p)


# =============================================================================
# THE LAST SCENE: THE SAME FIT ON OTHER SKULLS
# =============================================================================
CAPTION_BAND = 84              # height (pixels) kept free for the caption at the bottom of the last scene


class OtherSkull:
    """One panel of the last scene: a skull and its fitted sphere, turning slowly."""
    def __init__(self, spec):
        what, self.name, self.group = spec
        W, H = WIDTH * SUPERSAMPLE // 2, (HEIGHT - CAPTION_BAND) * SUPERSAMPLE // 2
        p = self.p = pv.Plotter(off_screen=True, window_size=(W, H))
        p.set_background("white")
        if isinstance(what, str):           # a human cranium, fitted with the human settings of the paper
            h = next(h for h in F.human_results() if h["name"] == what)
            m, fit = F.mesh_of(h["path"]), h
            self.human = True
        else:
            m, fit = F.load_big(str(what)), F.run(str(what))
            self.human = False
        c, r = np.array([fit["cx"], fit["cy"], fit["cz"]]), fit["sphere_radius"]
        p.add_mesh(pv_mesh(m), color=BONE, smooth_shading=True, specular=0.25, specular_power=20, ambient=0.15)
        p.add_mesh(wire_sphere(24).scale(r, inplace=False).translate(c, inplace=False), color=SPHERE_BLUE,
                   line_width=1.0 * SUPERSAMPLE)
        p.add_mesh(pv.Sphere(radius=0.13 * r, center=fit["_seed"]), color=SEED_GREEN, smooth_shading=True)
        V = m.vertices
        self.focal = m.bounds.mean(axis=0)
        self.extent = np.ptp(V, axis=0)
        if self.human:
            self.side = 1.0 if c[1] >= V[:, 1].mean() else -1.0
        else:
            self.side = -1.0 if c[1] < 0 else 1.0
        # birds: the beak is at the low-x end; the picture is mirrored when it would point right
        self.mirror = (not self.human) and self.side > 0

    def frame(self, t):
        W, H = self.p.window_size
        turn = np.radians(-12.0 + 24.0 * t / dict(SCENES)["others"])
        if self.human:              # from the front, turned towards the fitted orbit (as in Fig 14)
            a = np.radians(35.0)
            base = np.array([-np.cos(a), self.side * np.sin(a), 0.3])
            rot = np.array([[np.cos(turn), -np.sin(turn), 0], [np.sin(turn), np.cos(turn), 0], [0, 0, 1]])
            direction = rot @ base
            distance = distance_for(self.extent[2], 0.78, 1.0)          # the height fills 78% of the panel
        else:                       # from the side of the fitted orbit
            direction = lateral_direction(self.side, np.degrees(turn), 14.0)
            distance = distance_for(self.extent[0], 0.62, W / H)        # the length fills 62% of the panel
        camera_on(self.p, self.focal, direction, distance)
        self.p.render()
        img = screenshot(self.p)
        return img.transpose(Image.FLIP_LEFT_RIGHT) if self.mirror else img


# =============================================================================
# TEXT
# =============================================================================
CAPTIONS = {
    "skull": ("Input: a 3D skull mesh", "one of the 100 skulls of Darwin's finches and their relatives"),
    "box": ("1  Skull size", "bounding box: length {L:.1f} mm, width {W:.1f} mm, height {H:.1f} mm"),
    "concave": ("2  Where is the orbit?", "the most concave surface in the middle 30–70% of the skull"),
    "sphere": ("3  Orbit", "sphere fitted to the concave patch: radius {r:.2f} mm"),
    "ellipsoid": ("4  Braincase", "ellipsoid fitted to the rear of the skull: semi-axes {a:.1f}, {b:.1f}, {c:.1f} mm"),
    "others": ("The same code on other skulls", "Darwin's finches, Hawaiian honeycreepers (also damaged ones) "
                                                 "and human crania"),
}


def draw_caption(img, title, text, alpha, species=None):
    """Caption at the bottom left (title in the accent colour, one line of text) and the species name at the
    top left; alpha fades the caption in and out."""
    s = SUPERSAMPLE
    layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(layer)
    a = int(255 * alpha)
    d.text((28 * s, img.size[1] - 66 * s), title, font=font(22 * s, bold=True), fill=ACCENT + (a,))
    d.text((28 * s, img.size[1] - 36 * s), text, font=font(17 * s), fill=TEXT_DARK + (a,))
    if species:
        d.text((28 * s, 22 * s), species[0], font=font(19 * s, italic=True), fill=TEXT_DARK + (255,))
        d.text((28 * s, 46 * s), species[1], font=font(15 * s), fill=TEXT_GREY + (255,))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def label_panel(img, name, group):
    s = SUPERSAMPLE
    d = ImageDraw.Draw(img)
    d.text((14 * s, 10 * s), name, font=font(15 * s, italic=True), fill=TEXT_DARK)
    d.text((14 * s, 30 * s), group, font=font(12 * s), fill=TEXT_GREY)
    return img


# =============================================================================
# MAIN
# =============================================================================
def main():
    pv.OFF_SCREEN = True
    path = paths.FINCHES / f"{SKULL}.stl"
    print(f"measuring {path.name} ...", flush=True)
    S = measure_skull(path)
    L, W, H = np.ptp(S["bounds"], axis=0)
    o, b = S["orbit"], S["brain"]
    values = dict(L=L, W=W, H=H, r=o["sphere_radius"], a=b["axes"][0], b=b["axes"][1], c=b["axes"][2])
    print(f"  box {L:.2f} x {W:.2f} x {H:.2f} mm, orbit radius {o['sphere_radius']:.3f} mm "
          f"({o['n_inliers']} inliers), ellipsoid {b['axes'][0]:.2f}, {b['axes'][1]:.2f}, {b['axes'][2]:.2f} mm")

    times, t0 = {}, 0.0
    for name, dur in SCENES:
        times[name] = t0; t0 += dur
    total = t0
    n_frames = int(round(total * FPS))

    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    scene = PipelineScene(S)
    print("drawing the other skulls ...", flush=True)
    others = [OtherSkull(spec) for spec in OTHERS]
    size = (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE)
    white = Image.new("RGB", size, "white")

    def dip(a, b, u):
        """From picture a to picture b through white, u from 0 to 1."""
        return Image.blend(a, white, ease(u / 0.5)) if u < 0.5 else Image.blend(white, b, ease((u - 0.5) / 0.5))

    first = last_pipeline = last_others = None
    print(f"drawing {n_frames} frames ...", flush=True)
    for i in range(n_frames):
        t = i / FPS
        name = max((n for n, _ in SCENES if times[n] <= t), key=lambda n: times[n])
        if name in ("skull", "box", "concave", "sphere", "ellipsoid"):
            img = scene.frame(t, times)
            k = dict(SCENES)[name]
            fade_in = 1.0 if name in ("skull", "ellipsoid") else ramp(t, times[name], 0.35)
            fade_out = 1.0 if name == "ellipsoid" else 1 - ramp(t, times[name] + k - 0.3, 0.3)
            title, text = CAPTIONS[name]
            img = draw_caption(img, title, text.format(**values), min(fade_in, fade_out), SKULL_NAME)
            last_pipeline = img
        else:
            tt = t - times["others"]
            grid = Image.new("RGB", size, "white")
            for k, other in enumerate(others):
                panel = label_panel(other.frame(min(tt, dict(SCENES)["others"])), other.name, other.group)
                grid.paste(panel, ((k % 2) * panel.size[0], (k // 2) * panel.size[1]))
            title, text = CAPTIONS["others"]
            grid = draw_caption(grid, title, text, 1.0)
            if name == "others":
                img = dip(last_pipeline, grid, tt / 0.6) if tt < 0.6 else grid
                last_others = grid
            else:                                         # back to the first picture, so that the GIF loops
                img = dip(last_others, first, (t - times["loop"]) / dict(SCENES)["loop"])
        if i == 0:
            first = img
        img.resize((WIDTH, HEIGHT), Image.LANCZOS).save(FRAMES / f"frame_{i:04d}.png")
        if i % 50 == 0:
            print(f"  {i}/{n_frames}", flush=True)

    write_gif_and_mp4(n_frames)


def write_gif_and_mp4(n_frames):
    """demo.gif and demo.mp4 from the frames: with ffmpeg if it is installed, otherwise a GIF from Pillow."""
    gif, mp4 = OUT / "demo.gif", OUT / "demo.mp4"
    if shutil.which("ffmpeg"):
        pattern = str(FRAMES / "frame_%04d.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", pattern,
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(mp4)],
                       check=True)
        palette = OUT / "palette.png"
        vf = f"fps={GIF_FPS},scale={GIF_WIDTH}:-1:flags=lanczos"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", pattern,
                        "-vf", vf + ",palettegen=stats_mode=diff", str(palette)], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", pattern, "-i", str(palette),
                        "-lavfi", vf + " [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                        "-loop", "0", str(gif)], check=True)
        palette.unlink()
    else:                                  # without ffmpeg: a GIF from Pillow (larger, fewer colours), no MP4
        step = FPS / GIF_FPS
        size = (GIF_WIDTH, int(round(GIF_WIDTH * HEIGHT / WIDTH)))
        imgs = [Image.open(FRAMES / f"frame_{int(round(k * step)):04d}.png").convert("RGB").resize(size, Image.LANCZOS)
                .quantize(colors=128) for k in range(int(n_frames / step))]
        imgs[0].save(gif, save_all=True, append_images=imgs[1:], duration=int(1000 / GIF_FPS), loop=0,
                     optimize=True)
        print("ffmpeg not found: demo.gif written by Pillow, and no demo.mp4 (install ffmpeg for both)")
        mp4 = None
    for f in (gif, mp4):
        if f is not None and f.exists():
            print(f"written: {f}  ({f.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
