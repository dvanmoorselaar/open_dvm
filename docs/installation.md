# Installation

## Requirements

- Python 3.8 or higher
- MNE-Python >= 1.0
- NumPy, SciPy, Pandas, Matplotlib

## Install from PyPI

```bash
pip install open-dvm
```

## Install from source (development)

```bash
git clone https://github.com/dvanmoorselaar/open_dvm.git
cd open_dvm
pip install -e ".[dev]"
```

## Verify installation

```python
import open_dvm
print(open_dvm.__version__)
```

## Getting Started

After installation, check out the [Tutorials](tutorials/index) to learn how to use open_dvm for EEG analysis!

## Troubleshooting

If you encounter issues during installation, ensure you have the latest versions of pip and setuptools:

```bash
pip install --upgrade pip setuptools
```

Then try installing open_dvm again.
