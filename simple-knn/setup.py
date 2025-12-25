#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["TORCH_CUDA_ARCH_LIST"] = "9.0"

from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension

# 跳过 CUDA 版本检查
import torch.utils.cpp_extension as cpp_ext
_original_check = cpp_ext._check_cuda_version
def _patched_check(*args, **kwargs):
    try:
        _original_check(*args, **kwargs)
    except RuntimeError as e:
        if "mismatches" in str(e):
            print(f"[WARN] Ignoring CUDA version mismatch: {e}")
        else:
            raise
cpp_ext._check_cuda_version = _patched_check

cxx_compiler_flags = []
nvcc_flags = ['-allow-unsupported-compiler', '-gencode=arch=compute_90,code=sm_90']

if os.name == 'nt':
    cxx_compiler_flags.append("/wd4624")

setup(
    name="simple_knn",
    ext_modules=[
        CUDAExtension(
            name="simple_knn._C",
            sources=[
            "spatial.cu",
            "simple_knn.cu",
            "ext.cpp"],
            extra_compile_args={"nvcc": nvcc_flags, "cxx": cxx_compiler_flags})
        ],
    cmdclass={
        'build_ext': BuildExtension
    },
    version='1.0.0'
)
