
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def superdense_coding(bits_to_send):
    """
    Simulates the superdense coding protocol.
    
    Args:
        bits_to_send (list of 2 ints): The classical bits Alice wants to send, e.g., [1, 0].
    
    Transmits two classical bits using one qubit via a shared entangled pair.
    """
    if len(bits_to_send) != 2 or any(b not in [0, 1] for b in bits_to_send):
        raise ValueError("bits_to_send must be a list of two bits (0 or 1).")

    print("--- Running Superdense Coding ---")
    print(f"Alice wants to send the classical bits: {bits_to_send}")

    # Create a 2-qubit circuit with 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Step 1: Alice and Bob share an entangled Bell pair
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # Step 2: Alice encodes her bits
    # bits_to_send[0] = MSB → X gate
    # bits_to_send[1] = LSB → Z gate
    if bits_to_send[0] == 1:
        qc.x(0)
    if bits_to_send[1] == 1:
        qc.z(0)
    qc.barrier()

    # Step 3: Bob decodes using Bell measurement
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # Step 4: Measure both qubits
    qc.measure(0, 0)  # Alice's qubit -> classical bit 0
    qc.measure(1, 1)  # Bob's qubit -> classical bit 1

    # Run simulation
    backend = AerSimulator()
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1).result()
    counts = result.get_counts()

    # Extract measured bits
    measured_bits_str = list(counts.keys())[0]
    measured_bits = [int(measured_bits_str[0]), int(measured_bits_str[1])]
    print(f"Bob receives the classical bits: {measured_bits}")

    if bits_to_send == measured_bits:
        print("✅ Superdense coding successful!")
    else:
        print("❌ Superdense coding failed.")
    print("-------------------------------------")


if __name__ == "__main__":
    # Test all possible 2-bit messages
    test_messages = [[0,0], [0,1], [1,0], [1,1]]
    for msg in test_messages:
        superdense_coding(msg)
