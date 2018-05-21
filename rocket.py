""" Run rocket.wasm in Python!

* Load the wasm module, compile to PPCI IR and then to native.
* Load the native object in memory, feed it the API it needs (wasm imports).
* Implement a Python app that uses the exposed API (wasm exports).

At the moment, the game is text based. But we can use Qt or SDL2 (or tk?)
to run it visually, and also feed in user interaction.
"""

import math
import logging
import io

from ppci import wasm
from ppci.irutils import verify_module
from ppci.arch.arch_info import TypeInfo
from ppci.api import ir_to_object, get_current_arch, ir_to_python
from ppci.binutils.outstream import TextOutputStream
from ppci.utils.reporting import HtmlReportGenerator
from ppci.instrument import add_tracer

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

## Canvas

# todo: this part is silly. We need a Qt widget, or maybe tk? Anyway, something to draw to and capture keyboards input.

# todo: ha! we could run this in prompt_toolkit :P

class Canvas:
    
    def __init__(self, wasm_api):
        self.wasm_api = wasm_api
        
        self.wasm_api.resize(100, 100)
    
    def run(self):
        while True:
            
            time.sleep(0.5)
            
            self.wasm_api.update()
            self.wasm_api.draw()


## Imports

def sin(a):  # [(0, 'f64')] -> ['f64'] 
    return Math.sin(a)

def cos(a):  # [(0, 'f64')] -> ['f64']
    return Math.cos(a)

def Math_atan(a):  # [(0, 'f64')] -> ['f64']
    return math.atan(a)

def clear_screen():  # [] -> []
    print('clearing screen')

def draw_bullet(x, y):  # [(0, 'f64'), (1, 'f64')] -> []
    print(f'There is a bullet at {x}, {y}')

def draw_enemy(x, y):  # [(0, 'f64'), (1, 'f64')] -> []
    print(f'There is an enemy at {x}, {y}')

def draw_particle(x, y, a): # [(0, 'f64'), (1, 'f64'), (2, 'f64')] -> []
    print(f'There is a partical at {x}, {y} angle {a}')

def draw_player(x, y, a):  # [(0, 'f64'), (1, 'f64'), (2, 'f64')] -> []
    print(f'The player is at {x}, {y} angle {a}')

def draw_score(score):  #  env.draw_score:    [(0, 'f64')] -> []
    print(f'The score is {score}!')


imports = {
    'sin': sin,
    'cos': cos,
    'Math_atan': Math_atan,
    'clear_screen': clear_screen,
    'draw_bullet': draw_bullet,
    'draw_enemy': draw_enemy,
    'draw_particle': draw_particle,
    'draw_player': draw_player,
    'draw_score': draw_score,
}


## Compose

# Load WASM module
wasm_data = open('rocket.wasm', 'rb').read()
wasm_module = wasm.Module(wasm_data)

# WASM to PPCI
with open('report.html', 'w') as rfh, HtmlReportGenerator(rfh) as reporter:
    ptr_info = TypeInfo(4, 4)
    ppci_module = wasm.wasm_to_ir(wasm_module, ptr_info, reporter=reporter)
    reporter.message(ppci_module.stats())
    reporter.dump_ir(ppci_module)
    verify_module(ppci_module)
    add_tracer(ppci_module)
    verify_module(ppci_module)
    # ppci_module.display()

    # PPCI to native
    arch = get_current_arch()
    f = io.StringIO()
    txt_stream = TextOutputStream(f=f, add_binary=True)
    # obj = ir_to_object([ppci_module], arch, debug=True, outstream=txt_stream, reporter=reporter)

    with open('gen_rocket_wasm.py', 'w') as f:
        ir_to_python([ppci_module], f, reporter=reporter)

# Load the native module in this process, with the provided imports
# native_module = load_obj(obj, imports=imports)
# import rocket_wasm
# rocket_wasm.update(1)


## Run it in our app wrapper

# canvas = Canvas(native_module.exports)
# canvas.run()
