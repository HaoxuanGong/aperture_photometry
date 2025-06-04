import argparse
import scienceplots
import numpy as np
import matplotlib.pyplot as plt
from   astropy.io               import fits
from   astropy.stats            import sigma_clipped_stats
from   photutils.detection      import DAOStarFinder
from   photutils.aperture       import (CircularAperture,
                                        CircularAnnulus,
                                        aperture_photometry)

# ─── Command-line interface ───────────────────────────────────
parser = argparse.ArgumentParser(description="Generate a CMD for M 12.")
parser.add_argument("--fwhm", type=float, default=3.0,
                    help="FWHM of stellar PSF in pixels "
                         "(default: 3.0)")
parser.add_argument("--aperture-radius", "-r", type=float, default=5.0,
                    help="Photometric aperture radius in pixels "
                         "(default: 5)")
parser.add_argument("--threshold", "-t", type=float, default=5.0,
                    help="Detection threshold in σ above background "
                         "(default: 5)")
args = parser.parse_args()

r_ap   = args.aperture_radius
r_in   = 1.5 * r_ap
r_out  = 2.5 * r_ap

# ─── Read data ────────────────────────────────────────────────
b_data = fits.getdata("Bcomb.fits")
v_data = fits.getdata("Vcomb.fits")

# ─── Detect sources in V band ─────────────────────────────────
mean, median, std = sigma_clipped_stats(v_data, sigma=3)
daofind = DAOStarFinder(fwhm=args.fwhm,
                        threshold=args.threshold * std)
sources  = daofind(v_data - median)
positions = list(zip(sources["xcentroid"], sources["ycentroid"]))

# ─── Build apertures/annuli ───────────────────────────────────
apertures = CircularAperture(positions, r=r_ap)
annuli    = CircularAnnulus(positions, r_in=r_in, r_out=r_out)

# ─── Photometry in both filters ───────────────────────────────
phot_b = aperture_photometry(b_data, [apertures, annuli])
phot_v = aperture_photometry(v_data, [apertures, annuli])

n_ap  = apertures.area
n_ann = annuli.area

bkg_b = phot_b["aperture_sum_1"] / n_ann
bkg_v = phot_v["aperture_sum_1"] / n_ann

flux_b = phot_b["aperture_sum_0"] - n_ap * bkg_b
flux_v = phot_v["aperture_sum_0"] - n_ap * bkg_v

# ─── Clean and convert to magnitudes ──────────────────────────
valid  = (flux_b > 0) & (flux_v > 0)
flux_b = flux_b[valid]
flux_v = flux_v[valid]

def mag(flux):   # zero-points from your previous calibration
    return -2.5 * np.log10(flux)

b_mag = mag(flux_b) + 24.305
v_mag = mag(flux_v) + 25.245
color = b_mag - v_mag   # B−V

# ─── Plot – Nature style ──────────────────────────────────────
plt.style.use(["science", "nature"])
plt.rcParams.update({
    "font.size":       15,
    "axes.labelsize":  15,
    "axes.titlesize":  15,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "legend.fontsize": 15,
    "font.family":     "sans-serif",
    "font.sans-serif": ["Arial"],
})

fig = plt.figure(figsize=(7.2, 4.5))  # ≈ 183 mm × 114 mm
sc  = plt.scatter(color, v_mag, c=color, cmap="viridis",
                  s=10, alpha=0.7, edgecolors="none")

plt.gca().invert_yaxis()
plt.xlabel(r"$B-V$")
plt.ylabel(r"$V$ Magnitude")
plt.title("M12 Colour–Magnitude Diagram")
plt.colorbar(sc, label=r"$B-V$ colour")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# ─── Save and launch browser ──────────────────────────────────
outfile = "m12_cmd_revised.png"
plt.savefig(outfile, dpi=300, bbox_inches="tight")
plt.close(fig)
