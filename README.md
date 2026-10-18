# 🌳 CareerTree — Interactive Binary Decision Tree Career Advisor

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557c.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**CareerTree** is an interactive, educational career recommendation platform built on a deterministic **Binary Decision Tree** data structure from fundamental computer science principles. Rather than relying on opaque black-box machine learning models, CareerTree uses explicit node hierarchies, binary question branches (`yes`/`no`), and recursive traversal algorithms to guide users to tailored tech careers with full mathematical transparency.

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
- **📊 Interactive Tree Visualization:** High-resolution graph rendered with Matplotlib displaying the entire binary tree, with real-time path highlighting for user traversals or selected careers.
- **⚡ Asymptotic Efficiency:** Fast $\mathcal{O}(h) = \mathcal{O}(\log_2 N)$ decision inference time complexity ($h = 4$).
- **💼 Rich Career Profiles:** Every leaf includes category tags, match rationales, skill matrices, industry toolchains, salary compensation bands, market growth forecasts, certifications, and realistic workday descriptions.
- **🗺️ 3-Stage Learning Roadmaps:** Structured learning paths from *Foundational* to *Intermediate* and *Advanced* for every role.
- **📥 One-Click Career Dossier Export:** Download customized assessment reports in clean Markdown format.
- **📚 Searchable Career Catalog:** Filter and search all 16 pathways by domain, tools, and required decision paths.
- **🧠 Educational DSA Explorer:** Live interactive demonstration of tree traversal algorithms (**BFS Level-Order**, **Pre-Order DFS**, and **In-Order DFS**).

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

### Prerequisites
- Python **3.10** or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/bshubhayu07/career-tree.git
cd career-tree
```

### 2. Create and Activate Virtual Environment (Optional, Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests

Run the automated test suite verifying node counts, balance, paths, and traversals:

```bash
python test_tree.py
```

Output:
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

---

## 📁 Project Structure

```text
career-tree/
├── app.py                     # Streamlit frontend & interactive dashboard
├── tree.py                    # Binary decision tree algorithms, nodes, & career profiles
├── test_tree.py               # Unit tests verifying tree properties & all 16 paths
├── requirements.txt           # Python dependencies
├── .gitignore                 # Standard Python/Streamlit gitignore
├── README.md                  # Detailed documentation
├── Mini_Project_Report.docx   # Academic project report
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
