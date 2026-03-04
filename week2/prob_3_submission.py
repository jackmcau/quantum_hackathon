from typing import List
from qiskit import *
from qiskit_aer import QasmSimulator
from qiskit.circuit.library import HGate, IGate

def generate_random_string(n: int) -> str: # We wrote this in week 1
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr,cr)
    for i in range(n):
        qc.h(qr[i])
    qc.measure(range(n), range(n))
    backend = QasmSimulator()
    result = list(backend.run(qc.reverse_bits(), shots=1).result().get_counts().keys())[0]
    return result

def generate_alice_state(a: str) -> List[QuantumCircuit]:
    outList = []
    # I choose to represent the qubits as a list of individual quantum circuits since
    # Python was throwing a memory error with quantum circuits of size 1000
    # The math is the same
    for i, v in enumerate(a):
    # For every character in a, if the character is a 1 apply a hadamard gate to the corresponding qubit
    # Phi a = kronecker phi a sub i
    # Corresponding to step 2
        outList.append(QuantumCircuit(1,1))
        if v == "1":
            outList[i].h(0)
    return outList

def eavesdrop(e: bool, n: int, state: List[QuantumCircuit]) -> List[QuantumCircuit]:
    if e:
        for i in state:
            i.y([0]) # apply y gate to all qubits as the eavesdropping
        #state[len(state)-1].h([0])
    return state

def bob_evolution(b: str): # U b --> Hadamard gate on all "1"s and I on everything else
    gatesOut = []
    for i, v in enumerate(b):
        if v == "1":
            gatesOut.append(HGate())
        else:
            gatesOut.append(IGate())
    return gatesOut

def measurement_result(b: str, state: List[QuantumCircuit], U_b) -> str:
    strout = ""
    backend = QasmSimulator()
    for i, v in enumerate(state):
        v.append(U_b[i], [0]) # apply the states given by bob_evolution
        v.measure(0,0)
        strout += list(backend.run(v.reverse_bits(), shots=1).result().get_counts().keys())[0]
    return strout

def alice_create_secret_key(a: str, t: str) -> str:
    key = ""
    for i, v in enumerate(t):
        if v == "1":
            key += a[i]
    return key

def bob_create_secret_key(b: str, t: str) -> str:
    key = ""
    for i, v in enumerate(t):
        if v == "1":
            if b[i] == "0":
                key += "1"
            else:
                key += "0"
    return key

def check_for_eve(SK_a: str, SK_b: str) -> str: # As a "random sample" i just decided to use the first half of the secret key
    return (SK_a[len(SK_a)//2:] if (SK_a[:len(SK_a)//2] == SK_b[:len(SK_a)//2]) else "Eve detected!")
    # Returns the not compared half of SK if equivalent


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
    print(f"\tFalse positives: {gone} -> {float(gone)/float(trials)*100}%")
    print(f"\tFalse negatives: {present} -> {float(present)/float(trials)*100}%")
    print(f"\tAverage key length: {sum/len(keys)}")

if __name__ == "__main__":
    if(input("Enter 'test' for testing, anything else to normally run: ") == "test"):
        testCount()
    else:
        main()

# Question 1: Let n be small (say less than 10). Running the protocol 10 times, is Eve detected in every case?
#   Running the program with n=5 for 10 trials while Eve is present gives 4 false negatives, or Eve is not detected 4 out of the 10 times she eavesdrops.
# Question 2: Let n be large (say more than 1000). Running the protocol 10 times, is Eve detected in every case?
#   With n=1500 for 10 trials, Eve is detected in every case. Increasing the security parameter makes Eve more detectable.
# Question 3: Based on your observations in cases when Eve is not detected (or does not exist), what would you guess is the expected length of SK in terms of n?
#   The average length of SK goes up with the security parameter, (in 10 trials) n=5 has an average length of 1, n=10 is 1.7, n=500 gets 62.8, and n=1000 gets 128.
#   The ratio of length of SK to n sits at about 0.125 (62.8/500=0.1256 and 128/1000=0.128) for higher ranges of n, but this is not as good of an estimate for small n near 10.
#   Thus, the expected length of SK from these observations is 0.125n.