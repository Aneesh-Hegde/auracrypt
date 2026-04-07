# Contributing to AuraCrypt-96

First, thank you for taking the time to contribute to this project. AuraCrypt-96 is a specialized tool for hybrid neural-symbolic cryptanalysis, and community contributions are vital for expanding its capabilities to new ciphers and models.

---

## Code of Conduct

By participating in this project, you agree to maintain a professional and respectful environment. Please ensure that all communication is constructive and focused on the technical advancement of the framework.

---

## How to Contribute

### Reporting Bugs
If you find a bug in the cipher implementation, the neural network training loop, or the Z3 solver logic:
1. Open an issue on GitHub.
2. Provide a clear description of the problem.
3. Include steps to reproduce the bug, along with your environment details (Python version, PyTorch version, CUDA status).

### Feature Requests
We are always looking to expand AuraCrypt. If you have ideas for the following, please open a feature request:
* Support for new lightweight ciphers (e.g., Simon, Lea, Simeck).
* Alternative neural architectures (e.g., Transformers or LSTMs for bit-sequence analysis).
* Optimizations for the Z3 SMT solver logic.

### Pull Requests
1. Fork the repository and create your branch from `main`.
2. Ensure your code follows PEP 8 standards.
3. If you are adding a new cipher, include the mathematical reference for the implementation.
4. Run the training loop to ensure your changes do not break the 96-bit feature engineering logic.
5. Submit your pull request with a detailed description of the changes.

---

## Development Workflow

To set up a development environment:

1. Clone your fork:
   `git clone https://github.com/your-username/auracrypt.git`
2. Create a virtual environment:
   `python -m venv venv`
3. Activate the environment:
   * Windows: `venv\Scripts\activate`
   * macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   `pip install -r requirements.txt`

---

## Research and Cryptanalysis Guidelines

AuraCrypt-96 is a research-oriented tool. If you are contributing new cryptanalytic findings (e.g., higher round counts or new differential trails):

* **Documentation:** Explain the mathematical basis for the new differential.
* **Verification:** Provide sample outputs showing the AI Distinguisher's accuracy and the Solver's recovery time.
* **Modularity:** Keep cipher implementations in `speck.py` (or a new cipher-specific file) and keep the solver logic in `solver.py`.

---

## Licensing

By contributing to AuraCrypt-96, you agree that your contributions will be licensed under the project's existing license.

---

### Commit Message Guidelines

To keep the history clean, please use descriptive commit messages. Examples:
* `feat: add support for Simeck32/64`
* `fix: resolve bit-vector overflow in Z3 solver`
* `docs: update README with new round-reduced findings`

