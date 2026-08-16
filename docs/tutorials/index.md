# Tutorials

These notebooks demonstrate the core open_dvm workflows end-to-end, running against a small
auto-downloaded example dataset -- no manual data setup required. Outputs on this site are
re-executed automatically whenever the tutorials change (see `.github/workflows/docs-notebooks.yml`),
so they always reflect the current codebase, just not necessarily the exact commit being viewed.

```{note}
**Tutorial 1 (Preprocessing)** requires interactive ICA component selection, so it can't run
headless. Run it locally in Jupyter instead -- see
`tutorials/01_preprocessing.ipynb` in the repository. All other tutorials use already-preprocessed
example data, so they run immediately.
```

## Getting Started

- **[00 -- Visualization and Statistics](00_visualization_and_statistics)** -- Synthetic-data tour of open_dvm's plotting and statistics utilities.

## ERP Analysis

- **[02 -- ERP Analysis](02_erp_analysis)** -- Condition-specific ERPs, lateralization, and the N2pc component.

## Time-Frequency Analysis

- **[03 -- TFR Analysis](03_tfr_analysis)** -- Morlet wavelet decomposition, evoked vs. total power.
- **[04 -- TFR Advanced](04_tfr_advanced)** -- Advanced time-frequency techniques.

## Multivariate Decoding (BDM)

- **[05 -- BDM Decoding](05_bdm_decoding)** -- Within- and cross-condition decoding.
- **[06 -- BDM Advanced](06_bdm_advanced)** -- Generalization across time (GAT), time-frequency decoding, statistical testing.

## Channel Tuning Functions (CTF)

- **[07 -- CTF Analysis](07_ctf_analysis)** -- Inverted encoding models for spatial reconstruction.
- **[08 -- CTF Advanced](08_ctf_advanced)** -- Cross-task generalization and advanced CTF techniques.

## Comparing Methods

- **[09 -- BDM/CTF Comparison](09_bdm_ctf_comparison)** -- Comparing decoding and encoding approaches on the same data.

```{toctree}
:hidden:

00_visualization_and_statistics
02_erp_analysis
03_tfr_analysis
04_tfr_advanced
05_bdm_decoding
06_bdm_advanced
07_ctf_analysis
08_ctf_advanced
09_bdm_ctf_comparison
```
