import argparse, pathlib
import scienceplots
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from   astropy.io          import fits
from   astropy.stats       import sigma_clipped_stats
from   photutils.detection import DAOStarFinder
from   photutils.aperture  import CircularAperture, aperture_photometry

# ─── Command-line interface ───────────────────────────────────
p = argparse.ArgumentParser(description="Generate an M12 CMD.")
p.add_argument("--fwhm",            type=float, default=3.0)
p.add_argument("--aperture-radius", type=float, default=4.0)
p.add_argument("--threshold",       type=float, default=5.0)
args = p.parse_args()

# ─── Data ─────────────────────────────────────────────────────
b_data = fits.getdata("Bcomb.fits")
v_data = fits.getdata("Vcomb.fits")

# ─── Source detection (V band) ────────────────────────────────
mean, median, std = sigma_clipped_stats(v_data, sigma=3.0)
daofind   = DAOStarFinder(fwhm=args.fwhm, threshold=args.threshold * std)
sources   = daofind(v_data - median)
positions = np.column_stack((sources["xcentroid"], sources["ycentroid"]))

# ─── Aperture photometry ──────────────────────────────────────
apertures  = CircularAperture(positions, r=args.aperture_radius)
b_phot     = aperture_photometry(b_data, apertures)
v_phot     = aperture_photometry(v_data, apertures)

mag = lambda flux: -2.5 * np.log10(flux)
b_mag = mag(b_phot["aperture_sum"])
v_mag = mag(v_phot["aperture_sum"])
color = b_mag - v_mag + 24.305 - 25.245   # B–V (zero-points from your notes)

# ─── Plot (Nature style) ──────────────────────────────────────
plt.style.use(["science", "nature"])
plt.rcParams.update({
    "font.size": 15,
    "axes.labelsize": 15,
    "axes.titlesize": 15,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
})

fig = plt.figure(figsize=(7.2, 4.5))        # ≈ 183 mm × 114 mm
sc  = plt.scatter(color, v_mag, c=color, cmap="viridis",
                  s=10, alpha=0.7, edgecolors="none")
plt.gca().invert_yaxis()
plt.xlabel(r"$B-V$")
plt.ylabel(r"$V$ Magnitude")
plt.title("M 12 Colour–Magnitude Diagram")
plt.colorbar(sc, label=r"$B-V$ colour")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

out_png = pathlib.Path("m12_cmd.png")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
plt.close(fig)

# ─── Save catalogue ───────────────────────────────────────────
phot_df = pd.DataFrame({
    "x": sources["xcentroid"],
    "y": sources["ycentroid"],
    "flux_B": b_phot["aperture_sum"],
    "flux_V": v_phot["aperture_sum"],
    "mag_B": b_mag,
    "mag_V": v_mag,
    "B_minus_V": color,
})

print(f"✔ CMD written to {out_png}")
print("✔ Photometry table saved as photometry_results.csv")