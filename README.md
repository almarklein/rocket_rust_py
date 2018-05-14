# The Rocket game, implemented in Rust, running in Python, via WASM 

A [Rocket game implemented in Rust](https://github.com/aochagavia/rocket_wasm)
is compiled to WebAssembly (WASM). We take the resulting `.wasm` file, and run
it in Python using [PPCI](https://bitbucket.org/windel/ppci/).

* `rocket.wasm`: the wasm module compiled from Rust.
* `rocket.py`: the Python code to wrap the above in an app.
* `info.py`: print some info about the wasm module.
* `rocket.html`: for reference, the (nearly) original html/js to run the wasm module in the browser (standalone HTML).
