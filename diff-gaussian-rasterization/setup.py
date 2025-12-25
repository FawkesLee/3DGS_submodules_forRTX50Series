import os
import torch
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension

# 核心配置：适配RTX5080(12.0) + CUDA13.1 + 禁用Dynamo
os.environ["USE_NINJA"] = "0"
os.environ["DISTUTILS_USE_SDK"] = "1"
os.environ["TORCH_NO_VC_ENV"] = "1"
os.environ["TORCH_DISABLE_DYNAMO"] = "1"
os.environ["TORCH_CUDA_ARCH_LIST"] = "9.0"  # 12.0兼容编码

# 跳过 CUDA 版本检查 (CUDA 13.1 vs PyTorch CUDA 12.4)
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

# 系统CUDA路径（根据你的安装路径调整）
CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.1"

# 验证显卡信息
try:
    cc = torch.cuda.get_device_capability(0)
    print(f"[OK] Detected GPU Compute Capability: {cc[0]}.{cc[1]}")
    print(f"[OK] Using CUDA Arch: 9.0 (compatible with 12.0)")
except Exception as e:
    print(f"[WARN] GPU detection failed: {e}")

# 编译参数配置
include_dirs = [
    os.path.join(CUDA_PATH, "include"),
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party", "glm"),
    torch.utils.cpp_extension.include_paths()[0],
]

library_dirs = [
    os.path.join(CUDA_PATH, "lib/x64"),
]

# NVCC编译参数
nvcc_args = [
    '-O3',
    '-std=c++17',
    '--expt-relaxed-constexpr',
    '--expt-extended-lambda',
    '--use_fast_math',
    '-gencode=arch=compute_90,code=sm_90',
    '-gencode=arch=compute_90,code=compute_90',
    '-allow-unsupported-compiler',
    '-DTORCH_DISABLE_DYNAMO=1',
    '-diag-suppress=1569',
    '-diag-suppress=902',
]

# C++编译参数
cxx_args = [
    '/O2',
    '/std:c++17',
    '/DTORCH_DISABLE_DYNAMO=1',
]

# 构建扩展
ext_modules = [
    CUDAExtension(
        name='diff_gaussian_rasterization._C',
        sources=[
            'rasterize_points.cu',
            'cuda_rasterizer/rasterizer_impl.cu',
            'cuda_rasterizer/forward.cu',
            'cuda_rasterizer/backward.cu',
        ],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        extra_compile_args={
            'nvcc': nvcc_args,
            'cxx': cxx_args
        },
        libraries=['cudart']
    )
]

setup(
    name='diff_gaussian_rasterization',
    version='0.1',
    packages=['diff_gaussian_rasterization'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExtension.with_options(use_ninja=False)}
)