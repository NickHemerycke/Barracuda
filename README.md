🐟 Barracuda Programming Language

Barracuda is a high-performance systems programming language designed for the modern Linux ecosystem. It combines the clean, indentation-based elegance of Python with the raw power and memory control of C, powered by the LLVM compiler infrastructure.

The goal of Barracuda is to provide a "no-compromise" experience: write code that looks like a script, but executes as a highly optimized native ELF binary.
🚀 Key Features

    Pythonic Syntax: Clean, brace-free code using meaningful indentation.

    LLVM Backend: Leverages the same optimization engine as Clang and Swift for industry-leading performance.

    Static Type Inference: The speed of static types with the feel of a dynamic language.

    Zero-Cost Abstractions: No Garbage Collector (GC) and no hidden runtime overhead.

    Linux First: Built-in support for native syscalls and ELF executable generation.


Barracuda follows a modular compiler pipeline:

    Lexer/Parser: Converts .ba source files into an Abstract Syntax Tree (AST).

    Semantic Analyzer: Handles type inference and ensures the logic is sound.

    IR Generator: Translates the AST into LLVM Intermediate Representation (IR).

    Backend: LLVM optimizes the IR and emits a native Linux object file.

    Linker: Produces the final standalone ELF binary.

🛠️ Getting Started
Prerequisites

    A Linux-based operating system.

    llvm (version 15 or higher recommended).

    clang and lld (for linking).

    python3 (for the initial compiler prototyping).

Installation

(Development in progress)
Bash

git clone https://github.com/your-username/barracuda.git
cd barracuda
make install

⚖️ License

Barracuda is released under the Apache License 2.0. This license allows for free use, modification, and distribution while providing an explicit grant of patent rights from contributors. See the LICENSE file for details.
🤝 Contributing

Barracuda is born from a love for Linux and systems engineering. We welcome contributors who are interested in:

    Compiler Design & AST logic.

    LLVM IR optimization.

    Linux Kernel syscall interfacing.

Next Step: Would you like me to generate a LICENSE file text or a Makefile to help you organize the build process for your compiler?
