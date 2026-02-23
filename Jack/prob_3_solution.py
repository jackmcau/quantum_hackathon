from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit_aer import QasmSimulator

#qr = QuantumRegister(2, 'q')
#cr = ClassicalRegister(2, 'c')
#
#qc = QuantumCircuit(qr,cr)
#qc.x(0)
#qc.h(1)
#
#print(qc)
#
#state = Statevector(qc.reverse_bits())
#print(state.data)
#
#qc.measure(0,0)
#qc.measure(1,1)
#
#backend = QasmSimulator()
#result = backend.run(qc.reverse_bits(), shots=100).result()
#counts = result.get_counts()
#print(counts)

n= int(input("Bits? "))


qr = QuantumRegister(n, 'q')
cr = ClassicalRegister(n, 'c')

qc = QuantumCircuit(qr,cr)
for i in range(n):
    qc.h(0)

qc.measure(range(n),range(n))

backend = QasmSimulator()
result = backend.run(qc.reverse_bits(), shots=100).result()
counts = result.get_counts()
print(counts)