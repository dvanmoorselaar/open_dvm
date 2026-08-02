"""
Test suite for open_dvm.support.datasets.

Organization
------------
- TestGetCacheDir: cache-directory resolution (path arg > env var > default)
- TestFetchArchive: pooch.create()/fetch() called with the right arguments
- TestFetchRawData / TestFetchProcessedData: correct archive dict used
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from open_dvm.support.datasets import (
    _PROCESSED_ARCHIVE,
    _RAW_ARCHIVE,
    _fetch_archive,
    _get_cache_dir,
    fetch_processed_data,
    fetch_raw_data,
)


class TestGetCacheDir:
    @pytest.mark.unit
    def test_explicit_path_wins(self, monkeypatch, tmp_path):
        monkeypatch.setenv("OPEN_DVM_DATA", str(tmp_path / "env_dir"))

        result = _get_cache_dir(path=tmp_path / "explicit_dir")

        assert result == tmp_path / "explicit_dir"

    @pytest.mark.unit
    def test_env_var_used_when_no_explicit_path(self, monkeypatch, tmp_path):
        monkeypatch.setenv("OPEN_DVM_DATA", str(tmp_path / "env_dir"))

        result = _get_cache_dir(path=None)

        assert result == tmp_path / "env_dir"

    @pytest.mark.unit
    def test_default_when_neither_given(self, monkeypatch):
        monkeypatch.delenv("OPEN_DVM_DATA", raising=False)

        result = _get_cache_dir(path=None)

        assert result == Path.home() / "open_dvm_data"


class TestFetchArchive:
    @pytest.mark.unit
    def test_creates_cache_dir(self, tmp_path):
        cache_dir = tmp_path / "does_not_exist_yet"
        archive = {"fname": "raw.zip", "url": "http://example.com/raw.zip", "hash": None}

        with patch("open_dvm.support.datasets.pooch.create") as mock_create:
            mock_create.return_value = MagicMock()
            _fetch_archive(archive, path=cache_dir)

        assert cache_dir.is_dir()

    @pytest.mark.unit
    def test_pooch_create_called_with_expected_registry_and_urls(self, tmp_path):
        archive = {"fname": "raw.zip", "url": "http://example.com/raw.zip", "hash": "abc123"}

        with patch("open_dvm.support.datasets.pooch.create") as mock_create:
            mock_create.return_value = MagicMock()
            _fetch_archive(archive, path=tmp_path)

        mock_create.assert_called_once_with(
            path=str(tmp_path),
            base_url="",
            registry={"raw.zip": "abc123"},
            urls={"raw.zip": "http://example.com/raw.zip"},
        )

    @pytest.mark.unit
    def test_fetcher_fetch_called_with_unzip_processor_into_cache_dir(self, tmp_path):
        archive = {"fname": "raw.zip", "url": "http://example.com/raw.zip", "hash": None}
        mock_fetcher = MagicMock()

        with patch("open_dvm.support.datasets.pooch.create", return_value=mock_fetcher):
            with patch("open_dvm.support.datasets.pooch.Unzip") as mock_unzip:
                _fetch_archive(archive, path=tmp_path)

        mock_unzip.assert_called_once_with(extract_dir=str(tmp_path))
        mock_fetcher.fetch.assert_called_once_with("raw.zip", processor=mock_unzip.return_value)

    @pytest.mark.unit
    def test_returns_cache_dir_as_string(self, tmp_path):
        archive = {"fname": "raw.zip", "url": "http://example.com/raw.zip", "hash": None}

        with patch("open_dvm.support.datasets.pooch.create") as mock_create:
            mock_create.return_value = MagicMock()
            result = _fetch_archive(archive, path=tmp_path)

        assert result == str(tmp_path)

    @pytest.mark.unit
    def test_archive_not_deleted_after_extraction(self, tmp_path):
        # Regression: deleting the archive after extraction breaks pooch's
        # own re-download check (download_action() returns 'download'
        # whenever the archive file doesn't exist locally, regardless of
        # hash) -- so repeated calls would silently re-download every time
        # instead of being a no-op. The fix is to simply not delete it;
        # this test guards against that regressing.
        archive = {"fname": "raw.zip", "url": "http://example.com/raw.zip", "hash": None}
        # simulate pooch actually having "downloaded" the archive to disk
        (tmp_path / "raw.zip").write_text("pretend zip bytes")

        with patch("open_dvm.support.datasets.pooch.create") as mock_create:
            mock_create.return_value = MagicMock()
            _fetch_archive(archive, path=tmp_path)

        assert (tmp_path / "raw.zip").is_file()


class TestFetchRawData:
    @pytest.mark.unit
    def test_uses_raw_archive_dict(self, tmp_path):
        with patch("open_dvm.support.datasets._fetch_archive") as mock_fetch:
            mock_fetch.return_value = str(tmp_path)
            result = fetch_raw_data(path=tmp_path)

        mock_fetch.assert_called_once_with(_RAW_ARCHIVE, path=tmp_path)
        assert result == str(tmp_path)


class TestFetchProcessedData:
    @pytest.mark.unit
    def test_uses_processed_archive_dict(self, tmp_path):
        with patch("open_dvm.support.datasets._fetch_archive") as mock_fetch:
            mock_fetch.return_value = str(tmp_path)
            result = fetch_processed_data(path=tmp_path)

        mock_fetch.assert_called_once_with(_PROCESSED_ARCHIVE, path=tmp_path)
        assert result == str(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
