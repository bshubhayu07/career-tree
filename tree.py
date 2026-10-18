"""
tree.py - Core Binary Decision Tree Engine for CareerTree
Implements a strict binary decision tree with node traversals, metrics,
and rich career profiles.
"""

from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches


@dataclass
class CareerProfile:
    title: str
    category: str
    tagline: str
    overview: str
    why_match: str
    skills: List[str]
    tools: List[str]
    day_in_the_life: str
    salary_range: str
    growth_outlook: str
    certifications: List[str]
    roadmap: List[Tuple[str, str]]


class DecisionNode:
    """
    Represents a node in the binary decision tree.
    - Internal nodes contain a question, context tip, and two children: yes and no.
    - Leaf nodes contain a CareerProfile.
    """
    def __init__(
        self,
        question: Optional[str] = None,
        context_tip: Optional[str] = None,
        yes: Optional["DecisionNode"] = None,
        no: Optional["DecisionNode"] = None,
        career: Optional[CareerProfile] = None,
        node_id: Optional[str] = None
    ):
        self.question = question
        self.context_tip = context_tip
        self.yes = yes
        self.no = no
        self.career = career
        self.node_id = node_id

    @property
    def is_leaf(self) -> bool:
        return self.career is not None

    def count_nodes(self) -> int:
        """Calculate total number of nodes in this subtree."""
        if self.is_leaf:
            return 1
        count = 1
        if self.yes:
            count += self.yes.count_nodes()
        if self.no:
            count += self.no.count_nodes()
        return count

    def count_leaves(self) -> int:
        """Calculate total number of leaf nodes in this subtree."""
        if self.is_leaf:
            return 1
        leaves = 0
        if self.yes:
            leaves += self.yes.count_leaves()
        if self.no:
            leaves += self.no.count_leaves()
        return leaves

    def get_height(self) -> int:
        """Calculate height of the subtree."""
        if self.is_leaf:
            return 0
        left_h = self.yes.get_height() if self.yes else 0
        right_h = self.no.get_height() if self.no else 0
        return 1 + max(left_h, right_h)

    def is_balanced(self) -> bool:
        """Verify if subtree satisfies binary tree balance criteria."""
        def check(node):
            if not node or node.is_leaf:
                return 0, True
            lh, lb = check(node.yes)
            rh, rb = check(node.no)
            balanced = lb and rb and abs(lh - rh) <= 1
            return 1 + max(lh, rh), balanced
        _, balanced = check(self)
        return balanced


def build_career_tree() -> DecisionNode:
    """
    Constructs a balanced binary decision tree of depth 4 with 16 distinct career leaves.
    Total nodes: 31 (15 internal decision nodes + 16 leaf nodes).
    """

    # --- 16 CAREER PROFILES ---

    # Leaf 1: Yes -> Yes -> Yes -> Yes
    c_cyber = CareerProfile(
        title="Cybersecurity Analyst & Ethical Hacker",
        category="Security & Defense",
        tagline="Protect mission-critical systems and hunt vulnerabilities before adversaries do.",
        overview="Cybersecurity Analysts monitor networks, perform vulnerability penetration assessments, audit threat surfaces, and respond to security breaches to safeguard critical infrastructure.",
        why_match="You chose technical depth, systems-level architecture, infrastructure resilience, and offensive/defensive security engineering.",
        skills=["Network Protocols (TCP/IP)", "Penetration Testing", "Threat Modeling", "SIEM & Log Auditing", "Cryptography", "Incident Response"],
        tools=["Wireshark", "Burp Suite", "Metasploit", "Splunk", "Kali Linux", "Nmap"],
        day_in_the_life="Analyze firewall logs and anomaly alerts, conduct authorized penetration testing against web endpoints, and design zero-trust threat containment workflows.",
        salary_range="$95,000 - $160,000 / ₹12 - ₹30 LPA",
        growth_outlook="+32% (Much faster than average, extreme talent shortage)",
        certifications=["CompTIA Security+", "Certified Ethical Hacker (CEH)", "Offensive Security Certified Professional (OSCP)"],
        roadmap=[
            ("Foundational", "Master networking fundamentals, Linux command line, and common CVE vulnerabilities."),
            ("Intermediate", "Participate in CTF (Capture The Flag) competitions and audit web security (OWASP Top 10)."),
            ("Advanced", "Specialize in red-teaming, reverse engineering, and cloud security architecture.")
        ]
    )

    # Leaf 2: Yes -> Yes -> Yes -> No
    c_cloud = CareerProfile(
        title="Cloud Solutions Architect & DevOps Engineer",
        category="Infrastructure & Cloud",
        tagline="Design resilient cloud foundations and automate continuous deployment pipelines at planet scale.",
        overview="Cloud Architects and DevOps Engineers build highly scalable, distributed cloud architectures, configure automated CI/CD pipelines, and guarantee 99.999% uptime for cloud services.",
        why_match="You prefer technical problem solving, backend systems, and automated infrastructure design over pure security auditing.",
        skills=["Infrastructure as Code (IaC)", "Container Orchestration", "CI/CD Pipelines", "System Architecture", "Networking & DNS", "Observability"],
        tools=["Docker", "Kubernetes", "Terraform", "AWS / Azure / GCP", "GitHub Actions", "Prometheus & Grafana"],
        day_in_the_life="Write Terraform templates for multi-region microservices, optimize Kubernetes cluster autoscaling, and troubleshoot CI/CD release pipelines.",
        salary_range="$105,000 - $175,000 / ₹14 - ₹35 LPA",
        growth_outlook="+26% (Very High, cornerstone of modern tech enterprises)",
        certifications=["AWS Certified Solutions Architect", "Certified Kubernetes Administrator (CKA)", "Terraform Associate"],
        roadmap=[
            ("Foundational", "Learn Linux sysadmin, networking, Docker containerization, and basic Bash/Python scripting."),
            ("Intermediate", "Build automated CI/CD workflows and deploy containerized apps using Kubernetes and Helm."),
            ("Advanced", "Architect multi-cloud hybrid systems, implement zero-trust networking and cost-optimization.")
        ]
    )

    # Leaf 3: Yes -> Yes -> No -> Yes
    c_game = CareerProfile(
        title="Game Developer & Real-Time 3D Engineer",
        category="Game Tech & Interactive Systems",
        tagline="Fuse high-performance physics, graphics programming, and immersive interactive worlds.",
        overview="Game Developers engineer game mechanics, physics simulations, 3D graphics rendering pipelines, and multiplayer networking to create captivating interactive entertainment.",
        why_match="You love technical programming and application development, specifically channeled into real-time rendering, physics, and gameplay mechanics.",
        skills=["C++ / C# Programming", "Linear Algebra & Vectors", "Game Physics & Collision", "Shaders & HLSL/GLSL", "Multiplayer Networking", "Memory Management"],
        tools=["Unreal Engine 5", "Unity", "Godot", "Blender", "DirectX / Vulkan", "Git LFS"],
        day_in_the_life="Program procedural animation systems, optimize frame render times from 30 FPS to 60+ FPS, and script combat gameplay state machines.",
        salary_range="$85,000 - $145,000 / ₹10 - ₹26 LPA",
        growth_outlook="+18% (Strong global demand across AAA, Indie, and Metaverse studios)",
        certifications=["Unity Certified Professional Programmer", "Epic Games Unreal Engine Certificate"],
        roadmap=[
            ("Foundational", "Master C++ or C# and mathematical fundamentals (matrices, quaternions, coordinate spaces)."),
            ("Intermediate", "Build 2D and 3D indie playable game prototypes with sound, physics, and collision detection."),
            ("Advanced", "Dive into custom rendering engines, memory optimization, spatial audio, and multiplayer replication.")
        ]
    )

    # Leaf 4: Yes -> Yes -> No -> No
    c_fullstack = CareerProfile(
        title="Full Stack Software Engineer",
        category="Software Engineering",
        tagline="Architect and ship end-to-end modern digital products from responsive UI to resilient databases.",
        overview="Full Stack Engineers bridge frontend user experiences with robust backend services, designing REST/GraphQL APIs, database schemas, and scalable web architectures.",
        why_match="You prefer technical application development focused on creating modern web and mobile apps that millions of people use every day.",
        skills=["Full-Lifecycle Web Dev", "REST & GraphQL APIs", "Relational & NoSQL DBs", "State Management", "System Design", "Unit & Integration Testing"],
        tools=["React / Next.js", "Node.js / FastAPI / Go", "TypeScript", "PostgreSQL", "Tailwind CSS", "Redis"],
        day_in_the_life="Implement responsive frontend components in TypeScript, create microservice endpoints in Go/Python, and optimize database indexing for high query volumes.",
        salary_range="$90,000 - $155,000 / ₹11 - ₹28 LPA",
        growth_outlook="+24% (Evergreen core demand across all tech companies)",
        certifications=["Meta Full-Stack Developer Professional Certificate", "AWS Certified Developer - Associate"],
        roadmap=[
            ("Foundational", "Master HTML5/CSS3, modern JavaScript (ES6+), TypeScript, and responsive web design."),
            ("Intermediate", "Build full-stack applications with React/Next.js, SQL databases, and secure JWT authentication."),
            ("Advanced", "Master distributed microservices, caching with Redis, message queues (Kafka), and scalable architecture.")
        ]
    )

    # Leaf 5: Yes -> No -> Yes -> Yes
    c_mlops = CareerProfile(
        title="Machine Learning Operations (MLOps) Engineer",
        category="AI Platform & Systems",
        tagline="Bridge the gap between experimental AI prototypes and battle-tested production deployments.",
        overview="MLOps Engineers operationalize machine learning models by orchestrating training pipelines, managing model registries, monitoring data drift, and serving high-throughput inference APIs.",
        why_match="You combine a passion for AI/ML with systems engineering, production automation, and scalable deployment pipelines.",
        skills=["Model Deployment & Serving", "Feature Stores & Data Versioning", "Data Drift & Monitoring", "Docker & Kubernetes for AI", "Distributed Training Pipelines", "CI/CD for ML"],
        tools=["MLflow", "Kubeflow", "Triton Inference Server", "DVC", "Docker", "PyTorch / ONNX"],
        day_in_the_life="Configure automated retraining triggers when model performance drifts, optimize model quantization for edge inference, and manage GPU cluster workloads.",
        salary_range="$110,000 - $185,000 / ₹16 - ₹38 LPA",
        growth_outlook="+35% (Rapidly emerging as one of the highest-paid AI specialties)",
        certifications=["Google Cloud Professional Machine Learning Engineer", "Databricks Certified MLOps Professional"],
        roadmap=[
            ("Foundational", "Solidify Python, basic Machine Learning workflows, and Linux containerization with Docker."),
            ("Intermediate", "Implement automated experiment tracking, model registry, and CI/CD pipelines with MLflow & DVC."),
            ("Advanced", "Deploy large language models (LLMs) and computer vision models with Triton, TensorRT, and Kubernetes.")
        ]
    )

    # Leaf 6: Yes -> No -> Yes -> No
    c_airesearch = CareerProfile(
        title="AI & Deep Learning Research Scientist",
        category="Artificial Intelligence",
        tagline="Push the frontiers of intelligence, generative AI, and novel mathematical neural architectures.",
        overview="AI Research Scientists investigate foundational breakthroughs in deep neural networks, transformers, reinforcement learning, and generative models, publishing research and designing state-of-the-art algorithms.",
        why_match="You thrive on deep mathematical inquiry, algorithmic innovation, and theoretical advances in artificial intelligence.",
        skills=["Deep Neural Network Theory", "Multivariable Calculus & Linear Algebra", "Probability & Statistics", "Algorithm Design", "Scientific Experimentation", "Academic Research Writing"],
        tools=["PyTorch", "JAX", "Transformers (Hugging Face)", "Weights & Biases", "CUDA", "LaTeX"],
        day_in_the_life="Formulate hypotheses on novel attention mechanisms, run multi-GPU training benchmarks on supercomputers, and author research papers for NeurIPS/ICLR.",
        salary_range="$120,000 - $220,000 / ₹20 - ₹50+ LPA",
        growth_outlook="+33% (Intense global competition for frontier research talent)",
        certifications=["DeepLearning.AI Deep Learning Specialization", "Stanford CS224N / CS231n Certifications"],
        roadmap=[
            ("Foundational", "Master advanced calculus, linear algebra, probability, and implement classic ML algorithms from scratch."),
            ("Intermediate", "Read and replicate seminal papers in CNNs, Transformers, Diffusion Models, and Reinforcement Learning."),
            ("Advanced", "Contribute novel architectures to open-source libraries, conduct ablation studies, and publish research.")
        ]
    )

    # Leaf 7: Yes -> No -> No -> Yes
    c_quant = CareerProfile(
        title="Quantitative Analyst (Quant) & Financial Modeler",
        category="Quantitative Finance",
        tagline="Harness stochastic calculus, statistical arbitrage, and algorithms to decode financial markets.",
        overview="Quants construct complex mathematical and statistical models for pricing financial derivatives, managing systemic risk, and executing algorithmic high-frequency trading strategies.",
        why_match="You love mathematical rigor, probability, financial markets, and high-stakes data-driven decision making.",
        skills=["Stochastic Calculus", "Time-Series Forecasting", "Statistical Arbitrage", "Monte Carlo Simulations", "Risk Modeling (VaR)", "High-Performance Computing"],
        tools=["Python (NumPy, SciPy)", "C++ for Low Latency", "R", "Bloomberg Terminal", "KDB+ / q", "Pandas"],
        day_in_the_life="Backtest algorithmic volatility trading strategies against historical tick data, calibrate Black-Scholes derivative pricing models, and optimize portfolio risk factors.",
        salary_range="$125,000 - $240,000+ / ₹22 - ₹60+ LPA",
        growth_outlook="+19% (Consistently prestigious, lucrative Wall Street and hedge-fund demand)",
        certifications=["Chartered Financial Analyst (CFA)", "Financial Risk Manager (FRM)", "Certificate in Quantitative Finance (CQF)"],
        roadmap=[
            ("Foundational", "Build deep proficiency in probability theory, matrix operations, financial markets, and Python/R."),
            ("Intermediate", "Model asset pricing, implement Monte Carlo options pricing, and execute algorithmic backtests."),
            ("Advanced", "Master high-frequency trading architectures in low-latency C++, market microstructure, and deep reinforcement learning in finance.")
        ]
    )

    # Leaf 8: Yes -> No -> No -> No
    c_datasci = CareerProfile(
        title="Data Scientist & Business Intelligence Lead",
        category="Data Science & Analytics",
        tagline="Transform massive datasets into strategic executive insights and predictive business value.",
        overview="Data Scientists extract actionable patterns from structured and unstructured data, build predictive machine learning models, and present interactive executive dashboards.",
        why_match="You enjoy finding hidden insights in data, statistical inference, and explaining business strategy through analytical storytelling.",
        skills=["Exploratory Data Analysis", "Hypothesis Testing & A/B Testing", "Statistical Modeling", "Data Wrangling & SQL", "Executive Presentation", "Dashboarding"],
        tools=["SQL", "Python / R", "Tableau / PowerBI", "Pandas & Scikit-Learn", "Snowflake / BigQuery", "dbt"],
        day_in_the_life="Extract million-row cohorts from Snowflake, run multivariate A/B testing on user retention, and present quarterly predictive forecasts to executive leadership.",
        salary_range="$92,000 - $155,000 / ₹11 - ₹27 LPA",
        growth_outlook="+28% (Critical role across finance, healthcare, e-commerce, and tech)",
        certifications=["Google Advanced Data Analytics Professional Certificate", "Microsoft Certified: Power BI Data Analyst"],
        roadmap=[
            ("Foundational", "Master advanced SQL querying, data cleaning with Pandas, and essential descriptive/inferential statistics."),
            ("Intermediate", "Build interactive dashboards in PowerBI/Tableau and deploy predictive regression and classification models in Scikit-Learn."),
            ("Advanced", "Design enterprise A/B test experiments, causal inference models, and automated data pipelines with dbt.")
        ]
    )

    # Leaf 9: No -> Yes -> Yes -> Yes
    c_uxres = CareerProfile(
        title="UX Researcher & Usability Specialist",
        category="UX & Human Factors",
        tagline="Champion the voice of users through behavioral observation, psychology, and empathy.",
        overview="UX Researchers conduct user interviews, usability audits, heuristic evaluations, and behavioral studies to uncover user pain points and guide intuitive product designs.",
        why_match="You care deeply about human psychology, user empathy, ethnographic observation, and validating interface usability.",
        skills=["User Interviewing", "Usability Testing Protocols", "Heuristic Evaluation", "Qualitative & Quantitative Synthesis", "Persona & Journey Mapping", "Behavioral Psychology"],
        tools=["Figma", "UserTesting", "Miro", "Dovetail", "Optimal Workshop (Card Sorting)", "Hotjar"],
        day_in_the_life="Interview participants to test an upcoming feature prototype, synthesize thematic insights in Dovetail, and present usability findings to engineering teams.",
        salary_range="$85,000 - $145,000 / ₹10 - ₹25 LPA",
        growth_outlook="+16% (Essential role as software complexity grows and human-centered design dominates)",
        certifications=["Nielsen Norman Group (NN/g) UX Master Certified", "Interaction Design Foundation (IxDF) Certification"],
        roadmap=[
            ("Foundational", "Study cognitive psychology, human-computer interaction (HCI) heuristics, and qualitative research methods."),
            ("Intermediate", "Run real-world usability test sessions, construct user journey maps, and document case studies."),
            ("Advanced", "Lead mixed-methods research combining telemetry analytics with deep qualitative ethnographic discovery.")
        ]
    )

    # Leaf 10: No -> Yes -> Yes -> No
    c_uidesign = CareerProfile(
        title="UI / Visual Design & Design Systems Architect",
        category="UI & Visual Design",
        tagline="Craft elegant, pixel-perfect design systems, typography, and captivating modern interfaces.",
        overview="UI Designers and Design System Architects create harmonious color palettes, fluid component libraries, responsive layouts, and interactive micro-animations for digital applications.",
        why_match="You love visual aesthetics, typography, design consistency, and building standardized UI component systems that scale.",
        skills=["Visual Hierarchy", "Design Systems & Tokens", "Typography & Color Theory", "Micro-Interactions & Prototyping", "Responsive Layouts", "Accessibility (WCAG)"],
        tools=["Figma", "Adobe Creative Cloud", "Framer", "Storybook", "Principle", "Tokens Studio"],
        day_in_the_life="Define reusable multi-state button tokens in Figma, test color contrast for WCAG accessibility compliance, and review component parity with frontend developers.",
        salary_range="$82,000 - $140,000 / ₹9 - ₹24 LPA",
        growth_outlook="+15% (High demand across digital agencies, startups, and product companies)",
        certifications=["Google UX Design Professional Certificate", "CalArts Graphic Design Specialization"],
        roadmap=[
            ("Foundational", "Master design fundamentals: grid systems, visual hierarchy, typography, and Figma components."),
            ("Intermediate", "Create comprehensive design systems with responsive auto-layout, variants, and design tokens."),
            ("Advanced", "Master advanced micro-interactions, accessibility compliance, and developer design system handoff.")
        ]
    )

    # Leaf 11: No -> Yes -> No -> Yes
    c_xr = CareerProfile(
        title="XR / Spatial Computing & AR/VR Experience Designer",
        category="Immersive Computing",
        tagline="Pioneer the future of 3D spatial computing, augmented reality, and virtual worlds.",
        overview="XR Experience Designers craft spatial interactions, 3D user interfaces, ergonomic virtual environments, and gestures for devices like Apple Vision Pro and Meta Quest.",
        why_match="You want to explore the cutting edge of visual design combined with immersive 3D spatial computing and augmented reality.",
        skills=["Spatial UI / UX Design", "3D Ergonomics & Depth Perception", "Spatial Audio Integration", "Gesture & Gaze Interaction", "Rapid 3D Prototyping", "Environment Storytelling"],
        tools=["Unity", "Unreal Engine", "Blender", "ShapesXR", "Figma", "Reality Composer Pro"],
        day_in_the_life="Prototype spatial window interactions in ShapesXR, test hand-tracking ergonomics in a VR headset, and refine spatial audio cues for seamless immersion.",
        salary_range="$95,000 - $165,000 / ₹12 - ₹30 LPA",
        growth_outlook="+25% (Surging field driven by Apple Vision Pro, Meta Quest, and spatial computing)",
        certifications=["Unity Certified XR Developer", "Circuit Stream XR Design Professional"],
        roadmap=[
            ("Foundational", "Learn 3D modeling basics in Blender and understand spatial human ergonomics and field-of-view."),
            ("Intermediate", "Build interactive AR/VR prototypes in Unity using OpenXR and ShapesXR."),
            ("Advanced", "Design spatial interaction paradigms with gaze, eye-tracking, and hand-gesture interfaces.")
        ]
    )

    # Leaf 12: No -> Yes -> No -> No
    c_motion = CareerProfile(
        title="Digital Brand & Motion Graphics Art Director",
        category="Creative Media & Motion",
        tagline="Electrify brands with kinetic typography, captivating motion design, and visual narratives.",
        overview="Motion Graphics Art Directors produce high-impact brand identities, animated video content, cinematic title sequences, and social campaigns that capture modern audiences.",
        why_match="You prefer artistic expression, video storytelling, animation timing, and brand aesthetics over interface psychology.",
        skills=["Kinetic Typography", "Motion Graphics & Animation", "Brand Storytelling", "Video Editing & Post-Production", "Color Grading", "Art Direction"],
        tools=["Adobe After Effects", "Cinema 4D", "Premiere Pro", "Illustrator", "DaVinci Resolve", "Blender"],
        day_in_the_life="Keyframe an animated 3D product launch reveal in After Effects, balance color grading for a commercial spot, and direct visual style guides for brand marketing campaigns.",
        salary_range="$75,000 - $135,000 / ₹8 - ₹22 LPA",
        growth_outlook="+14% (Consistent demand across advertising, entertainment, and digital media)",
        certifications=["Adobe Certified Professional in After Effects & Premiere Pro", "School of Motion Certificate"],
        roadmap=[
            ("Foundational", "Master the 12 principles of animation, vector illustration in Illustrator, and timeline editing."),
            ("Intermediate", "Produce kinetic typography, logo reveals, and motion graphics packages in After Effects."),
            ("Advanced", "Incorporate 3D motion design in Cinema 4D and lead creative art direction for commercial campaigns.")
        ]
    )

    # Leaf 13: No -> No -> Yes -> Yes
    c_consultant = CareerProfile(
        title="Technology Strategy & Management Consultant",
        category="Tech Strategy & Advisory",
        tagline="Advise global leadership on digital transformation, technology roadmaps, and enterprise ROI.",
        overview="Tech Strategy Consultants advise Fortune 500 executives on technology investments, cloud migrations, AI adoption strategies, and organizational process re-engineering.",
        why_match="You possess high-level strategic vision, business acumen, executive communication skills, and love solving organizational problems.",
        skills=["Digital Transformation Strategy", "Enterprise Architecture Advisory", "Business Case & ROI Modeling", "Executive Storytelling", "Change Management", "Market & Competitive Analysis"],
        tools=["PowerPoint / Keynote", "Excel Financial Modeling", "Miro / Lucidchart", "Gartner Research", "Tableau", "Jira Align"],
        day_in_the_life="Build cost-benefit models for a legacy-to-cloud transition, facilitate an executive strategy workshop with a Chief Information Officer, and craft an advisory board deck.",
        salary_range="$115,000 - $190,000 / ₹18 - ₹42 LPA",
        growth_outlook="+20% (High corporate demand for navigating AI and digital disruptions)",
        certifications=["TOGAF Enterprise Architecture", "PMP (Project Management Professional)", "Certified Information Systems Auditor (CISA)"],
        roadmap=[
            ("Foundational", "Understand business fundamentals, technology stacks, financial accounting, and structured problem solving."),
            ("Intermediate", "Learn consulting frameworks (SWOT, Porter's Five Forces, MECE) and executive slide design."),
            ("Advanced", "Lead digital transformation initiatives, enterprise risk management, and C-suite client engagements.")
        ]
    )

    # Leaf 14: No -> No -> Yes -> No
    c_pm = CareerProfile(
        title="Technical Product Manager (TPM)",
        category="Product Leadership",
        tagline="Steer product vision from zero to one, uniting engineering, design, and business goals.",
        overview="Technical Product Managers define product requirements, prioritize roadmap backlogs, coordinate cross-functional agile teams, and ensure products deliver measurable customer value.",
        why_match="You love operating at the intersection of technology, user needs, and business strategy without getting bogged down in low-level code.",
        skills=["Product Vision & Roadmap Planning", "Agile & Scrum Methodologies", "Feature Prioritization (RICE/MoSCoW)", "User Story Specification", "Data-Driven Decision Making", "Stakeholder Alignment"],
        tools=["Jira", "Notion", "Linear", "Figma", "Mixpanel / Amplitude", "Productboard"],
        day_in_the_life="Analyze product retention metrics in Mixpanel, conduct sprint planning with the engineering leads, and draft comprehensive PRDs (Product Requirement Documents).",
        salary_range="$105,000 - $175,000 / ₹15 - ₹36 LPA",
        growth_outlook="+21% (Critical cornerstone role in every software organization)",
        certifications=["Certified Scrum Product Owner (CSPO)", "Product School Product Management Certificate (PMC)"],
        roadmap=[
            ("Foundational", "Learn agile development frameworks, basic technical literacy (APIs, databases), and user research basics."),
            ("Intermediate", "Write clear PRDs, run sprint ceremonies, and conduct product metric analysis (DAU, CAC, LTV)."),
            ("Advanced", "Drive high-impact multi-team product portfolios, launch 0-to-1 products, and establish market positioning.")
        ]
    )

    # Leaf 15: No -> No -> No -> Yes
    c_devrel = CareerProfile(
        title="Developer Relations (DevRel) & Technical Advocate",
        category="Developer Advocacy & Community",
        tagline="Inspire global developers through technical tutorials, open-source demos, and keynote talks.",
        overview="DevRel Advocates serve as the voice of the community and the public face of developer tools, crafting technical content, open-source sample apps, and presenting at developer conferences.",
        why_match="You love public communication, building fun technical demos, teaching developers, and cultivating open-source communities.",
        skills=["Technical Writing & Blogging", "Public Speaking & Keynotes", "Sample Application Building", "Community Management", "Developer Feedback Synthesis", "Video & Livestream Production"],
        tools=["GitHub", "Markdown", "Obsidian", "OBS Studio", "Discord / Discourse", "YouTube / Twitch"],
        day_in_the_life="Write an engaging blog post explaining a new SDK release, build an open-source demo repository, and host a live community Q&A session with external developers.",
        salary_range="$95,000 - $160,000 / ₹12 - ₹30 LPA",
        growth_outlook="+22% (Essential role for developer-first SaaS, API, and cloud platforms)",
        certifications=["GitHub Foundations / Actions Certified", "AWS Technical Evangelism Accreditations"],
        roadmap=[
            ("Foundational", "Develop strong technical writing skills and maintain an active GitHub profile with clean READMEs."),
            ("Intermediate", "Speak at local meetups, record developer tutorials, and contribute to open-source projects."),
            ("Advanced", "Keynote at international developer conferences, run developer hackathons, and shape product developer experience (DX).")
        ]
    )

    # Leaf 16: No -> No -> No -> No
    c_edtech = CareerProfile(
        title="EdTech Instructional Designer & Learning Specialist",
        category="Education & Learning Tech",
        tagline="Reimagine how the world learns through cognitive science, interactive curricula, and modern tech.",
        overview="Instructional Designers and Learning Specialists develop educational software, interactive courses, simulations, and corporate training programs using pedagogy and learning science.",
        why_match="You are driven by empathy, educational pedagogy, mentoring others, and designing transformative learning experiences.",
        skills=["Instructional Design (ADDIE / SAM)", "Adult Learning Principles", "Curriculum Architecture", "Assessment & Rubric Design", "Interactive Learning Media", "Gamification in Education"],
        tools=["Articulate 360", "Canvas LMS / Moodle", "Notion", "Loom", "Figma", "Kahoot / Slido"],
        day_in_the_life="Structure a modular cybersecurity curriculum for corporate learners, build interactive knowledge checks in Articulate Storyline, and review learner completion rates.",
        salary_range="$75,000 - $130,000 / ₹8 - ₹20 LPA",
        growth_outlook="+17% (Rapid growth across online academies, universities, and corporate L&D)",
        certifications=["ATD Master Instructional Designer Certification", "Coursera Instructional Design Specialization"],
        roadmap=[
            ("Foundational", "Study cognitive learning theories, Bloom's Taxonomy, and the ADDIE instructional model."),
            ("Intermediate", "Author interactive e-learning modules using Articulate Storyline, interactive quizzes, and micro-learning."),
            ("Advanced", "Design scalable enterprise learning ecosystems, gamified simulation platforms, and university programs.")
        ]
    )

    # --- HIERARCHY ASSEMBLY (Depth 4 Binary Tree) ---

    # Level 4 Decision Nodes:
    # 4A: Cybersecurity vs Cloud Architect
    n_4a = DecisionNode(
        question="Do you enjoy defending systems against attacks and finding vulnerabilities more than designing scalable cloud infrastructure and pipelines?",
        context_tip="Choose 'Yes' for Cybersecurity & Ethical Hacking; choose 'No' for Cloud Infrastructure & DevOps.",
        yes=DecisionNode(career=c_cyber, node_id="leaf_cyber"),
        no=DecisionNode(career=c_cloud, node_id="leaf_cloud"),
        node_id="n_4a"
    )

    # 4B: Game Dev vs Full Stack
    n_4b = DecisionNode(
        question="Do you prefer creating interactive games, 3D graphics, and physics over building modern full-stack web and mobile applications?",
        context_tip="Choose 'Yes' for Game Development & 3D; choose 'No' for Full Stack Web & Mobile Engineering.",
        yes=DecisionNode(career=c_game, node_id="leaf_game"),
        no=DecisionNode(career=c_fullstack, node_id="leaf_fullstack"),
        node_id="n_4b"
    )

    # 4C: MLOps vs AI Research
    n_4c = DecisionNode(
        question="Do you prefer operationalizing, scaling, and deploying AI models in production (MLOps) over researching mathematical algorithms and experimental architectures?",
        context_tip="Choose 'Yes' for MLOps & Production Platforms; choose 'No' for Deep Learning & Algorithmic Research.",
        yes=DecisionNode(career=c_mlops, node_id="leaf_mlops"),
        no=DecisionNode(career=c_airesearch, node_id="leaf_airesearch"),
        node_id="n_4c"
    )

    # 4D: Quant Finance vs Data Science
    n_4d = DecisionNode(
        question="Are you interested in high-frequency trading, financial risk, and mathematical quantitative modeling over business intelligence dashboards and statistical storytelling?",
        context_tip="Choose 'Yes' for Quantitative Finance & Modeling; choose 'No' for Data Science & Business Intelligence.",
        yes=DecisionNode(career=c_quant, node_id="leaf_quant"),
        no=DecisionNode(career=c_datasci, node_id="leaf_datasci"),
        node_id="n_4d"
    )

    # 4E: UX Research vs UI Design
    n_4e = DecisionNode(
        question="Do you enjoy conducting user interviews, usability audits, and psychological research more than crafting pixel-perfect visual design systems and animations?",
        context_tip="Choose 'Yes' for UX Research & Psychology; choose 'No' for UI Design & Design Systems.",
        yes=DecisionNode(career=c_uxres, node_id="leaf_uxres"),
        no=DecisionNode(career=c_uidesign, node_id="leaf_uidesign"),
        node_id="n_4e"
    )

    # 4F: Spatial XR vs Motion Graphics
    n_4f = DecisionNode(
        question="Do you want to pioneer immersive 3D AR/VR virtual spaces and spatial computing experiences rather than digital brand media and motion graphics?",
        context_tip="Choose 'Yes' for Spatial Computing & XR/VR; choose 'No' for Digital Branding & Motion Graphics.",
        yes=DecisionNode(career=c_xr, node_id="leaf_xr"),
        no=DecisionNode(career=c_motion, node_id="leaf_motion"),
        node_id="n_4f"
    )

    # 4G: Tech Strategy vs Technical PM
    n_4g = DecisionNode(
        question="Do you prefer high-level technology strategy, enterprise transformation, and executive advisory over hands-on product feature roadmaps and agile delivery?",
        context_tip="Choose 'Yes' for Tech Strategy Consulting; choose 'No' for Technical Product Management (TPM).",
        yes=DecisionNode(career=c_consultant, node_id="leaf_consultant"),
        no=DecisionNode(career=c_pm, node_id="leaf_pm"),
        node_id="n_4g"
    )

    # 4H: DevRel vs EdTech
    n_4h = DecisionNode(
        question="Do you enjoy public developer community advocacy, keynote speaking, and coding demos more than structured educational curriculum and instructional design?",
        context_tip="Choose 'Yes' for Developer Relations (DevRel); choose 'No' for EdTech & Instructional Design.",
        yes=DecisionNode(career=c_devrel, node_id="leaf_devrel"),
        no=DecisionNode(career=c_edtech, node_id="leaf_edtech"),
        node_id="n_4h"
    )

    # Level 3 Decision Nodes:
    # 3A: Backend & Cloud & Security vs Application Development
    n_3a = DecisionNode(
        question="Are you more drawn to backend architecture, cloud infrastructure, and security than to interactive user-facing web, mobile, or game applications?",
        context_tip="Evaluates your preference between infrastructure/foundations vs application-layer engineering.",
        yes=n_4a,
        no=n_4b,
        node_id="n_3a"
    )

    # 3B: Advanced AI/Deep Learning vs Applied Data Analytics & Finance
    n_3b = DecisionNode(
        question="Are you primarily interested in cutting-edge deep learning, LLMs, and neural architectures rather than practical data analytics, predictive metrics, and quantitative finance?",
        context_tip="Evaluates frontier AI/neural networks vs applied analytics & financial mathematics.",
        yes=n_4c,
        no=n_4d,
        node_id="n_3b"
    )

    # 3C: Product & UX Interface vs Creative Media & Spatial XR
    n_3c = DecisionNode(
        question="Are you fascinated by user psychology, wireframing, and intuitive app interfaces over visual storytelling, 3D motion, and immersive multimedia?",
        context_tip="Evaluates software interface & ergonomics vs artistic/spatial digital media.",
        yes=n_4e,
        no=n_4f,
        node_id="n_3c"
    )

    # 3D: Product & Tech Strategy vs Community, Education & Advocacy
    n_3d = DecisionNode(
        question="Do you prefer defining product vision, business strategy, and roadmap priorities over empowering people, teaching, and developer advocacy?",
        context_tip="Evaluates product management/business strategy vs human mentorship, advocacy, and education.",
        yes=n_4g,
        no=n_4h,
        node_id="n_3d"
    )

    # Level 2 Decision Nodes:
    # 2A: Software/Systems vs Data/AI
    n_2a = DecisionNode(
        question="Do you prefer building software architectures, systems, and platforms rather than analyzing data patterns, statistical models, and AI algorithms?",
        context_tip="Distinguishes core software engineering from data science, machine learning, and quantitative analytics.",
        yes=n_3a,
        no=n_3b,
        node_id="n_2a"
    )

    # 2B: Visual & Interactive Design vs Strategy, People & Leadership
    n_2b = DecisionNode(
        question="Do you lean more toward visual, interactive design, and sensory digital experiences rather than business leadership, team coordination, and strategic management?",
        context_tip="Distinguishes visual/creative interface craft from product management, strategy, and education.",
        yes=n_3c,
        no=n_3d,
        node_id="n_2b"
    )

    # Level 1 Root Decision Node:
    root = DecisionNode(
        question="Do you prefer technical, analytical, and systems-oriented problem solving over creative, design, or human-centric strategy?",
        context_tip="The fundamental root branch: Engineering, Data & Systems vs Design, Product Strategy & People.",
        yes=n_2a,
        no=n_2b,
        node_id="root"
    )

    return root


def trace_tree(root: DecisionNode, answers: List[bool]) -> Tuple[DecisionNode, List[Tuple[str, bool]]]:
    """
    Follow yes/no choices from root to leaf.
    Returns (reached_node, path_history).
    """
    node = root
    path = []
    for ans in answers:
        if node.is_leaf:
            break
        path.append((node.question, ans))
        node = node.yes if ans else node.no
    return node, path


def find_path_to_career(root: DecisionNode, target_title: str) -> Optional[List[Tuple[DecisionNode, str]]]:
    """
    Depth-first search (DFS) to find the exact sequence of decisions leading to a target career.
    Returns list of (node, decision_string) pairs from root to leaf.
    """
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
    """In-order traversal yielding all career profiles."""
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
    """Calculate key DSA metrics of the decision tree."""
    total_nodes = root.count_nodes()
    total_leaves = root.count_leaves()
    height = root.get_height()
    internal_nodes = total_nodes - total_leaves
    balanced = root.is_balanced()

    return {
        "total_nodes": total_nodes,
        "leaf_nodes": total_leaves,
        "internal_nodes": internal_nodes,
        "tree_height": height,
        "is_balanced": balanced,
        "time_complexity": "O(h) = O(log2 N)",
        "space_complexity": "O(N)"
    }


def draw_tree(root: DecisionNode, highlighted_path_nodes: Optional[List[DecisionNode]] = None) -> plt.Figure:
    """
    Render a clean, high-resolution visual layout of the decision tree with Matplotlib.
    Highlights path if provided.
    """
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

    # Draw edges
    for parent, child, label in edges:
        p_id, c_id = id(parent), id(child)
        x1, y1 = positions[p_id]
        x2, y2 = positions[c_id]
        in_path = p_id in highlighted_ids and c_id in highlighted_ids

        edge_color = "#38bdf8" if in_path else "#334155"
        edge_width = 3.0 if in_path else 1.2
        edge_alpha = 1.0 if in_path else 0.45

        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=edge_width, alpha=edge_alpha, zorder=1)

        # Label on edge
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

    # Draw nodes
    for node_id, (x, y) in positions.items():
        is_highlighted = node_id in highlighted_ids
        ntype = node_types[node_id]
        label = node_labels[node_id]

        if ntype == "leaf":
            # Leaf career node
            face_color = "#059669" if is_highlighted else "#1e293b"
            edge_color = "#34d399" if is_highlighted else "#475569"
            size = 900
            ax.scatter([x], [y], s=size, facecolors=face_color, edgecolors=edge_color, linewidths=2.0, zorder=3)
            # Format text label
            words = label.split()
            short_label = "\n".join([" ".join(words[i:i+2]) for i in range(0, min(len(words), 4), 2)])
            ax.text(x, y - 0.28, short_label, ha="center", va="top", fontsize=7.0, color="#f1f5f9", fontweight="bold", zorder=4)
        else:
            # Internal question node
            face_color = "#2563eb" if is_highlighted else "#0f172a"
            edge_color = "#60a5fa" if is_highlighted else "#334155"
            size = 1200
            ax.scatter([x], [y], s=size, facecolors=face_color, edgecolors=edge_color, linewidths=2.0, zorder=3)
            q_num = "Q" if y == 0 else f"L{abs(int(y))}"
            ax.text(x, y, q_num, ha="center", va="center", fontsize=8.5, color="#ffffff", fontweight="bold", zorder=4)

    ax.set_title("CareerTree 4-Level Binary Decision Architecture (16 Pathways)", fontsize=15, color="#f8fafc", pad=20, fontweight="bold")
    ax.axis("off")
    fig.tight_layout()
    return fig


def generate_markdown_report(career: CareerProfile, path_answers: List[Tuple[str, bool]]) -> str:
    """Export a comprehensive career recommendation dossier in markdown."""
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
    report.append("---\n*Generated by CareerTree — Binary Decision Tree Career Engine*")
    return "\n".join(report)
