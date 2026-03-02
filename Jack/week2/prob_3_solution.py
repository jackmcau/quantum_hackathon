from qiskit import *
from qiskit_aer import QasmSimulator
from matplotlib.pyplot import *

backend = QasmSimulator()

def generate_random_string(n): # We wrote this in week 1
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr,cr)
    for i in range(n):
        qc.h(qr[i])
    qc.measure(range(n), range(n))
    result = list(backend.run(qc.reverse_bits(), shots=1).result().get_counts().keys())[0]
    return result

def generate_alice_state(a):
    qr = QuantumRegister(len(a), 'q')
    cr = ClassicalRegister(len(a), 'c')
    qc = QuantumCircuit(qr, cr)
    for i, v in enumerate(a):
        if v == "1":
            qc.h(qr[i]) # put into |+>
    return qc

def eavesdrop(e, n, state: QuantumCircuit):
    if e:
        state.x([i for i in range(n)]) # Unitary x gate on first qubit
    return state

def bob_evolution(b): # U b --> Hadamard gate on all "1"s and I on everything else
    qc = QuantumCircuit(len(b))
    for i, v in enumerate(b):
        if v == "1":
            qc.h(i)
    return qc

def measurement_result(b, state: QuantumCircuit, U_b: QuantumCircuit):
    state.append(U_b.to_gate(), [i for i in range(len(b))])
    state.measure(range(len(b)), range(len(b)))
    result = list(backend.run(state.decompose().reverse_bits(), shots=1).result().get_counts().keys())[0]
    return result

def alice_create_secret_key(a, t):
    key = ""
    for i, v in enumerate(t):
        if v == "1":
            key += a[i]
    return key

def bob_create_secret_key(b, t):
    key = ""
    for i, v in enumerate(t):
        if v == "1":
            if b[i] == "0":
                key += "1"
            else:
                key += "0"
    return key

def check_for_eve(SK_a, SK_b): # As a "random sample" i just decided to use the first half of the secret key
    return (SK_a[len(SK_a)//2:] if (SK_a[:len(SK_a)//2] == SK_b[:len(SK_a)//2]) else "Eve detected!")


# Provided test
def main():
    n = int(input("Security parameter: ")) # Choose security parameter
    e = bool(int(input("Eavesdrop? (0=n,1=y) "))) # Choose to have eavesdropper or not
    a = generate_random_string(n) # Alice generates string a
    state = generate_alice_state(a) # Alice encodes a into quantum state

    # Alice sends state to Bob
    state = eavesdrop(e,n,state) # Eve intercepts state

    # Eve sends (possibly modified) state to Bob
    b = generate_random_string(n) # Bob generates string b
    U_b = bob_evolution(b) # Bob constructs his unitary U_b
    t = measurement_result(b,state,U_b) # Bob measures state, constructs string t

    # Bob sends t to Alice
    SK_a = alice_create_secret_key(a,t) # Alice constructs her key SK_a
    SK_b = bob_create_secret_key(b,t) # Bob constructs his key SK_b
    check = check_for_eve(SK_a, SK_b) # Check for Eve
#
    if check == "Eve detected!": # Eve detected, abort
        print("Eve detected! Aborting protocol.")
    else: # Eve not detected
        print("Eve not detected.")
        SK = check # Set SK to unchecked bits of SK_a
        print("Secret Key: " + SK)
        print("Secret Key Length: " + str(len(SK)))

def testCount():
    n = int(input("Security parameter: ")) # Choose security parameter
    trials = int(input("Trials: "))
    keys = []
    present = 0 # Present and gone serve as counts for the number of times the algorithm has failed for eve being present and gone
    gone = 0
    for e in [True, False]:
        for i in range(trials):
            a = generate_random_string(n) # Alice generates string a
            state = generate_alice_state(a) # Alice encodes a into quantum state

            # Alice sends state to Bob
            state = eavesdrop(e,n,state) # Eve intercepts state

            # Eve sends (possibly modified) state to Bob
            b = generate_random_string(n) # Bob generates string b
            U_b = bob_evolution(b) # Bob constructs his unitary U_b
            t = measurement_result(b,state,U_b) # Bob measures state, constructs string t

            # Bob sends t to Alice
            SK_a = alice_create_secret_key(a,t) # Alice constructs her key SK_a
            SK_b = bob_create_secret_key(b,t) # Bob constructs his key SK_b
            check = check_for_eve(SK_a, SK_b) # Check for Eve

            if check == "Eve detected!": # Eve detected, abort
                if not e: # Eve detected when not actually there
                    gone += 1
            else: # Eve not detected
                if e: # eve not detected while present
                    present += 1
                else:
                    keys.append(check)
    sum = 0
    for i in keys:
        sum += len(i)
    print("Stats:")
    print(f"\tFalse positives: {gone}")
    print(f"\tFalse negatives: {present}")
    print(f"\tAverage key length: {sum/len(keys)}")

if __name__ == "__main__":
    if(input("Enter 'test' for testing, anything else to normally run: ") == "test"):
        testCount()
    else:
        main()