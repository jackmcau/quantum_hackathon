from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit_aer import QasmSimulator
import matplotlib.pyplot as plt

# Length of bit-string from user
n = int(input("Bits? "))

# Create registers of n Qubits
qr = QuantumRegister(n, 'q')
cr = ClassicalRegister(n, 'c')
qc = QuantumCircuit(qr,cr)

# Apply Hadamard gate to each Qubit
for i in range(n):
    qc.h(qr[i])

# Measure all Qubits with applied transformations
qc.measure(range(n),range(n))

# Simulate for 10,000 trials
backend = QasmSimulator()
result = backend.run(qc.reverse_bits(), shots=10000).result()
counts = result.get_counts()

# Plot the result
plot_histogram(counts,
               bar_labels=False,
               title="Counts over 10000 runs of random number generator")
plt.show()