"""
Download-and-cache the open_dvm example dataset (raw or processed) from OSF.

Mirrors MNE-Python's own dataset-fetching convention (``mne.datasets.sample``),
using ``pooch`` under the hood -- ``pooch`` is already a transitive dependency
via ``mne``, so no new dependency is introduced.

Two independent datasets are available, matching the two ways a tutorial can
start:

- ``fetch_raw_data()`` -- raw EEG/behavioral/eye-tracking files, for
  `01_preprocessing.ipynb` (which actually runs the preprocessing pipeline,
  including its manual ICA-review step).
- ``fetch_processed_data()`` -- already-preprocessed epochs, for
  `02_erp_analysis.ipynb` onward (a fast-path that skips preprocessing
  entirely, since open_dvm's main purpose is analysis of preprocessed data,
  not preprocessing itself).

Both extract directly into a local cache directory using open_dvm's own
folder conventions (see NAMING_CONVENTIONS.md) -- ``eeg/raw/``,
``behavioral/raw/``, ``eye/raw/`` for the raw dataset; ``eeg/processed/``,
``eye/processed/``, ``preprocessing/group_info/`` for the processed one
(behavioral data for processed epochs lives in each epochs file's
``.metadata``, not a separate CSV). The returned path is a drop-in
``project_folder`` for ``FolderStructure``.
"""

import os
from pathlib import Path
from typing import Optional, Union

import pooch

# Direct-download links for the individual files (not the project/folder
# URL) -- each file on OSF has its own short ID; the project page at
# https://osf.io/hmybn/files/osfstorage lists `raw/raw.zip` (~1.3 GB) and
# `processed/processed.zip` (~2.2 GB), both well under OSF's 5 GB per-file
# storage limit. `hash: None` skips integrity verification; pooch logs the
# real SHA256 to the console on first download, so it can be pasted in here
# later once you want the check.
_RAW_ARCHIVE = {
    "fname": "raw.zip",
    "url": "https://osf.io/download/6a6b5798ce7350b7ef22f06f/",
    "hash": None,
}

_PROCESSED_ARCHIVE = {
    "fname": "processed.zip",
    "url": "https://osf.io/download/6a6b5515db4840ed68012fc7/",
    "hash": None,
}


def _get_cache_dir(path: Optional[Union[str, os.PathLike]] = None) -> Path:
    """Resolve the local cache directory for downloaded datasets.

    Priority: explicit `path` argument > `OPEN_DVM_DATA` environment
    variable > `~/open_dvm_data` (created if it doesn't exist yet).
    Mirrors MNE-Python's own `_get_path()` cache-resolution convention.

    Parameters
    ----------
    path : str or os.PathLike, optional
        Explicit cache directory. Takes precedence over everything else.

    Returns
    -------
    Path
        The resolved cache directory (not guaranteed to exist yet --
        created lazily on first fetch, matching pooch's own behavior).
    """
    if path is not None:
        return Path(path)
    env_path = os.environ.get("OPEN_DVM_DATA")
    if env_path:
        return Path(env_path)
    return Path.home() / "open_dvm_data"


def _fetch_archive(archive: dict, path: Optional[Union[str, os.PathLike]] = None) -> str:
    """Download (if not already cached) and extract a single dataset zip.

    Parameters
    ----------
    archive : dict
        Must have keys ``fname``, ``url``, ``hash``.
    path : str or os.PathLike, optional
        Explicit cache directory (see `_get_cache_dir`).

    Returns
    -------
    str
        The local cache directory the archive was extracted into --
        this is what each tutorial assigns to `project_folder`.
    """
    cache_dir = _get_cache_dir(path)
    cache_dir.mkdir(parents=True, exist_ok=True)

    fetcher = pooch.create(
        path=str(cache_dir),
        base_url="",  # full URL given directly in `urls` below
        registry={archive["fname"]: archive["hash"]},
        urls={archive["fname"]: archive["url"]},
    )
    # Deliberately does NOT delete the archive after extraction (unlike
    # MNE's own equivalent, which can rely on a permanent registry hash).
    # pooch's own re-download check is `path.exists() and hash_matches(...)`
    # -- with `hash: None` in the registry, hash_matches() always returns
    # True, so keeping the archive around is what makes repeated calls a
    # no-op instead of re-downloading every time. This also stays correct
    # once real hashes are filled in later (hash_matches then does a real
    # comparison instead of always passing).
    fetcher.fetch(archive["fname"], processor=pooch.Unzip(extract_dir=str(cache_dir)))

    return str(cache_dir)


def fetch_raw_data(path: Optional[Union[str, os.PathLike]] = None) -> str:
    """Download (if needed) and locate the raw tutorial dataset.

    Fetches ``eeg/raw/``, ``behavioral/raw/``, and ``eye/raw/`` for all 7
    tutorial subjects from OSF, extracting into a local cache directory
    that can be used directly as `project_folder` (e.g. for
    `01_preprocessing.ipynb`). A no-op if already cached.

    Parameters
    ----------
    path : str or os.PathLike, optional
        Explicit local directory to use instead of the default cache
        location (`OPEN_DVM_DATA` env var, or `~/open_dvm_data`).

    Returns
    -------
    str
        Local path containing the extracted raw dataset.
    """
    return _fetch_archive(_RAW_ARCHIVE, path=path)


def fetch_processed_data(path: Optional[Union[str, os.PathLike]] = None) -> str:
    """Download (if needed) and locate the preprocessed tutorial dataset.

    Fetches already-preprocessed epochs (`eeg/processed/`), eye-tracking
    data (`eye/processed/`), and the preprocessing parameter log
    (`preprocessing/group_info/`) for all 7 tutorial subjects from OSF --
    a fast-path that skips running `01_preprocessing.ipynb` yourself.
    Extracts into a local cache directory usable directly as
    `project_folder` (e.g. for `02_erp_analysis.ipynb` onward). A no-op
    if already cached.

    Parameters
    ----------
    path : str or os.PathLike, optional
        Explicit local directory to use instead of the default cache
        location (`OPEN_DVM_DATA` env var, or `~/open_dvm_data`).

    Returns
    -------
    str
        Local path containing the extracted processed dataset.
    """
    return _fetch_archive(_PROCESSED_ARCHIVE, path=path)
