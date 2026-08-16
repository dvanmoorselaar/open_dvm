# open_dvm

**open_dvm** is a comprehensive Python toolbox for EEG, eye-tracking, and behavioral data
analysis, built on top of [MNE-Python](https://mne.tools/). It covers the full pipeline from
raw-data preprocessing through:

- **EEG Preprocessing** -- Filtering, ICA-based artifact removal, autoreject-based trial rejection, eye-tracking-based quality control
- **Event-Related Potentials (ERP)** -- Condition-specific ERPs, lateralization, topography plots
- **Time-Frequency Representations (TFR)** -- Morlet wavelet decomposition, evoked vs. total power
- **Multivariate Decoding (BDM)** -- Within- and cross-condition decoding, generalization across time (GAT), permutation testing
- **Channel Tuning Functions (CTF)** -- Inverted encoding models for spatial reconstruction, cross-task generalization
- **Statistics & Visualization** -- Cluster-based permutation tests, FDR correction, bootstrap statistics, publication-quality plotting

## Quick Start

```python
from open_dvm.analysis import ERP
from open_dvm.support import FolderStructure

# Load preprocessed epochs + behavioral data for one subject
df, epochs = FolderStructure().load_processed_epochs(
    sj=1, fname="ses_01_main", preproc_name="main"
)

# Compute condition-specific ERPs
erp = ERP(sj=1, epochs=epochs, df=df)
erp.condition_erps(cnds=dict(dist_cnd=["absent", "present"]), f_name="distractor")
```

See the [tutorials](tutorials/index) for a complete, runnable walkthrough of this and every
other analysis module against real example data.

## Next Steps

- **[Installation](installation)** -- Get started with open_dvm
- **[Tutorials](tutorials/index)** -- Learn through interactive, output-included notebooks
- **[API Reference](api)** -- Detailed documentation of all modules

## Citation

If you use open_dvm in your research, please cite the accompanying methods paper -- see
[`CITATION.cff`](https://github.com/dvanmoorselaar/open_dvm/blob/master/CITATION.cff) in the
repository for the up-to-date reference and BibTeX/APA export via GitHub's "Cite this repository"
button.

```{toctree}
:hidden:
:maxdepth: 2

installation
tutorials/index
api
```
