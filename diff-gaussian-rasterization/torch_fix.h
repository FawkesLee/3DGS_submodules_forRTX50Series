// Workaround for PyTorch 2.9 + CUDA 12.9 + MSVC 14.44 compatibility issue
// The "std" namespace becomes ambiguous in compiled_autograd.h
// This header must be included BEFORE torch/extension.h

#ifndef TORCH_FIX_H
#define TORCH_FIX_H

// Force include standard headers first to establish "std" namespace
#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <fstream>
#include <sstream>
#include <iostream>

// Now include torch - the std namespace should be properly resolved
#include <torch/extension.h>

#endif // TORCH_FIX_H
