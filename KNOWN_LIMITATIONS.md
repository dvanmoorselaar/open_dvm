# Known Limitations

This document tracks known gaps, deferred features, and open methodological
questions in `open_dvm` -- things that are intentionally not fixed yet,
either because they need a design decision, are genuinely deferred to a
future release, or are inherent trade-offs rather than bugs. If you hit one
of these, this is the place to check whether it's already known before
filing an issue.

## BDM (decoding)

- **`bdm_info` reproducibility metadata is incomplete for some code paths.**
  `classify_`'s cross-condition (`self.cross`) branch only ever sets
  `bdm_info` to an empty placeholder, and `localizer_classify_` never
  populates or returns it at all. For the standard `classify()` path (no
  cross-condition, no split factor), `bdm_info` is fully populated. If you
  rely on `bdm_info` for reproducing exact train/test splits, this only
  works for that standard path today.
- **Trial-averaging subsets are not seeded/reproducible.** `average_trials`
  uses the global `random.shuffle()` to pick which trials get grouped
  together, without ever calling `random.seed(self.seed)` -- so which
  trials end up averaged together differs between runs even with a fixed
  seed, despite the class's general reproducibility guarantee.
- **Class balancing via undersampling is mandatory.** `select_max_trials`
  always equalizes trial counts across conditions/labels by discarding
  surplus trials; there's no option to decode unbalanced designs directly
  (e.g. via classifier class-weighting) instead.
- **`get_classifier_weights` only reports one class's discriminant
  direction for 3+ class decoding.** `clf.coef_` has one row per class for
  multi-class LDA/SVM; only row 0 is returned (with a warning, as of this
  release). A genuinely informative multi-class topography would return
  per-class weight maps (each row is independently interpretable as "which
  electrodes distinguish this class from the rest") -- but that requires
  extending the `weights` array's shape, `set_bdm_weights`'s Haufe
  transform, and `plot_bdm_timecourse`'s topography plotting to carry an
  extra class dimension. Not implemented; planned for a future release.
- **TFR-mode decoding + `power='induced'` + `avg_trials > 1`.** Trial
  averaging for `data_type='tfr'` now correctly averages post-decomposition
  power (fixed this release) rather than raw voltage, which is correct for
  the default `power='total'`. But `power='induced'` subtracts a
  per-condition evoked response as part of decomposition -- when combined
  with the fix, that evoked response is now estimated from the same
  per-trial data that then gets averaged, not from a description on the
  post-averaged data. If you use `power='induced'` together with
  `avg_trials > 1`, treat results with some caution; `avg_trials=1` avoids
  the ambiguity entirely.

## CTF (forward encoding)

- **Trial pre-averaging is disabled for CTF (`select_ctf_data`).**
  `CTF` inherits `BDM.average_trials`, but the call is commented out and
  `CTF.__init__` doesn't set `self.avg_trials` at all (calling it directly
  raises `AttributeError`). Open question before enabling: `BDM`'s
  pre-averaging collapses raw trials into fixed pseudo-trials once, before
  any resampling; CTF's own noise reduction instead comes from
  re-randomizing train/test block assignments across `nr_iter` iterations
  and averaging the resulting reconstructions afterward. Stacking
  BDM-style pre-averaging on top would shrink the trial pool feeding that
  resampling loop and could understate variance in the resulting CTF/slope
  estimates -- not necessarily biased, but not verified safe either.
- **`localizer_spatial_ctf` is deferred, not part of this release.**
  Beyond the `method='k-fold'` and `nr_perm>0` guards added this release,
  this function has further unresolved prerequisites: `CTF.__init__`
  doesn't actually support the list-based `epochs`/`df` this function
  requires, `basisset` isn't initialized for it, and `train_test_cross`
  hardcodes a 2-way split that ignores `nr_folds`. Don't use this function
  yet.
- **`generate_ctf_report` only renders one frequency band per figure.**
  No support for plotting multiple bands from a `freqs` list in a single
  figure.
- **CTF report/save doesn't include forward-model weights or full
  permutation results.** Only the true (unpermuted) reconstructed CTFs are
  pickled/added to the report; `W_E`/`W_T` and per-permutation results are
  discarded.
- **Broadband downsampling (`tfr_decomposition`) uses naive strided
  slicing**, not an anti-aliased resampling filter -- there's a real
  (if small) aliasing risk at low downsampling factors.
- **`forward_model_loop`'s nested time loop is not parallelized.** For GAT
  analyses with many time samples, this is a real performance bottleneck
  (each iteration runs two `linalg.lstsq` calls).

## TFR (time-frequency)

- **Laplacian/CSD is applied at analysis time, not during raw
  preprocessing** (`TFR`/`ERP`/`CTF`, wherever `laplacian=True`). This is
  standard practice and safe in practice -- MNE itself raises
  `ValueError: CSD already applied, should not be reapplied` if you pass in
  epochs that already have CSD applied, so double-application is caught
  rather than silent. Just don't pre-apply CSD yourself before passing
  epochs to a class with `laplacian=True`. Note this recomputes CSD on
  every call (no caching) -- a performance-only concern.
- **`lateralization_index` defaults to a hardcoded biosemi64 electrode-pair
  list** when `elec_pairs` isn't supplied. Already supports other montages
  via the `elec_pairs` parameter; only the convenience default is
  biosemi64-specific.

## EEG / Eye-tracking

- **No validation that eye-tracker and EEG timebases stay aligned**
  after upstream trial-removal/session-splicing steps (`align_eye_data`).
  Silent timing misalignment could currently go undetected.
- **Drift correction has no fixation-quality metric** (`EYE.set_xy`). It
  only checks for the absence of missing data/saccades in the fixation
  window, not how tightly gaze was actually held -- a "clean but drifting"
  fixation still triggers correction.
- **`bin_tracker_angles` excludes a trial entirely on any single NaN gaze
  sample**, even a brief blink-related one, rather than offering partial
  tolerance or interpolation.

## ERP

- **CSD-transformed (`laplacian=True`) evokeds are silently dropped from
  HTML reports** (`generate_erp_report`). This is a confirmed upstream MNE
  gap (`mne.Report.add_evokeds` raises `KeyError: 'csd'` internally when
  building its topomap slider, even on current MNE versions) -- not
  something that updating `mne` will fix on its own. Consider reporting
  upstream to MNE, or building a custom CSD-aware report section.
