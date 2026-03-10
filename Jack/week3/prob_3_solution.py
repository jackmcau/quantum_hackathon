from qiskit import *
from qiskit_aer import QasmSimulator
from qiskit.circuit.library import grover_operator, MCMTGate, ZGate
import matplotlib.pyplot as plt

def create_oracle(marked_state):
    circuit = QuantumCircuit(len(marked_state))
    for i, v in enumerate(marked_state):
        if v == "0":
            circuit.x(int(i))
    circuit.barrier()
    circuit.compose(MCMTGate(ZGate(), len(marked_state)-1, 1), inplace=True)
    circuit.barrier()

    for i,v in enumerate(marked_state):
        if v == "0":
            circuit.x(int(i))
    # lambda^(n-1)(Z)
    circuit.barrier()
    circuit.draw(output="mpl")
    plt.show
    return circuit
    
def create_grover_operator(oracle):
    grover_op = grover_operator(oracle)
    grover_op.barrier()
    return grover_op

def create_grover_circuit(r, grover_op):
    qc1 = QuantumCircuit(grover_op.num_qubits,grover_op.num_qubits)
    for i in range(grover_op.num_qubits):
        qc1.h(i) # Hadamard all of the qubits initially

    qc1.barrier()
    qc1.compose(grover_op.power(r), inplace=True)
    qc1.measure(range(grover_op.num_qubits), range(grover_op.num_qubits))
    return qc1


def run_grover_circuit(marked_state, r):
    oracle = create_oracle(marked_state)
    grover_op = create_grover_operator(oracle)
    grover_circuit = create_grover_circuit(r, grover_op)
    backend = QasmSimulator()
    grover_circuit = transpile(grover_circuit, backend)

    grover_circuit.draw(output="mpl")
    plt.show()
    result = backend.run(grover_circuit.reverse_bits(), shots=10000).result()
    counts = result.get_counts()
    return counts

if __name__ == "__main__":
    print(run_grover_circuit("0010", 2))
    #plt.hist(run_grover_circuit("0101", 2).values())
    #plt.show()