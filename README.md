🐟 Barracuda Programming Language

![Barracuda logo](Logo.png)


(Development in progress)

Barracuda v0.1 (Proof of Concept)

Welcome to the initial release of Barracuda, a language designed with type safety and Pythonic indentations to simplify high-performance frontend development.

🌊 What is Barracuda?

Barracuda is a proof-of-concept extension language that bridges the gap between readable Python-style logic and the raw performance of WebAssembly (Wasm).

The current implementation (v0.1) uses a Python-based interpreter/compiler to transform your .cuda scripts into logic that can eventually be offloaded to the browser's Wasm engine, specifically targeting heavy mathematical workloads where JavaScript often hits a "performance ceiling."

🛠 v0.1 Release Notes

    Pythonic Syntax Parser: Support for basic functions, if/else, and while loops using indentation-based scoping.

    Strict Type Safety: Initial support for int and bool declarations to prevent runtime type errors.

    Indentation Logic: Clean, readable code structure without the need for curly braces or semicolons.

    Python-Powered Compiler: A lightweight compiler written in Python that parses Barracuda source code (PoC phase).

📋 Example Usage

sample.cuda
    var int x == 8
    var int y == 2
    var bool z == True

    check == additionLoop: x, y, z

    println: check

    func: additionLoop: a, b, c
        while: a > b
            a = a + 1
        return: c

🚧 Current Limitations

    Interpreter Status: v0.1 is primarily a transpiler/interpreter; direct "one-click" binary Wasm compilation is the next major milestone.

    Limited Types: Currently only supports int and bool. Support for float and array is pending.

🛣 Roadmap

    Direct Wasm Compilation: Moving from interpreted logic to generating actual .wasm binaries.

    Native Math Ops: Embedding advanced trigonometric and algebraic operations directly into the core language.

    VS Code Support: Syntax highlighting and linting extension for .cuda files.



⚖️ License

Barracuda is released under the Apache License 2.0. This license allows for free use, modification, and distribution while providing an explicit grant of patent rights from contributors. See the LICENSE file for details.

