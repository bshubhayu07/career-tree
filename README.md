# 🌳 CareerTree — Binary Decision Tree Career Advisor (Pure C Engine + Streamlit GUI)

[![C99](https://img.shields.io/badge/C-C99-00599C.svg?logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C99)
[![GCC](https://img.shields.io/badge/GCC-15.2%2B-brightgreen.svg)](https://gcc.gnu.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**CareerTree** is a high-performance, deterministic career recommendation system implemented in pure **C (C99)** using fundamental **Binary Decision Tree** data structures. Rather than relying on opaque black-box machine learning models, CareerTree uses explicit heap-allocated pointer hierarchies, binary question branches (`yes`/`no`), LIFO undo stacks, linked FIFO queues, and recursive traversal algorithms to guide users to tailored tech careers with full mathematical and algorithmic transparency.

---

## 🌟 Key Features

- **🌲 4-Level Binary Decision Tree:** Evaluates user affinities through a structured sequence of 4 binary choices, branching through 15 internal decision nodes into **16 specialized career trajectories**.
- **🎯 16 High-Impact Tech Career Pathways:**
  - *Cybersecurity Analyst & Ethical Hacker*
  - *Cloud Solutions Architect & DevOps Engineer*
  - *Game Developer & Real-Time 3D Engineer*
  - *Full Stack Software Engineer*
  - *Machine Learning Operations (MLOps) Engineer*
  - *AI & Deep Learning Research Scientist*
  - *Quantitative Analyst (Quant) & Financial Modeler*
  - *Data Scientist & Business Intelligence Lead*
  - *UX Researcher & Usability Specialist*
  - *UI / Visual Design & Design Systems Architect*
  - *XR / Spatial Computing & AR/VR Experience Designer*
  - *Digital Brand & Motion Graphics Art Director*
  - *Technology Strategy & Management Consultant*
  - *Technical Product Manager (TPM)*
  - *Developer Relations (DevRel) & Technical Advocate*
  - *EdTech Instructional Designer & Learning Specialist*
- **📊 ASCII Structural Tree Map & Visualizer:** Terminal-rendered tree visualizer displaying the full binary tree structure with branch paths and node indices.
- **⚡ Asymptotic Efficiency:** Ultra-fast $\mathcal{O}(h) = \mathcal{O}(\log_2 N)$ decision inference time complexity ($h = 4$).
- **💼 Rich Career Profiles:** Every leaf includes category tags, match rationales, skill matrices, industry toolchains, salary compensation bands, market growth forecasts, certifications, and realistic workday descriptions.
- **🗺️ 3-Stage Learning Roadmaps:** Structured learning paths from *Foundational* to *Intermediate* and *Advanced* for every role.
- **📥 One-Click Career Dossier Export:** Export full customized career assessment reports directly to text file (`career_recommendation.txt`).
- **↩️ LIFO Interactive Undo Stack:** Step backward to modify any decision choice during traversal without restarting the session.
- **🧠 Educational DSA Explorer:** Live interactive demonstration of tree traversal algorithms (**BFS Level-Order via Linked Queue**, **Pre-Order DFS**, and **In-Order DFS**).

---

## 📐 Data Structures & Algorithms (DSA) Architecture

### Binary Tree Mathematical Properties
- **Tree Depth / Height ($h$):** $4$
- **Total Nodes ($N$):** $2^{h+1} - 1 = 2^5 - 1 = 31$
- **Internal Decision Nodes ($I$):** $2^h - 1 = 15$
- **Leaf Nodes ($L$):** $2^h = 16$
- **Balance Factor:** Perfectly balanced binary tree ($|h_{\text{left}} - h_{\text{right}}| = 0$ for all nodes).

### Complexity Analysis
| Operation | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **Questionnaire Traversal** | $\mathcal{O}(h) = \mathcal{O}(\log_2 N)$ | $\mathcal{O}(h)$ call stack / session history |
| **Full Tree Building** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ memory allocation |
| **Path Search (DFS)** | $\mathcal{O}(N)$ worst-case | $\mathcal{O}(h)$ recursive depth |
| **Tree Traversal (BFS / DFS)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ auxiliary queue / stack |

---

## 🏗️ Decision Tree Hierarchy

```text
Level 1: Root Decision (Technical/Systems vs Creative/Human-Centric)
├── [YES] Level 2: Technical Focus (Software/Systems vs Data/AI)
│   ├── [YES] Level 3: Infrastructure/Backend vs Interactive Applications
│   │   ├── [YES] Level 4: Security vs Cloud DevOps
│   │   │   ├── [YES] Cybersecurity Analyst & Ethical Hacker
│   │   │   └── [NO]  Cloud Solutions Architect & DevOps Engineer
│   │   └── [NO] Level 4: Game 3D Tech vs Full Stack Web/Mobile
│   │       ├── [YES] Game Developer & Real-Time 3D Engineer
│   │       └── [NO]  Full Stack Software Engineer
│   └── [NO] Level 3: Frontier Deep Learning vs Applied Analytics/Quant
│       ├── [YES] Level 4: MLOps Production vs Algorithmic AI Research
│       │   ├── [YES] Machine Learning Operations (MLOps) Engineer
│       │   └── [NO]  AI & Deep Learning Research Scientist
│       └── [NO] Level 4: Quant Finance vs Data Science / BI
│           ├── [YES] Quantitative Analyst (Quant) & Financial Modeler
│           └── [NO]  Data Scientist & Business Intelligence Lead
└── [NO] Level 2: Creative & Human-Centric (Visual/Spatial vs Strategy/People)
    ├── [YES] Level 3: Interface Psychology vs Creative Media & XR
    │   ├── [YES] Level 4: Qualitative UX Research vs UI Design Systems
    │   │   ├── [YES] UX Researcher & Usability Specialist
    │   │   └── [NO]  UI / Visual Design & Design Systems Architect
    │   └── [NO] Level 4: Spatial Computing AR/VR vs Motion Graphics/Branding
    │       ├── [YES] XR / Spatial Computing & AR/VR Experience Designer
    │       └── [NO]  Digital Brand & Motion Graphics Art Director
    └── [NO] Level 3: Product Strategy vs Community/Education
        ├── [YES] Level 4: Enterprise Strategy Consulting vs Technical Product Management
        │   ├── [YES] Technology Strategy & Management Consultant
        │   └── [NO]  Technical Product Manager (TPM)
        └── [NO] Level 4: Developer Relations vs EdTech Curriculum
            ├── [YES] Developer Relations (DevRel) & Technical Advocate
            └── [NO]  EdTech Instructional Designer & Learning Specialist
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/bshubhayu07/career-tree.git
cd career-tree
```

### 🌐 Quickstart: Launching the Streamlit Web Application

To straight up start the modern interactive web application:

1. **Install Frontend Dependencies:**
   ```bash
   pip install streamlit matplotlib
   ```

2. **Launch the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

> [!NOTE]
> **Pure C Backend Under the Hood:** `app.py` automatically compiles `tree.c` into a native shared library (`tree.dll` on Windows / `tree.so` on Linux) using GCC and connects via **C Foreign Function Interface (`ctypes`)**. Every node, pointer dereference, and tree structure is executed in native C machine code!

Your browser will automatically open at `http://localhost:8501`.

---

### 🖥️ Alternative: Running the Pure C Terminal CLI

If you want to run the native C terminal program directly with zero Python dependencies:

1. **Compile with GCC:**
   ```bash
   gcc -Wall -Wextra -O2 -std=c99 main.c tree.c -o career_tree.exe
   # Or simply: make
   ```

2. **Launch the Executable:**
   ```bash
   # Windows
   .\career_tree.exe

   # Linux / macOS
   ./career_tree.exe
   ```

**CLI Interactive Capabilities:**
- `[1]` **Interactive Career Assessment:** Step-by-step decision traversal with an active LIFO Undo stack.
- `[2]` **ASCII Tree Hierarchy Visualizer:** Complete visual blueprint of all 31 nodes and binary branch trajectories.
- `[3]` **Career Pathway Finder:** DFS backtracking path tracer across all 16 career leaf nodes.
- `[4]` **DSA Traversal Engine:** Live BFS (FIFO linked queue) and DFS (recursive / stack) traversals.
- `[5]` **Automated Unit Test Suite:** In-memory validation of invariants, balance factor, leaf counts, and memory cleanliness.
- `[6]` **Export Career Dossier:** Exports the completed assessment report and metrics to `career_recommendation.txt`.
- `[0]` **Exit & Clean Shutdown:** Safely triggers `free_tree(root)` to free heap allocations with 0 memory leaks.

---

## 🧪 Running Unit Tests

Run the integrated automated C test suite verifying node counts, tree balance, leaf heights, and BFS/DFS queue invariants:

```bash
# Via Makefile
make test

# Or run the executable directly and choose Option 5
.\career_tree.exe
```

**Expected Test Output:**
```text
=== RUNNING SYSTEM UNIT TESTS ===
[TEST 1] Verifying 31 Total Nodes & Perfect Balance... [PASS] (31 nodes, h=4)
[TEST 2] Verifying 16 Distinct Leaf Nodes at Depth 4... [PASS] (16 leaves)
[TEST 3] Verifying DFS Backtracking Path Search for All 16 Paths... [PASS] (16/16 verified)
[TEST 4] Verifying BFS FIFO Queue Memory Invariants... [PASS] (Queue empty, 0 leaks)
ALL UNIT TESTS PASSED IN 0.000 SECONDS!
```

---

## 📁 Project Structure

```text
career-tree/
├── main.c                     # Interactive C CLI interface, LIFO undo stack, & unit tests
├── tree.c                     # Pure C binary tree implementation, BFS/DFS, & memory management
├── tree.h                     # C data structures (DecisionNode, CareerProfile, NodeStack, Queue)
├── Makefile                   # GCC build automation (all, clean, test)
├── .gitignore                 # Git ignore rules for C binaries and build artifacts
├── README.md                  # Comprehensive documentation
├── Mini_Project_Report.docx   # Academic mini-project report
├── CareerTree_Project_Overview.pdf # 5-Page system overview & architecture document
└── screenshots/               # Application UI previews
```

---

## 👥 Author

- **Shubhayu Bhattacharya**
- GitHub: [@bshubhayu07](https://github.com/bshubhayu07)
- Repository: [bshubhayu07/career-tree](https://github.com/bshubhayu07/career-tree)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
