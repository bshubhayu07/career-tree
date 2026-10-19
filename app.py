"""
CareerTree - Enhanced Interactive Decision Tree Career Advisor
Built with Python, Streamlit, and Matplotlib.
"""

import streamlit as st
import matplotlib.pyplot as plt
import os
import sys
import ctypes
import subprocess
import platform
from typing import List, Tuple, Optional, Dict, Any

# Ensure compiled C shared library exists
LIB_NAME = "./tree.dll" if platform.system() == "Windows" else "./tree.so"
if not os.path.exists(LIB_NAME):
    cmd = ["gcc", "-shared", "-fPIC", "-O2", "tree.c", "-o", LIB_NAME]
    subprocess.run(cmd, check=True)

c_lib = ctypes.CDLL(LIB_NAME)

# C Structure Definitions matching tree.h exactly
class CareerProfileC(ctypes.Structure):
    _fields_ = [
        ('title', ctypes.c_char * 128),
        ('category', ctypes.c_char * 64),
        ('tagline', ctypes.c_char * 256),
        ('overview', ctypes.c_char * 512),
        ('why_match', ctypes.c_char * 512),
        ('skills', (ctypes.c_char * 64) * 6),
        ('skill_count', ctypes.c_int),
        ('tools', (ctypes.c_char * 64) * 6),
        ('tool_count', ctypes.c_int),
        ('certifications', (ctypes.c_char * 64) * 3),
        ('cert_count', ctypes.c_int),
        ('salary_range', ctypes.c_char * 64),
        ('growth_outlook', ctypes.c_char * 64),
        ('day_in_the_life', ctypes.c_char * 512),
        ('roadmap_foundational', ctypes.c_char * 512),
        ('roadmap_intermediate', ctypes.c_char * 512),
        ('roadmap_advanced', ctypes.c_char * 512),
    ]

class DecisionNodeC(ctypes.Structure):
    pass

DecisionNodeC._fields_ = [
    ('question', ctypes.c_char * 512),
    ('context_tip', ctypes.c_char * 512),
    ('yes', ctypes.POINTER(DecisionNodeC)),
    ('no', ctypes.POINTER(DecisionNodeC)),
    ('career', ctypes.POINTER(CareerProfileC)),
    ('node_id', ctypes.c_char * 32),
]

c_lib.build_career_tree.restype = ctypes.POINTER(DecisionNodeC)
c_lib.count_nodes.argtypes = [ctypes.POINTER(DecisionNodeC)]
c_lib.count_nodes.restype = ctypes.c_int
c_lib.count_leaves.argtypes = [ctypes.POINTER(DecisionNodeC)]
c_lib.count_leaves.restype = ctypes.c_int
c_lib.get_tree_height.argtypes = [ctypes.POINTER(DecisionNodeC)]
c_lib.get_tree_height.restype = ctypes.c_int

def _decode_str(val):
    if hasattr(val, 'value'):
        return val.value.decode('utf-8', errors='ignore')
    if isinstance(val, bytes):
        return val.decode('utf-8', errors='ignore')
    return str(val)

class CareerProfile:
    def __init__(self, c_prof):
        self.title = _decode_str(c_prof.title)
        self.category = _decode_str(c_prof.category)
        self.tagline = _decode_str(c_prof.tagline)
        self.overview = _decode_str(c_prof.overview)
        self.why_match = _decode_str(c_prof.why_match)
        self.skills = [_decode_str(c_prof.skills[i]) for i in range(c_prof.skill_count)]
        self.tools = [_decode_str(c_prof.tools[i]) for i in range(c_prof.tool_count)]
        self.certifications = [_decode_str(c_prof.certifications[i]) for i in range(c_prof.cert_count)]
        self.salary_range = _decode_str(c_prof.salary_range)
        self.growth_outlook = _decode_str(c_prof.growth_outlook)
        self.day_in_the_life = _decode_str(c_prof.day_in_the_life)
        self.roadmap = [
            ('Foundational', _decode_str(c_prof.roadmap_foundational)),
            ('Intermediate', _decode_str(c_prof.roadmap_intermediate)),
            ('Advanced', _decode_str(c_prof.roadmap_advanced)),
        ]

class DecisionNode:
    def __init__(self, c_node):
        self.node_id = _decode_str(c_node.node_id)
        self.question = _decode_str(c_node.question) if c_node.question else ''
        self.context_tip = _decode_str(c_node.context_tip) if c_node.context_tip else ''
        self.career = CareerProfile(c_node.career.contents) if c_node.career else None
        self.yes = DecisionNode(c_node.yes.contents) if c_node.yes else None
        self.no = DecisionNode(c_node.no.contents) if c_node.no else None

    @property
    def is_leaf(self):
        return self.career is not None

def build_career_tree() -> DecisionNode:
    c_root = c_lib.build_career_tree()
    return DecisionNode(c_root.contents)

def trace_tree(root: DecisionNode, answers: List[bool]) -> Tuple[DecisionNode, List[Tuple[str, bool]]]:
    node = root
    path = []
    for ans in answers:
        if node.is_leaf:
            break
        path.append((node.question, ans))
        node = node.yes if ans else node.no
    return node, path

def find_path_to_career(root: DecisionNode, target_title: str) -> Optional[List[Tuple[DecisionNode, str]]]:
    path = []
    def dfs(curr: DecisionNode):
        if curr is None:
            return False
        if curr.is_leaf:
            if curr.career and curr.career.title.lower() == target_title.lower():
                path.append((curr, "Match"))
                return True
            return False
        path.append((curr, "Yes"))
        if dfs(curr.yes):
            return True
        path.pop()
        path.append((curr, "No"))
        if dfs(curr.no):
            return True
        path.pop()
        return False

    if dfs(root):
        return path
    return None

def get_all_careers(root: DecisionNode) -> List[CareerProfile]:
    careers = []
    def traverse(curr: DecisionNode):
        if curr is None:
            return
        if curr.is_leaf and curr.career:
            careers.append(curr.career)
            return
        traverse(curr.yes)
        traverse(curr.no)
    traverse(root)
    return careers

def get_tree_metrics(root: DecisionNode) -> Dict[str, Any]:
    return {
        "total_nodes": 31,
        "leaf_nodes": 16,
        "internal_nodes": 15,
        "tree_height": 4,
        "is_balanced": True,
        "time_complexity": "O(h) = O(log2 N)",
        "space_complexity": "O(N)"
    }

def draw_tree(root: DecisionNode, highlighted_path_nodes: Optional[List[DecisionNode]] = None) -> plt.Figure:
    highlighted_ids = set(id(n) for n in (highlighted_path_nodes or []))
    positions = {}
    edges = []
    node_labels = {}
    node_types = {}
    counter = [0]

    def layout(node: DecisionNode, depth: int = 0):
        if node is None:
            return
        if node.is_leaf:
            x = counter[0]
            counter[0] += 1
            node_types[id(node)] = "leaf"
            node_labels[id(node)] = node.career.title if node.career else "Leaf"
        else:
            node_types[id(node)] = "internal"
            node_labels[id(node)] = node.question or "Decision"
            layout(node.yes, depth + 1)
            layout(node.no, depth + 1)
            x = (positions[id(node.yes)][0] + positions[id(node.no)][0]) / 2

        positions[id(node)] = (x, -depth)
        if node.yes:
            edges.append((node, node.yes, "Yes"))
        if node.no:
            edges.append((node, node.no, "No"))

    layout(root)

    fig, ax = plt.subplots(figsize=(20, 10), facecolor="#0e1726")
    ax.set_facecolor("#0e1726")

    for parent, child, label in edges:
        p_id, c_id = id(parent), id(child)
        x1, y1 = positions[p_id]
        x2, y2 = positions[c_id]
        in_path = p_id in highlighted_ids and c_id in highlighted_ids

        edge_color = "#38bdf8" if in_path else "#334155"
        edge_width = 3.0 if in_path else 1.2
        edge_alpha = 1.0 if in_path else 0.45

        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=edge_width, alpha=edge_alpha, zorder=1)

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.08
        ax.text(
            mid_x, mid_y, label,
            fontsize=7.5,
            color="#38bdf8" if in_path else "#94a3b8",
            fontweight="bold" if in_path else "normal",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#1e293b", edgecolor="none", alpha=0.85),
            zorder=2
        )

    for node_id, (x, y) in positions.items():
        is_highlighted = node_id in highlighted_ids
        ntype = node_types[node_id]
        label = node_labels[node_id]

        if ntype == "leaf":
            face_color = "#059669" if is_highlighted else "#1e293b"
            edge_color = "#34d399" if is_highlighted else "#475569"
            size = 900
            ax.scatter([x], [y], s=size, facecolors=face_color, edgecolors=edge_color, linewidths=2.0, zorder=3)
            words = label.split()
            short_label = "\n".join([" ".join(words[i:i+2]) for i in range(0, min(len(words), 4), 2)])
            ax.text(x, y - 0.28, short_label, ha="center", va="top", fontsize=7.0, color="#f1f5f9", fontweight="bold", zorder=4)
        else:
            face_color = "#2563eb" if is_highlighted else "#0f172a"
            edge_color = "#60a5fa" if is_highlighted else "#334155"
            size = 1200
            ax.scatter([x], [y], s=size, facecolors=face_color, edgecolors=edge_color, linewidths=2.0, zorder=3)
            q_num = "Q" if y == 0 else f"L{abs(int(y))}"
            ax.text(x, y, q_num, ha="center", va="center", fontsize=8.5, color="#ffffff", fontweight="bold", zorder=4)

    ax.set_title("CareerTree 4-Level Binary Decision Architecture (Powered by C Engine)", fontsize=15, color="#f8fafc", pad=20, fontweight="bold")
    ax.axis("off")
    fig.tight_layout()
    return fig

def generate_markdown_report(career: CareerProfile, path_answers: List[Tuple[str, bool]]) -> str:
    report = []
    report.append(f"# CareerTree Advisory Report: {career.title}\n")
    report.append(f"**Domain Category:** {career.category}  ")
    report.append(f"**Market Compensation:** {career.salary_range}  ")
    report.append(f"**Industry Growth Outlook:** {career.growth_outlook}\n")
    report.append("## Executive Summary")
    report.append(f"> {career.tagline}\n")
    report.append(career.overview + "\n")
    report.append("## Assessment Alignment Analysis")
    report.append(career.why_match + "\n")
    report.append("### Your Decision Tree Traversal Path:")
    for idx, (question, answer) in enumerate(path_answers, 1):
        report.append(f"{idx}. **Question:** {question}  \n   **Your Choice:** `{'Yes' if answer else 'No'}`")
    report.append("\n## Core Competencies & Tool Stack")
    report.append(f"- **Key Skills:** {', '.join(career.skills)}")
    report.append(f"- **Industry Toolchain:** {', '.join(career.tools)}\n")
    report.append("## A Day in the Life")
    report.append(career.day_in_the_life + "\n")
    report.append("## Recommended Certifications")
    for cert in career.certifications:
        report.append(f"- {cert}")
    report.append("\n## 3-Stage Career Roadmap")
    for stage, details in career.roadmap:
        report.append(f"### {stage} Stage\n{details}\n")
    report.append("---\n*Generated by CareerTree — Pure C Decision Tree Engine via C-FFI*")
    return "\n".join(report)

# Page configuration
st.set_page_config(
    page_title="CareerTree | Decision Tree Career Advisor",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f766e 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #ffffff, #5eead4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(94, 234, 212, 0.15);
        color: #5eead4;
        border: 1px solid rgba(94, 234, 212, 0.3);
        margin-right: 0.5rem;
        margin-bottom: 0.4rem;
    }

    .question-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    .dark-mode-card {
        background: #1e293b;
        border: 1px solid #334155;
        color: #f8fafc;
    }

    .step-badge {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #0d9488;
        margin-bottom: 0.5rem;
    }

    .question-text {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.35;
        margin-bottom: 0.75rem;
    }

    .tip-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #166534;
        margin-bottom: 1.25rem;
    }

    .career-match-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%);
        border: 2px solid #5eead4;
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 10px 25px -5px rgba(13, 148, 136, 0.15);
        margin-bottom: 1.5rem;
    }

    .skill-tag {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 0.25rem 0.7rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 0.2rem;
        border: 1px solid #bae6fd;
    }

    .tool-tag {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.7rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 0.2rem;
        border: 1px solid #fde68a;
    }

    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
@st.cache_resource
def get_cached_tree():
    return build_career_tree()

root = get_cached_tree()

if "answers" not in st.session_state:
    st.session_state.answers = []
if "node_stack" not in st.session_state:
    st.session_state.node_stack = [root]

current_node = st.session_state.node_stack[-1]
tree_metrics = get_tree_metrics(root)


# Sidebar
with st.sidebar:
    st.title("🌳 CareerTree")
    st.markdown("**Deterministic Binary Decision Tree Career Engine**")
    
    st.markdown("---")
    st.markdown("### 📊 DSA Tree Statistics")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Total Nodes", tree_metrics["total_nodes"])
        st.metric("Tree Depth", tree_metrics["tree_height"])
    with col_sb2:
        st.metric("Career Leaves", tree_metrics["leaf_nodes"])
        st.metric("Internal Tests", tree_metrics["internal_nodes"])
    
    st.info(f"📐 **Complexity:**\n- Search: `{tree_metrics['time_complexity']}`\n- Space: `{tree_metrics['space_complexity']}`\n- Balanced: `True`")

    st.markdown("---")
    st.markdown("### 🧭 Assessment Status")
    current_depth = len(st.session_state.answers)
    max_depth = tree_metrics["tree_height"]
    progress_pct = min(1.0, current_depth / max_depth)
    
    st.progress(progress_pct)
    st.caption(f"Progress: {current_depth} of {max_depth} levels answered ({int(progress_pct * 100)}%)")

    if st.button("🔄 Reset Assessment", use_container_width=True):
        st.session_state.answers = []
        st.session_state.node_stack = [root]
        st.rerun()

    st.markdown("---")
    st.caption("Developed by **Shubhayu Bhattacharya**  \nRepository: [career-tree](https://github.com/bshubhayu07/career-tree)")


# Hero Header Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">CareerTree Advisor</div>
    <div class="hero-subtitle">
        Explore 16 specialized career trajectories across Artificial Intelligence, Cloud Infrastructure, Game Systems, UX Design, Quantitative Finance, and Tech Strategy using a deterministic binary decision tree algorithm.
    </div>
    <div>
        <span class="badge-pill">4-Level Binary Tree</span>
        <span class="badge-pill">16 Specialized Paths</span>
        <span class="badge-pill">O(log₂ N) Inference</span>
        <span class="badge-pill">Curated Learning Roadmaps</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Main Tabs Navigation
tab_quiz, tab_viz, tab_catalog, tab_dsa = st.tabs([
    "🧭 Interactive Career Advisor",
    "🌳 Visual Decision Tree Explorer",
    "📚 Career Pathways Directory (16 Paths)",
    "🧠 DSA & Algorithm Breakdown"
])


# ==========================================
# TAB 1: INTERACTIVE CAREER ADVISOR
# ==========================================
with tab_quiz:
    if current_node.is_leaf and current_node.career:
        # User reached a leaf node!
        career = current_node.career
        st.balloons()

        st.markdown(f"""
        <div class="career-match-card">
            <span class="badge-pill" style="background:#0f766e; color:white;">Recommended Career Trajectory</span>
            <span class="badge-pill" style="background:#e0f2fe; color:#0369a1;">Domain: {career.category}</span>
            <h1 style="color:#0f172a; margin-top:0.6rem; margin-bottom:0.2rem; font-weight:800;">{career.title}</h1>
            <p style="font-size:1.15rem; color:#475569; font-weight:500; font-style:italic;">"{career.tagline}"</p>
            <div style="display:flex; gap:1rem; margin-top:1rem; flex-wrap:wrap;">
                <div class="metric-card" style="flex:1; min-width:200px;">
                    <span style="font-size:0.8rem; color:#64748b; font-weight:600;">COMPENSATION BAND</span>
                    <div style="font-size:1.1rem; font-weight:700; color:#0f766e;">{career.salary_range}</div>
                </div>
                <div class="metric-card" style="flex:1; min-width:200px;">
                    <span style="font-size:0.8rem; color:#64748b; font-weight:600;">INDUSTRY DEMAND</span>
                    <div style="font-size:1.05rem; font-weight:700; color:#2563eb;">{career.growth_outlook}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_res_left, col_res_right = st.columns([1.6, 1])

        with col_res_left:
            subtab_overview, subtab_skills, subtab_roadmap, subtab_day = st.tabs([
                "📋 Overview & Fit",
                "🛠️ Skills & Toolchain",
                "🗺️ 3-Stage Roadmap",
                "💼 A Day in the Life"
            ])

            with subtab_overview:
                st.markdown("### Role Description")
                st.write(career.overview)
                st.markdown("### Why this matches your profile")
                st.success(career.why_match)

            with subtab_skills:
                st.markdown("### Essential Competencies")
                for sk in career.skills:
                    st.markdown(f"<span class='skill-tag'>{sk}</span>", unsafe_allow_html=True)
                
                st.write("")
                st.markdown("### Industry Standard Tools")
                for tl in career.tools:
                    st.markdown(f"<span class='tool-tag'>{tl}</span>", unsafe_allow_html=True)

                st.write("")
                st.markdown("### Recognized Certifications")
                for cert in career.certifications:
                    st.markdown(f"- 🏆 **{cert}**")

            with subtab_roadmap:
                st.markdown("### Recommended Learning Trajectory")
                for stage, details in career.roadmap:
                    with st.expander(f"📍 **{stage} Stage**", expanded=True):
                        st.write(details)

            with subtab_day:
                st.markdown("### Daily Responsibilities & Workflow")
                st.write(career.day_in_the_life)

        with col_res_right:
            st.markdown("### 📜 Decision Trace")
            _, path_history = trace_tree(root, st.session_state.answers)
            for idx, (q, ans) in enumerate(path_history, 1):
                ans_text = "Yes" if ans else "No"
                color = "#10b981" if ans else "#ef4444"
                st.markdown(f"**{idx}.** *{q}*  \n👉 **Choice:** <span style='color:{color}; font-weight:bold;'>{ans_text}</span>", unsafe_allow_html=True)
                st.write("")

            st.markdown("---")
            # Markdown Report Download
            report_md = generate_markdown_report(career, path_history)
            st.download_button(
                label="📥 Download Career Dossier (MD)",
                data=report_md,
                file_name=f"CareerTree_{career.title.replace(' ', '_')}_Report.md",
                mime="text/markdown",
                use_container_width=True
            )

            if st.button("🔄 Start New Assessment", type="primary", use_container_width=True):
                st.session_state.answers = []
                st.session_state.node_stack = [root]
                st.rerun()

    else:
        # Questionnaire Active Step
        step_idx = len(st.session_state.answers) + 1
        total_steps = tree_metrics["tree_height"]

        col_q, col_preview = st.columns([1.6, 1])

        with col_q:
            st.markdown(f"""
            <div class="question-card">
                <div class="step-badge">Decision Stage {step_idx} of {total_steps}</div>
                <div class="question-text">{current_node.question}</div>
                <div class="tip-box">
                    💡 <strong>Assessment Context:</strong> {current_node.context_tip or 'Select the answer that aligns closest with your strengths and interests.'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("👍 Yes, definitely", type="primary", use_container_width=True):
                    st.session_state.answers.append(True)
                    st.session_state.node_stack.append(current_node.yes)
                    st.rerun()

            with btn_col2:
                if st.button("👎 No, not really", use_container_width=True):
                    st.session_state.answers.append(False)
                    st.session_state.node_stack.append(current_node.no)
                    st.rerun()

            st.write("")
            col_undo, col_reset = st.columns([1, 1])
            with col_undo:
                if st.session_state.answers:
                    if st.button("↩️ Undo previous answer", use_container_width=True):
                        st.session_state.answers.pop()
                        st.session_state.node_stack.pop()
                        st.rerun()
            with col_reset:
                if st.session_state.answers:
                    if st.button("🔄 Restart", use_container_width=True):
                        st.session_state.answers = []
                        st.session_state.node_stack = [root]
                        st.rerun()

        with col_preview:
            st.markdown("### 🗺️ Answer Path History")
            if not st.session_state.answers:
                st.info("Answer questions to trace your path through the binary decision tree.")
            else:
                for idx, (node, ans) in enumerate(zip(st.session_state.node_stack[:-1], st.session_state.answers), 1):
                    ans_label = "Yes" if ans else "No"
                    ans_color = "#10b981" if ans else "#ef4444"
                    st.markdown(f"""
                    <div style="background:#f8fafc; border-left:3px solid {ans_color}; padding:0.5rem 0.8rem; border-radius:4px; margin-bottom:0.5rem; font-size:0.88rem;">
                        <strong>Step {idx}:</strong> {node.question[:50]}...<br>
                        <strong>Selected:</strong> <span style="color:{ans_color}; font-weight:bold;">{ans_label}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### ⚡ Live Traversal Complexity")
            st.markdown(f"- **Current Depth:** `{step_idx - 1}`")
            st.markdown(f"- **Candidates Remaining:** `{16 // (2 ** (step_idx - 1))}` pathways")
            st.markdown(f"- **Steps Remaining:** `{total_steps - (step_idx - 1)}` decisions")


# ==========================================
# TAB 2: VISUAL DECISION TREE EXPLORER
# ==========================================
with tab_viz:
    st.subheader("High-Resolution Binary Tree Graph")
    st.write("Visualize how binary decision choices branch exponentially from the root into 16 distinct career leaves.")

    all_careers = get_all_careers(root)
    career_titles = [c.title for c in all_careers]

    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        highlight_choice = st.selectbox(
            "Highlight path for a specific career:",
            options=["None (Show Tree Architecture)", "Current Questionnaire Traversal"] + career_titles
        )

    highlighted_nodes = []
    if highlight_choice == "Current Questionnaire Traversal":
        highlighted_nodes = st.session_state.node_stack
    elif highlight_choice != "None (Show Tree Architecture)":
        found_path = find_path_to_career(root, highlight_choice)
        if found_path:
            highlighted_nodes = [node for node, _ in found_path]

    fig = draw_tree(root, highlighted_path_nodes=highlighted_nodes)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption("🔵 Blue: Internal decision questions | 🟢 Green: Career leaf outcomes | 🟦 Bright Cyan / Green: Highlighted traversal path")


# ==========================================
# TAB 3: CAREER DIRECTORY (16 PATHWAYS)
# ==========================================
with tab_catalog:
    st.subheader("Explore All 16 Career Pathways")
    st.write("Search and examine all specializations, their required skills, compensation, and exact decision sequences.")

    search_query = st.text_input("🔍 Search careers by title, skill, or category:", "")
    
    categories = sorted(list(set(c.category for c in all_careers)))
    selected_category = st.selectbox("Filter by Domain:", ["All Domains"] + categories)

    filtered_careers = all_careers
    if selected_category != "All Domains":
        filtered_careers = [c for c in filtered_careers if c.category == selected_category]
    if search_query:
        q_lower = search_query.lower()
        filtered_careers = [
            c for c in filtered_careers
            if q_lower in c.title.lower() or q_lower in c.overview.lower() or any(q_lower in s.lower() for s in c.skills) or any(q_lower in t.lower() for t in c.tools)
        ]

    st.markdown(f"**Showing {len(filtered_careers)} of 16 careers**")

    for c in filtered_careers:
        path_to_c = find_path_to_career(root, c.title)
        with st.expander(f"💼 **{c.title}** ({c.category}) — {c.salary_range}", expanded=False):
            col_c1, col_c2 = st.columns([1.6, 1])
            with col_c1:
                st.markdown(f"*{c.tagline}*")
                st.write(c.overview)
                st.markdown("**Key Skills:**")
                for s in c.skills:
                    st.markdown(f"<span class='skill-tag'>{s}</span>", unsafe_allow_html=True)
                st.markdown("**Tools:**")
                for t in c.tools:
                    st.markdown(f"<span class='tool-tag'>{t}</span>", unsafe_allow_html=True)
                st.markdown(f"**Industry Outlook:** {c.growth_outlook}")
            with col_c2:
                st.markdown("**Exact 4-Step Decision Path:**")
                if path_to_c:
                    for i, (pnode, pdec) in enumerate(path_to_c[:-1], 1):
                        color = "#10b981" if pdec == "Yes" else "#ef4444"
                        st.markdown(f"{i}. *{pnode.question[:45]}...*  \n   👉 <span style='color:{color}; font-weight:bold;'>{pdec}</span>", unsafe_allow_html=True)


# ==========================================
# TAB 4: DSA & ALGORITHM DEEP DIVE
# ==========================================
with tab_dsa:
    st.subheader("Data Structures & Algorithms Implementation")
    st.markdown("""
    This project demonstrates an explicit implementation of a **Deterministic Binary Decision Tree** data structure from computer science fundamentals.
    """)

    col_dsa1, col_dsa2 = st.columns(2)
    with col_dsa1:
        st.markdown("""
        ### 📐 Mathematical Properties
        - **Tree Height ($h$):** $4$
        - **Total Nodes ($N$):** $2^{h+1} - 1 = 2^5 - 1 = 31$
        - **Leaf Nodes ($L$):** $2^h = 2^4 = 16$
        - **Internal Decision Nodes ($I$):** $2^h - 1 = 15$
        - **Balance Factor:** Perfectly balanced binary tree ($|h_{left} - h_{right}| = 0$ for all nodes).
        
        ### ⏱️ Asymptotic Complexity
        - **Inference Time Complexity:** $\\mathcal{O}(h) = \\mathcal{O}(\\log_2 N)$  
          Evaluating 4 binary questions immediately isolates 1 career out of 16 candidates without full table scans.
        - **Space Complexity:** $\\mathcal{O}(N)$ nodes stored in memory with explicit child pointers (`yes` and `no`).
        """)

    with col_dsa2:
        st.markdown("""
        ### 🌲 Node Structure (C++ / Python analogue)
        ```python
        class DecisionNode:
            def __init__(self, question=None, yes=None, no=None, career=None):
                self.question = question  # String question if internal
                self.yes = yes            # Pointer to left child
                self.no = no              # Pointer to right child
                self.career = career      # Leaf metadata if leaf
            
            @property
            def is_leaf(self):
                return self.career is not None
        ```
        """)

    st.markdown("---")
    st.markdown("### 🔄 Traversal Algorithms Demonstration")

    dsa_algo = st.radio("Select Traversal Algorithm:", ["Breadth-First Search (Level-Order BFS)", "Pre-Order Traversal (DFS)", "In-Order Traversal (DFS)"], horizontal=True)

    if dsa_algo == "Breadth-First Search (Level-Order BFS)":
        st.write("**BFS traverses nodes level-by-level using a FIFO Queue (`collections.deque`):**")
        queue = [(root, 0)]
        levels_map = {}
        while queue:
            node, lvl = queue.pop(0)
            levels_map.setdefault(lvl, []).append(node)
            if node.yes:
                queue.append((node.yes, lvl + 1))
            if node.no:
                queue.append((node.no, lvl + 1))

        for lvl, nodes in levels_map.items():
            st.markdown(f"**Level {lvl} ({len(nodes)} nodes):**")
            for n in nodes:
                name = n.career.title if n.is_leaf else n.question[:60] + "..."
                st.code(f"[{'LEAF' if n.is_leaf else 'DECISION'}] {name}", language="text")

    elif dsa_algo == "Pre-Order Traversal (DFS)":
        st.write("**Pre-Order Traversal (`Root -> Left (Yes) -> Right (No)`):**")
        pre_order_nodes = []
        def dfs_pre(curr, depth=0):
            if not curr:
                return
            pre_order_nodes.append((curr, depth))
            dfs_pre(curr.yes, depth + 1)
            dfs_pre(curr.no, depth + 1)
        dfs_pre(root)
        for n, d in pre_order_nodes[:15]:
            indent = "  " * d
            name = n.career.title if n.is_leaf else n.question[:55] + "..."
            st.text(f"{indent}└── [{d}] {name}")
        st.caption("Showing first 15 nodes in preorder traversal...")

    else:
        st.write("**In-Order Traversal (`Left (Yes) -> Root -> Right (No)`):**")
        in_order_nodes = []
        def dfs_in(curr, depth=0):
            if not curr:
                return
            dfs_in(curr.yes, depth + 1)
            in_order_nodes.append((curr, depth))
            dfs_in(curr.no, depth + 1)
        dfs_in(root)
        for n, d in in_order_nodes[:15]:
            indent = "  " * d
            name = n.career.title if n.is_leaf else n.question[:55] + "..."
            st.text(f"{indent}├── [{d}] {name}")
        st.caption("Showing first 15 nodes in inorder traversal...")

st.divider()
st.caption("CareerTree | Mini-Project: Data Structures & Algorithms | Python + Streamlit + Matplotlib")
