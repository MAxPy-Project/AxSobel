from MAxPy import *
from testbench import sobel_testbench

circuit = maxpy.AxCircuit(top_name="sobel")
circuit.set_testbench_script(sobel_testbench)

# parameter substituition loop "study no 1"
circuit.set_group("study_no_1")
circuit.set_synth_tool(None)
circuit.set_results_filename("output.csv")
circuit.parameters = {
    "[[PARAM_ADD1]]": ["copyA","copyB", "eta1", "loa", "trunc0", "trunc1"],
    "[[PARAM_K1]]": ["0", "1", "2", "3", "4", "5", "6"],
    "[[PARAM_K2]]": ["0", "1", "2", "3", "4", "5", "6"],
    "[[PARAM_K3]]": ["0", "1", "2", "3", "4", "5", "6"],
    "[[PARAM_K4]]": ["0", "1", "2", "3", "4", "5", "6"],
}
circuit.rtl2py_param_loop(base="rtl_param")
