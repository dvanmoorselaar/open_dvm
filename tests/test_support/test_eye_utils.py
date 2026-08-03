"""
Test suite for open_dvm.support.eye_utils.

Organization
------------
- TestExcludeEye: exclude_eye trial-exclusion behavior
"""

import mne
import numpy as np
import pandas as pd

from open_dvm.support.eye_utils import exclude_eye


def _make_epochs_and_df(n_trials=5, n_times=50, sfreq=250, ch_names=("Fz", "Cz")):
    info = mne.create_info(list(ch_names), sfreq, ch_types="eeg")
    data = np.random.RandomState(0).randn(n_trials, len(ch_names), n_times)
    epochs = mne.EpochsArray(data, info, tmin=-0.1, verbose=False)
    df = pd.DataFrame({"condition": np.arange(n_trials)})
    return epochs, df


class TestExcludeEye:
    def test_no_tracker_data_does_not_crash(self, tmp_path):
        """
        Regression test: exclude_eye's no-tracker-data branch referenced
        an undefined variable ('beh' instead of 'df'), raising a
        NameError whenever use_tracker=True but no tracker data (no
        NpzFile, no 'x' channel) was actually available.
        """
        epochs, df = _make_epochs_and_df()
        preproc_file = str(tmp_path / "preproc.json")

        df_out, epochs_out = exclude_eye(
            sj=1,
            session=1,
            df=df,
            epochs=epochs,
            eye_dict={"use_tracker": True, "use_eog": False},
            eye=None,
            preproc_file=preproc_file,
        )

        assert len(df_out) == len(df)
        assert len(epochs_out) == len(df)
