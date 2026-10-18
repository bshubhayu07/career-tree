"""
CareerTree - Enhanced Interactive Decision Tree Career Advisor
Built with Python, Streamlit, and Matplotlib.
"""

import streamlit as st
import matplotlib.pyplot as plt
from tree import (
    build_career_tree,
    trace_tree,
    find_path_to_career,
    get_all_careers,
    get_tree_metrics,
    draw_tree,
    generate_markdown_report,
    DecisionNode,
    CareerProfile
)

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
