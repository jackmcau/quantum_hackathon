from qiskit import *
from qiskit_aer import QasmSimulator
from qiskit.circuit.library import grover_operator, MCMTGate, ZGate
import matplotlib.pyplot as plt
import pandas as pd

def create_oracle(marked_state):
    circuit = QuantumCircuit(len(marked_state))
    for i, v in enumerate(marked_state):
        if v == "0":
            circuit.x(int(i))

    circuit.compose(MCMTGate(ZGate(), len(marked_state)-1, 1), inplace=True)

    for i,v in enumerate(marked_state):
        if v == "0":
            circuit.x(int(i))
    # lambda^(n-1)(Z)
    return circuit
    
def create_grover_operator(oracle):
    grover_op = grover_operator(oracle) # add the rest of the grover operator
    return grover_op

def create_grover_circuit(r, grover_op):
    qc1 = QuantumCircuit(grover_op.num_qubits,grover_op.num_qubits)
    for i in range(grover_op.num_qubits):
        qc1.h(i) # Hadamard all of the qubits initially

    qc1.compose(grover_op.power(r), inplace=True)
    qc1.measure(range(grover_op.num_qubits), range(grover_op.num_qubits))
    return qc1


def run_grover_circuit(marked_state, r):
    oracle = create_oracle(marked_state)
    grover_op = create_grover_operator(oracle)
    grover_circuit = create_grover_circuit(r, grover_op)
    backend = QasmSimulator()
    grover_circuit = transpile(grover_circuit, backend)

    result = backend.run(grover_circuit.reverse_bits(), shots=10000).result()
    counts = result.get_counts()
    return counts

if __name__ == "__main__":
    data = run_grover_circuit("0010", 2)
    nums = pd.Series(data.keys())
    counts = pd.Series(data.values())
    counts = counts/sum(counts)
    plt.bar(nums, counts)
    plt.title("Outputs of Grover's Algorithm with Marked State 0010 and r=2")
    plt.xlabel("Output #")
    plt.ylabel("Probability")
    plt.show()
    data = run_grover_circuit("0010", 3)
    nums = pd.Series(data.keys())
    counts = pd.Series(data.values())
    counts = counts/sum(counts)
    plt.bar(nums, counts)
    plt.title("Outputs of Grover's Algorithm with Marked State 0010 and r=3")
    plt.xlabel("Output #")
    plt.ylabel("Probability")
    plt.show()