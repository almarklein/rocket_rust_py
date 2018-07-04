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
import os

from ppci import wasm
from ppci.wasm.instantiate import instantiate, create_runtime
from ppci.utils.reporting import HtmlReportGenerator

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

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
    return math.sin(a)

def cos(a):  # [(0, 'f64')] -> ['f64']
    return math.cos(a)

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
    'env': {
        'sin': sin,
        'cos': cos,
        'Math_atan': Math_atan,
        'clear_screen': clear_screen,
        'draw_bullet': draw_bullet,
        'draw_enemy': draw_enemy,
        'draw_particle': draw_particle,
        'draw_player': draw_player,
        'draw_score': draw_score,
    },
    'wasm_rt': create_runtime(),
}


## Compose

# Load WASM module
wasm_data = open('rocket.wasm', 'rb').read()
wasm_module = wasm.Module(wasm_data)
with open('report2.html', 'w') as rfh, HtmlReportGenerator(rfh) as reporter:
    instance = instantiate(wasm_module, imports, target='python', reporter=reporter)
print(instance)
for _ in range(5):
    instance.exports.update(0.1)
    instance.exports.draw()

# Load the native module in this process, with the provided imports
# native_module = load_obj(obj, imports=imports)
# import rocket_wasm
# rocket_wasm.update(1)


## Run it in our app wrapper

# canvas = Canvas(native_module.exports)
# canvas.run()
