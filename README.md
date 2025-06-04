# 🌌 Messier 12 Photometry
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Astropy 6.0.1](https://img.shields.io/badge/astropy-6.0.1-informational)
![Photutils 1.1.1](https://img.shields.io/badge/photutils-1.1.1-informational)
![MIT License](https://img.shields.io/badge/license-MIT-green)


_A small, self-contained toolkit for generating Colour Magnitude Diagrams of the globular cluster Messier 12 from both HST images and a published catalogue._

---

## 📦 Project Structure

| Script | Description |
|--------|-------------|
| `vanilla_approach.py` | Basic aperture photometry with uniform background assumption|
| `revised_approach.py` | Improved photometry using annular background subtraction |
| `catalog_cmd.py` | CMD from catalogue data (`asu (5).tsv`) with photometric error filtering |


### 📥 Input Data

| File | Description |
|------|-------------|
| `Bcomb.fits` | Co-added Hubble B-filter image of M12 |
| `Vcomb.fits` | Co-added Hubble V-filter image of M12 |
| `asu (5).tsv` | VizieR photometry catalogue for M12 (TSV format) |

### 🖼 Output Examples

| File | Description |
|------|-------------|
| `m12_cmd.png` | CMD from `vanilla_approach.py` |
| `m12_cmd_revised.png` | CMD from `revised_approach.py` |
| `m12_cmd_catalog.png` | CMD from `catalog_cmd.py` |


## 🔧 Script Parameters

Each script includes command-line options to fine-tune its behavior. These allow you to adjust detection thresholds, photometric apertures, and filtering criteria to best suit your images or catalogue data.

---

### `1 – vanilla_approach.py` *(baseline image pipeline)*

*Purpose* Perform simple aperture photometry on `Bcomb.fits` and `Vcomb.fits`, then plot a CMD.

| Option              | Default | Meaning                                                      |
|---------------------|---------|--------------------------------------------------------------|
| `--fwhm`            | `3.0`   | PSF FWHM (in pixels) for `DAOStarFinder`.                    |
| `--aperture-radius` | `4.0`   | Radius (in pixels) of the circular photometric aperture.     |
| `--threshold`       | `5.0`   | Detection threshold in σ above the local background noise.   |

> ✅ You can **tune** these parameters for better performance in faint or crowded regions.

---

### `2 – revised_approach.py` *(recommended image pipeline)*

Extends `approach.py` by using **local annular background subtraction** for more accurate sky estimation.

| Option              | Default | Meaning                                                      |
|---------------------|---------|--------------------------------------------------------------|
| `--fwhm`            | `3.0`   | PSF FWHM (pixels).                                           |
| `--aperture-radius` | `5.0`   | Radius of photometric aperture (pixels).                    |
| `--threshold`       | `5.0`   | Detection threshold in σ above the background.              |

---

### `3 – catalog_cmd.py` *(catalogue-based CMD)*

*Purpose* Load the fixed TSV catalogue (`asu (5).tsv`) and filter sources by photometric uncertainty before plotting the CMD.

| Option         | Default | Meaning                                                               |
|----------------|---------|-----------------------------------------------------------------------|
| `--max-error`  | `0.04`  | Maximum accepted uncertainty in **both** B and V magnitudes (in mag). |

> 📉 Use a **lower value** (e.g. `0.02`) for clean diagrams, or a **higher value** (e.g. `0.06`) to include more faint stars.

## 🖥️ How to Run (Command Line)

Navigate to the directory containing the scripts and required files (`Bcomb.fits`, `Vcomb.fits`, `asu (5).tsv`), then run one of the following:

```bash
python vanilla_approach.py
```
```bash
python revised_approach.py
```
```bash
python catalog_cmd.py
```
