# pip install qiskit qiskit-aer

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def chsh_game(shots_per_trial=10000, draw=False):
    """
    Simulates the CHSH game using quantum strategy.
    Quantum winning probability should approach ~0.8536.
    """
    print("--- Running CHSH Game ---")
    
    winning_count = 0
    backend = AerSimulator()
    
    # Alice and Bob's input settings
    settings = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    # Pre-generate random inputs for all shots
    inputs = [settings[np.random.randint(0, 4)] for _ in range(shots_per_trial)]
    
    # Loop over each input pair
    for x, y in inputs:
        qc = QuantumCircuit(2, 2)
        
        # 1) Create Bell pair
        qc.h(0)
        qc.cx(0, 1)
        
        # 2) Apply measurement rotations based on inputs
        if x == 1:
            qc.ry(-np.pi/4, 0)
        if y == 1:
            qc.ry(-np.pi/2, 1)
        
        # 3) Measure qubits
        qc.measure(0, 0)
        qc.measure(1, 1)
        
        # Run simulation (1 shot per input)
        tqc = transpile(qc, backend)
        result = backend.run(tqc, shots=1).result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]
        
        # Extract Alice and Bob results
        a, b = int(outcome[1]), int(outcome[0])
        
        # Winning condition: a XOR b == x AND y
        if (a ^ b) == (x * y):
            winning_count += 1
    
    win_probability = winning_count / shots_per_trial
    
    print(f"Classical winning probability limit: 0.75")
    print(f"Quantum winning probability (ideal): ~0.8536")
    print(f"Simulated quantum winning probability: {win_probability:.4f}")
    print("-------------------------------------")


if __name__ == "__main__":
    chsh_game(shots_per_trial=600)
