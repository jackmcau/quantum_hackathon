from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit_aer import QasmSimulator
import matplotlib.pyplot as plt

n = int(input("Bits? "))

qr = QuantumRegister(n, 'q')
cr = ClassicalRegister(n, 'c')

qc = QuantumCircuit(qr,cr)
for i in range(n):
    qc.h(qr[i])

qc.measure(range(n),range(n))

backend = QasmSimulator()
result = backend.run(qc.reverse_bits(), shots=10000).result()
counts = result.get_counts()

plot_histogram(counts,
               bar_labels=False,
               title="Counts over 10000 runs of random number generator")
plt.show()