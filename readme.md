# Introduction

This project is a guide on installing the essential sub-modules of 3DGS using NVIDIA RTX 5080 (Blackwell architecture) on Windows 11. It should be noted that due to Blackwell being too new, many old projects similar to the original version of 3DGS are not supported. This also indicates that overly new equipment may not be suitable for legacy projects.

# Acknowledgements

Special thanks to the original authors of 3D Gaussian Splatting for making their repository publicly available:

- **3D Gaussian Splatting**: [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) - Original reference implementation of "3D Gaussian Splatting for Real-Time Radiance Field Rendering"

# Preparations

Under the premise that the CUDA version within the system is relatively new, it is recommended to use the following versions of components:

| Component | Recommended Version |
|-----------|---------------------|
| **PyTorch** | 2.7.0+cu128 |
| **CUDA Toolkit** | >= 12.4 |
| **MSVC** (for `cl.exe`) | v143 (VS 2022) |
| **Python** | 3.10 - 3.12 |

> ⚠️ **Note**: PyTorch 2.9 has known compatibility issues with MSVC 14.44+ due to `std` namespace conflicts in `compiled_autograd.h`. Use PyTorch 2.7.0 for stable compilation. The command of installation is `pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128`
> Besides, if you need to install `torch-scatter` or `pytorch-scatter`, just put `pip install torch-scatter -f https://data.pyg.org/whl/torch-2.7.0+cu128.html` in the command line.

# How to Use

In order to facilitate the unification of the environment, please be sure to open the submodules folder in the **x64 Native Tools Command Prompt for VS 2022** command-line window and perform the following operations:

## 1. Check the CUDA Version in System

Make sure the CUDA version in system is compatible enough for the project (>= 12.4):

```cmd
nvcc -V
```

## 2. Activate Conda Environment

```cmd
conda activate <your_env_name>
```

## 3. Common Issues and Solutions

### OMP ERROR

You may encounter the problem:
```
OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
```

Solution:
```cmd
set KMP_DUPLICATE_LIB_OK=TRUE
```

### Cannot Open File "crtdefs.h": No such file or directory

The reason may be that nvcc compiler cannot detect the file `crtdefs.h` in the system. Even if you have installed the packages related to MSVC, you need to initialize the VS environment:

```cmd
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" amd64
```

Or for VS 2025 Preview with specific MSVC version:
```cmd
"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" amd64 -vcvars_ver=14.44.17.14
```

**Explanation**: You need to find the file `vcvarsall.bat` in your system and run it with:
- `amd64` - for 64-bit Windows with Intel/AMD x86-64 CPUs
- `-vcvars_ver=<version>` - optional, specify the MSVC version if you have multiple installed

## 4. Install the Sub-modules

Enter each sub-module folder and execute:

```cmd
cd diff-gaussian-rasterization
pip install . --no-build-isolation

cd ../simple-knn
pip install . --no-build-isolation
```

**Note**: The `--no-build-isolation` parameter tells pip to use the PyTorch and other dependencies already installed in your current conda environment for compilation, instead of creating an isolated build environment.

## 5. Verify Installation

```python
python -c "import diff_gaussian_rasterization; print('diff_gaussian_rasterization OK')"
python -c "import simple_knn; print('simple_knn OK')"
```

# Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `std: ambiguous symbol` | PyTorch 2.9 + MSVC 14.44+ incompatibility | Use PyTorch 2.5.1 |
| `CUDA version mismatch` | System CUDA differs from PyTorch CUDA | Patch setup.py to skip version check |
| `sm_120 not supported` | Blackwell arch not in PyTorch | Set `TORCH_CUDA_ARCH_LIST=9.0` |
| `ModuleNotFoundError: torch` | Build isolation enabled | Use `--no-build-isolation` |

# License

The sub-modules follow the original license from [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting). Please refer to their LICENSE.md for details.
