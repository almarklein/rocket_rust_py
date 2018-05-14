# Run Rocket, implemented in Rust, in Python, via WASM

A [Rocket game implemented in Rust](https://github.com/aochagavia/rocket_wasm)
is compiled to WebAssembly (WASM). We take the resulting `.wasm` file, and run
it in Python using [PPCI](https://bitbucket.org/windel/ppci/).
