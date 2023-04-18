from maxpy import *
from testbench import sobel_testbench

circuit = maxpy.AxCircuit(top_name="sobel")
circuit.set_testbench_script(sobel_testbench)
circuit.set_synth_tool("yosys")

circuit.rtl2py(base="rtl", target="exact")
circuit.rtl2py(base="rtl_onecomp", target="onecomp")
circuit.rtl2py(base="rtl_loak0", target="loak0")
