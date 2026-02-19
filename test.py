from qiskit import *
qr = QuantumRegister(2, 'q')
cr = ClassicalRegister(2, 'c')

qc = QuantumCircuit(qr,cr)
print(qc)