# Changelog

All notable changes to OpenDvM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

### Added
- Multi-format raw EEG support: `eeg_preprocessing_pipeline()` gained a `raw_ext` parameter (default `'bdf'`, no behavior change for existing callers) to discover and read `.edf`, BrainVision `.vhdr`, Neuroscan `.cnt`, and EEGLAB `.set` recordings, in addition to `.bdf`.
- `annotation_event_id` parameter (`eeg_preprocessing_pipeline` and `RAW.select_events`) for formats that represent triggers as annotations rather than a stim channel (BrainVision, Neuroscan, EEGLAB) -- `select_events` now falls back to `mne.events_from_annotations` when no stim channel is found.

### Fixed
- `RAW` crashed outright on BrainVision and Neuroscan CNT files with the default `eog=None`, since those readers require an iterable rather than `None`. EEGLAB `.set` silently dropped the `eog` argument entirely rather than forwarding it. Both fixed.

## [0.1.1] - 2026-08-16

### Added
- Documentation site (`docs/`, Sphinx + MyST-NB) published to [ReadTheDocs](https://open-dvm.readthedocs.io/), including a real API reference generated from docstrings and rendered tutorial notebooks with actual output.
- `.github/workflows/docs-notebooks.yml`: automatically re-executes the tutorial notebooks and commits rendered output whenever `tutorials/`, `open_dvm/`, or the docs config change, so the published tutorials always reflect the current codebase.

### Fixed
- `open_dvm.visualization.plot` hardcoded `font.family` to `"arial"`, which isn't installed on Linux (CI runners, ReadTheDocs, likely many users) -- matplotlib fell back correctly but printed a `findfont` warning on every text render. Now uses a portable `sans-serif` family with an `Arial`/`Helvetica`/`DejaVu Sans` fallback list.

## [0.1.0] - 2026-08-15

Initial release.

### Added
- EEG preprocessing pipeline: filtering, ICA-based artifact removal, autoreject-based trial rejection, eye-tracking-based quality control.
- Event-Related Potential (ERP) analysis: condition-specific ERPs, lateralization, topography plots.
- Time-Frequency Representation (TFR) analysis: Morlet wavelet decomposition, evoked vs. total power.
- Brain Decoding Multivariate (BDM) analysis: within- and cross-condition decoding, generalization across time (GAT), permutation testing, trial-history analyses via `special_col`.
- Channel Tuning Function (CTF) analysis: inverted encoding models for spatial reconstruction, cross-task generalization, subject-specific reference-location alignment via `special_loc`.
- Eye-tracking integration: saccade detection, fixation-based trial exclusion, with clean-room EyeLink (`.asc`) and EyeTribe (`.tsv`) file readers.
- Statistical utilities: cluster-based permutation tests, FDR correction, bootstrap statistics.
- Publication-quality plotting for all four analysis modalities (`open_dvm.visualization.plot`), including condition-difference (`cnd_diff`) testing and visualization.
- Synthetic-data generators (`open_dvm.support.synthetic_data`) for demonstrating plotting/statistics independent of any real dataset.
- Auto-downloaded example dataset (`open_dvm.support.datasets`), fetched and cached from OSF, so tutorials run without any manual data setup.
- 10 tutorial notebooks (`tutorials/`) covering the full workflow from preprocessing through advanced BDM/CTF analyses.
- Full test suite (818 tests) across all analysis and visualization modules.
