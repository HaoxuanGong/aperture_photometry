#!/usr/bin/env python3
"""
Create an M-12 colour–magnitude diagram (CMD) from the fixed VizieR catalogue
file 'asu (5).tsv'.

Optional flag
-------------
--max-error   Maximum acceptable magnitude error in both B and V
              [default: 0.04 mag]

Outputs
-------
* m12_cmd_filtered.png  – CMD image
* Console summary of magnitude / colour ranges and pass-rate statistics
"""

# ─── Imports ──────────────────────────────────────────────────
import argparse, pathlib
import numpy   as np
import pandas  as pd
import matplotlib.pyplot as plt
import scienceplots        # noqa: F401  (needed only for style)

# ─── Command-line interface (error cut only) ──────────────────
p = argparse.ArgumentParser(description="Make an M12 CMD with an error cut.")
p.add_argument("--max-error", type=float, default=0.04,
               help="Maximum σ in B and V (default 0.04 mag)")
args = p.parse_args()

# ─── Fixed TSV file name ──────────────────────────────────────
TSV_FILE = "asu (5).tsv"

# ─── Load catalogue ───────────────────────────────────────────
df = pd.read_csv(TSV_FILE, sep='\t', comment='#',
                 usecols=lambda c: c.strip() in
                 {"Bmag", "e_Bmag", "Vmag", "e_Vmag"})

for col in ["Bmag", "e_Bmag", "Vmag", "e_Vmag"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ─── Basic stats (before filtering) ───────────────────────────
df_bv  = df.dropna(subset=["Bmag", "Vmag"])
total  = len(df_bv)
print("\nAll stars with valid B & V:")
for band in ("Vmag", "Bmag"):
    med, _min, _max = df_bv[band].median(), df_bv[band].min(), df_bv[band].max()
    print(f"  {band:<4}: median={med:.4f}, min={_min:.4f}, max={_max:.4f}")

# ─── Error filtering ─────────────────────────────────────────
df_filt = df_bv.dropna(subset=["e_Bmag", "e_Vmag"])
mask    = (df_filt["e_Bmag"] < args.max_error) & (df_filt["e_Vmag"] < args.max_error)
df_filt = df_filt[mask]

kept, perc_keep = len(df_filt), len(df_filt) / total * 100
print(f"\nStars passing error cut (≤ {args.max_error} mag): "
      f"{kept}/{total}  ({perc_keep:.2f} %)")

# ─── Colour index stats ───────────────────────────────────────
df_filt["B-V"] = df_filt["Bmag"] - df_filt["Vmag"]
med_c, min_c, max_c = df_filt["B-V"].median(), df_filt["B-V"].min(), df_filt["B-V"].max()
print(f"B−V colour: median={med_c:.4f}, min={min_c:.4f}, max={max_c:.4f}")

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

fig = plt.figure(figsize=(7.2, 4.5))
sc  = plt.scatter(df_filt["B-V"], df_filt["Vmag"],
                  c=df_filt["B-V"], cmap="viridis",
                  s=10, alpha=0.7, edgecolors="none")
plt.gca().invert_yaxis()
plt.xlabel(r"$B-V$")
plt.ylabel(r"$V$ Magnitude")
plt.title("M 12 Colour–Magnitude Diagram")
plt.colorbar(sc, label=r"$B-V$ colour")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

out_png = pathlib.Path("m12_cmd_catalog.png")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"\n✔ CMD saved to {out_png.absolute()}\n")
