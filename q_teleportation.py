
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, Operator
import numpy as np

def quantum_teleportation():
    """
    Simulates quantum teleportation of a qubit using entanglement.
    """
    print("--- Running Quantum Teleportation ---")

    # Step 1: Initialize 3 qubits (q0 = state to teleport, q1 = Alice's entanglement, q2 = Bob's entanglement)
    qc = QuantumCircuit(3)

    # Step 2: Prepare the state to teleport (Alice's qubit)
    qc.h(0)
    qc.t(0)
 
    # Step 3: Create entangled Bell pair between q1 (Alice) and q2 (Bob)
    qc.h(1)
    qc.cx(1, 2)

    # Step 4: Bell measurement on Alice's qubits
    qc.cx(0, 1)
    qc.h(0)

    # Step 5: Get the full statevector
    state = Statevector.from_instruction(qc)

    # Define correction operators
    X2 = Operator.from_label('IIX')  # X on q2
    Z2 = Operator.from_label('IIZ')  # Z on q2

    print("Teleported state of Bob's qubit for all measurement outcomes:")

    # Simulate all 4 possible measurement outcomes for Alice
    for meas_q0 in [0, 1]:
        for meas_q1 in [0, 1]:
            corrected_state = state.copy()

            # Apply X if Alice's q1 = 1
            if meas_q1 == 1:
                corrected_state = corrected_state.evolve(X2)

            # Apply Z if Alice's q0 = 1
            if meas_q0 == 1:
                corrected_state = corrected_state.evolve(Z2)

            # Reduce to Bob's qubit
            bob_state = partial_trace(corrected_state, [0, 1])
            print(f"Alice measures q0={meas_q0}, q1={meas_q1} -> Bob's qubit state:\n{bob_state}\n")

    print("-------------------------------------")

if __name__ == "__main__":
    quantum_teleportation()
