from MAxPy import *

circuit = maxpy.AxCircuit(top_name="sobel")
circuit.rtl2py(base="rtl", target="exact")
