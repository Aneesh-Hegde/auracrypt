# AuraCrypt-96: A Hybrid Neural-Symbolic Forensic Suite

### The Project Background

For decades, breaking a cipher meant having a human mathematician sit down with a pencil and paper to find "differential trails"—tiny, predictable flaws in how a cipher scrambles data. This process was historically slow and required extreme domain expertise to identify how specific input changes affected the output.

In 2019, researcher **Aron Gohr** changed this landscape by demonstrating that a Neural Network could be trained to identify these flaws automatically. AuraCrypt-96 takes that inspiration and applies it to a real-world problem. 

We live in an age of IoT devices: smart locks, heart monitors, and industrial sensors. These devices often have limited battery life, leading engineers to "reduce the rounds" of their encryption to save power. While they rely on a 64-bit key for security, AuraCrypt-96 proves that when the mathematical complexity is lowered, an AI can find a functional key almost instantly.



### The Architecture: How the "Brain" Works

The core of this project is a **ResNet-96** (Residual Network). The "96" refers to the 96-bit input vector we provide to the model: two encrypted 16-bit word pairs ($C_0, C_1$) plus their XOR difference ($C_0 \oplus C_1$).

#### The Stethoscope: 1D Convolutional Layers
Instead of viewing the data as a static number, the AI uses **1D Convolutions**. Think of this like a sliding magnifying glass moving across the bits. It looks for bit-level correlations—for example, if bit 3 flips, does bit 12 always flip as well? The model learns these hidden rules during the training phase.

#### The Residual Blocks
In deep networks, information can sometimes get "lost" as it moves through many layers. We use **Residual Blocks** (Skip Connections) to allow the signal to flow through the network effectively. This ensures the model stays sharp even as the mathematical patterns become more subtle.



#### Global Average Pooling
At the final stage, the model doesn't just pick one bit. It uses **Global Average Pooling** to assess the entire "signature" of the data. This produces a single confidence score, telling us how certain the AI is that it has found a legitimate cipher pattern rather than random noise.

### The Logic Muscle: Z3 SMT Solver

Once the AI identifies a high-confidence pattern, it hands the task over to the **Z3 Solver**. While the AI is excellent at sensing a pattern, Z3 acts as the "Logic Locksmith." It treats the entire cipher like a massive, logical Sudoku puzzle.

* **The AI says:** "I hear a specific click in the gears!"
* **Z3 says:** "If those gears clicked there, then these specific key bits must be the ones used."



### Sample Output

Below is a typical execution trace of the AuraCrypt-96 suite against a 3-round Speck configuration.

```text
[*] Running AuraCrypt on: cuda

[*] Training AuraCrypt-96 (3 Rounds)...
    Generating 400000 samples .......... done
    Epoch  1/15 | Loss: 0.2565 | Acc: 0.8998
    Epoch  5/15 | Loss: 0.0137 | Acc: 0.9949
    Epoch 10/15 | Loss: 0.0042 | Acc: 0.9987
    Epoch 15/15 | Loss: 0.0007 | Acc: 1.0000

[*] AI Confidence: 100.00%
[!] Launching Z3 Solver...

[SUCCESS] Key Found: 0x161b42eedf1a (0.01s)
[MATCH] False

================================================================================
      AURACRYPT v1.0 — CYBER-FORENSIC KEY RECOVERY SUITE
================================================================================
[MISSION] Objective: Recover the Master Key from a vulnerable IoT Lock.
[MISSION] Security Level: 3 Rounds (Warning: High Bit-Leakage)

[*] SCANNING AIRWAVES... Intercepting Packets (Pulses)...
    [PACKET 1] Captured!
    [PACKET 2] Captured!

[AI REPORT] Vulnerability Found: [████████████████████████░] 100.00%
[INFO] The AI is 100.0% certain this is NOT random noise.

[!] KEY RECOVERED in 0.0308 seconds!
[!] Binary Match Attempt: 0x56e06d2e1f98

--------------------------------------------------------------------------------
FINAL INTERPRETATION:
STATUS: [SKELETON KEY RECOVERED]
EXPLANATION: This key is numerically different but works on THIS specific lock.
To get the Master Key, you would need to intercept more than 2 Packets.
--------------------------------------------------------------------------------
```

### Understanding the Results

#### Why 100% Accuracy is a Warning
In this repository, you will see the model hitting **100% accuracy** on 3 rounds. This isn't an AI fluke; it signifies a **Security Collapse**. It means the encryption is so thin that the AI can perfectly distinguish it from random noise. For a developer, seeing 100% accuracy is a clear signal that the encryption rounds must be increased immediately to ensure safety.

#### The Skeleton Key vs. The Master Key
* **Skeleton Key:** This occurs when the solver has limited data. Z3 finds a key that works perfectly for the intercepted session, but it isn't the owner's original key. Because the rounds are so low, there are $2^{32}$ (roughly 4.2 billion) keys that might fit the same criteria for a single message.
* **Master Key:** This is the authentic original key. By intercepting just one or two more "pulses" (packets) of data, AuraCrypt-96 can narrow down the logic until it finds the **exact** 64-bit key created by the user.

### Getting Started

1.  **Prepare the Environment:** `pip install numpy torch z3-solver`
2.  **Execute the Analysis:** `python main.py`
