/**
 * tree.c - Implementation of the Binary Decision Tree Engine in Pure C.
 */

#include "tree.h"

/* Allocate and initialize an internal decision node */
DecisionNode* create_decision_node(const char* question, const char* context_tip, 
                                  DecisionNode* yes, DecisionNode* no, const char* node_id) {
    DecisionNode* node = (DecisionNode*)malloc(sizeof(DecisionNode));
    if (!node) {
        fprintf(stderr, "Error: Memory allocation failed for DecisionNode\n");
        exit(EXIT_FAILURE);
    }
    strncpy(node->question, question ? question : "", sizeof(node->question) - 1);
    node->question[sizeof(node->question) - 1] = '\0';

    strncpy(node->context_tip, context_tip ? context_tip : "", sizeof(node->context_tip) - 1);
    node->context_tip[sizeof(node->context_tip) - 1] = '\0';

    node->yes = yes;
    node->no = no;
    node->career = NULL;

    strncpy(node->node_id, node_id ? node_id : "", sizeof(node->node_id) - 1);
    node->node_id[sizeof(node->node_id) - 1] = '\0';

    return node;
}

/* Allocate and initialize a leaf node containing a CareerProfile */
DecisionNode* create_leaf_node(CareerProfile* career, const char* node_id) {
    DecisionNode* node = (DecisionNode*)malloc(sizeof(DecisionNode));
    if (!node) {
        fprintf(stderr, "Error: Memory allocation failed for DecisionNode (Leaf)\n");
        exit(EXIT_FAILURE);
    }
    node->question[0] = '\0';
    node->context_tip[0] = '\0';
    node->yes = NULL;
    node->no = NULL;
    node->career = career;

    strncpy(node->node_id, node_id ? node_id : "", sizeof(node->node_id) - 1);
    node->node_id[sizeof(node->node_id) - 1] = '\0';

    return node;
}

/* Allocate and populate a CareerProfile structure */
CareerProfile* create_career_profile(
    const char* title, const char* category, const char* tagline, const char* overview,
    const char* why_match, const char* skills[], int skill_count,
    const char* tools[], int tool_count, const char* certs[], int cert_count,
    const char* salary, const char* growth, const char* day_life,
    const char* road_f, const char* road_i, const char* road_a
) {
    CareerProfile* c = (CareerProfile*)malloc(sizeof(CareerProfile));
    if (!c) {
        fprintf(stderr, "Error: Memory allocation failed for CareerProfile\n");
        exit(EXIT_FAILURE);
    }
    int i;
    strncpy(c->title, title, sizeof(c->title) - 1);
    strncpy(c->category, category, sizeof(c->category) - 1);
    strncpy(c->tagline, tagline, sizeof(c->tagline) - 1);
    strncpy(c->overview, overview, sizeof(c->overview) - 1);
    strncpy(c->why_match, why_match, sizeof(c->why_match) - 1);

    c->skill_count = skill_count > MAX_SKILLS ? MAX_SKILLS : skill_count;
    for (i = 0; i < c->skill_count; i++) {
        strncpy(c->skills[i], skills[i], sizeof(c->skills[i]) - 1);
    }

    c->tool_count = tool_count > MAX_TOOLS ? MAX_TOOLS : tool_count;
    for (i = 0; i < c->tool_count; i++) {
        strncpy(c->tools[i], tools[i], sizeof(c->tools[i]) - 1);
    }

    c->cert_count = cert_count > 3 ? 3 : cert_count;
    for (i = 0; i < c->cert_count; i++) {
        strncpy(c->certifications[i], certs[i], sizeof(c->certifications[i]) - 1);
    }

    strncpy(c->salary_range, salary, sizeof(c->salary_range) - 1);
    strncpy(c->growth_outlook, growth, sizeof(c->growth_outlook) - 1);
    strncpy(c->day_in_the_life, day_life, sizeof(c->day_in_the_life) - 1);
    strncpy(c->roadmap_foundational, road_f, sizeof(c->roadmap_foundational) - 1);
    strncpy(c->roadmap_intermediate, road_i, sizeof(c->roadmap_intermediate) - 1);
    strncpy(c->roadmap_advanced, road_a, sizeof(c->roadmap_advanced) - 1);

    return c;
}

/* Recursive post-order tree destruction to prevent memory leaks */
void free_tree(DecisionNode* root) {
    if (!root) return;
    free_tree(root->yes);
    free_tree(root->no);
    if (root->career) {
        free(root->career);
    }
    free(root);
}

int is_leaf(const DecisionNode* node) {
    return (node != NULL && node->career != NULL);
}

int count_nodes(const DecisionNode* root) {
    if (!root) return 0;
    if (is_leaf(root)) return 1;
    return 1 + count_nodes(root->yes) + count_nodes(root->no);
}

int count_leaves(const DecisionNode* root) {
    if (!root) return 0;
    if (is_leaf(root)) return 1;
    return count_leaves(root->yes) + count_leaves(root->no);
}

int get_tree_height(const DecisionNode* root) {
    if (!root || is_leaf(root)) return 0;
    int lh = get_tree_height(root->yes);
    int rh = get_tree_height(root->no);
    return 1 + (lh > rh ? lh : rh);
}

int is_tree_balanced(const DecisionNode* root, int* height) {
    if (!root || is_leaf(root)) {
        *height = 0;
        return 1;
    }
    int lh = 0, rh = 0;
    int lb = is_tree_balanced(root->yes, &lh);
    int rb = is_tree_balanced(root->no, &rh);
    *height = 1 + (lh > rh ? lh : rh);
    int diff = lh > rh ? lh - rh : rh - lh;
    return (lb && rb && diff <= 1);
}

/* --- BOTTOM-UP CONSTRUCTION OF THE 16-CAREER BINARY TREE --- */
DecisionNode* build_career_tree(void) {
    /* 1. Cybersecurity */
    const char* s_cyber[] = {"TCP/IP", "Penetration Testing", "Threat Modeling", "SIEM Auditing", "Cryptography", "Incident Response"};
    const char* t_cyber[] = {"Wireshark", "Burp Suite", "Metasploit", "Splunk", "Kali Linux", "Nmap"};
    const char* cert_cyber[] = {"CompTIA Security+", "CEH", "OSCP"};
    CareerProfile* c_cyber = create_career_profile(
        "Cybersecurity Analyst & Ethical Hacker", "Security & Defense",
        "Protect mission-critical systems and hunt vulnerabilities before adversaries do.",
        "Monitors network endpoints, executes authorized penetration audits, and engineers defense posture.",
        "Matches preference for technical problem-solving, infrastructure, and offensive/defensive security.",
        s_cyber, 6, t_cyber, 6, cert_cyber, 3,
        "$95,000 - $160,000 / INR 12 - 30 LPA", "+32% (Critical global demand)",
        "Analyze firewall alerts, conduct web penetration testing, and write mitigation patches.",
        "Master networking protocols (OSI model, TCP/IP) and Linux sysadmin commands.",
        "Perform web audits (OWASP Top 10), participate in CTFs, and analyze SIEM logs.",
        "Specialize in red-teaming, kernel exploit reverse engineering, and cloud security."
    );

    /* 2. Cloud Architect */
    const char* s_cloud[] = {"IaC (Terraform)", "Kubernetes Orchestration", "CI/CD Pipelines", "System Architecture", "Networking", "Observability"};
    const char* t_cloud[] = {"Docker", "Kubernetes", "Terraform", "AWS/Azure/GCP", "GitHub Actions", "Prometheus"};
    const char* cert_cloud[] = {"AWS Solutions Architect", "CKA (Kubernetes)", "Terraform Associate"};
    CareerProfile* c_cloud = create_career_profile(
        "Cloud Solutions Architect & DevOps Engineer", "Infrastructure & Cloud",
        "Design resilient cloud foundations and automate continuous delivery at scale.",
        "Builds scalable multi-region cloud infrastructures, manages clusters, and guarantees high availability.",
        "Matches preference for technical systems, backend architectures, and production deployment automation.",
        s_cloud, 6, t_cloud, 6, cert_cloud, 3,
        "$105,000 - $175,000 / INR 14 - 35 LPA", "+26% (Core backbone of modern tech)",
        "Author Terraform templates, tune Kubernetes cluster autoscaling, and optimize release pipelines.",
        "Learn Linux, Docker containerization, networking fundamentals, and Python/Bash scripting.",
        "Build automated CI/CD workflows and deploy microservices with Kubernetes and Helm.",
        "Architect multi-cloud hybrid systems, zero-trust network policies, and disaster recovery."
    );

    /* 3. Game Developer */
    const char* s_game[] = {"C++ Programming", "Linear Algebra", "Game Physics", "Shaders (GLSL)", "Multiplayer Netcode", "Memory Optimization"};
    const char* t_game[] = {"Unreal Engine 5", "Unity", "Godot", "Blender", "Vulkan/DirectX", "Git LFS"};
    const char* cert_game[] = {"Unity Certified Programmer", "Unreal Engine Professional", "Epic Dev Grant"};
    CareerProfile* c_game = create_career_profile(
        "Game Developer & Real-Time 3D Engineer", "Game Tech & Interactive",
        "Fuse high-performance physics, rendering pipelines, and immersive virtual worlds.",
        "Engineers gameplay mechanics, 3D render loops, collision physics, and multiplayer replication.",
        "Matches passion for technical coding focused on graphics math, simulation, and real-time gaming.",
        s_game, 6, t_game, 6, cert_game, 3,
        "$85,000 - $145,000 / INR 10 - 26 LPA", "+18% (High demand across AAA and indie studios)",
        "Profile GPU frame times, script gameplay state machines in C++, and optimize spatial audio.",
        "Master C++ or C# and mathematical coordinate transforms (matrices, quaternions).",
        "Build complete 2D and 3D indie game prototypes with sound, physics, and gameplay logic.",
        "Write custom rendering shaders, low-latency netcode, and multithreaded ECS architectures."
    );

    /* 4. Full Stack Engineer */
    const char* s_full[] = {"Web Architecture", "REST & GraphQL", "SQL & NoSQL DBs", "State Management", "System Design", "Automated Testing"};
    const char* t_full[] = {"React/Next.js", "Node.js/FastAPI", "TypeScript", "PostgreSQL", "Tailwind CSS", "Redis"};
    const char* cert_full[] = {"Meta Full-Stack Engineer", "AWS Certified Developer", "Node.js Certified"};
    CareerProfile* c_full = create_career_profile(
        "Full Stack Software Engineer", "Software Engineering",
        "Architect and ship end-to-end modern digital products from user interface to databases.",
        "Builds responsive frontend interfaces connected to resilient backend services and distributed databases.",
        "Matches passion for building user-facing web and mobile applications used by millions.",
        s_full, 6, t_full, 6, cert_full, 3,
        "$90,000 - $155,000 / INR 11 - 28 LPA", "+24% (Evergreen demand across all companies)",
        "Create React components, implement secure API endpoints, and optimize database indexing.",
        "Master HTML5/CSS3, modern JavaScript (ES6+), TypeScript, and responsive layout design.",
        "Build full-stack applications with React, backend APIs, relational databases, and auth.",
        "Design distributed microservices, caching layers (Redis), and message queues (Kafka)."
    );

    /* 5. MLOps Engineer */
    const char* s_mlops[] = {"Model Deployment", "Feature Stores", "Drift Monitoring", "Docker for AI", "Distributed Training", "CI/CD for ML"};
    const char* t_mlops[] = {"MLflow", "Kubeflow", "Triton Server", "DVC", "Docker", "PyTorch/ONNX"};
    const char* cert_mlops[] = {"GCP Machine Learning Engineer", "Databricks MLOps", "AWS Machine Learning"};
    CareerProfile* c_mlops = create_career_profile(
        "Machine Learning Operations (MLOps) Engineer", "AI Platform & Systems",
        "Bridge the gap between experimental AI prototypes and resilient production systems.",
        "Orchestrates model training pipelines, manages model registries, and serves low-latency inference APIs.",
        "Combines passion for machine learning with production infrastructure engineering.",
        s_mlops, 6, t_mlops, 6, cert_mlops, 3,
        "$110,000 - $185,000 / INR 16 - 38 LPA", "+35% (Rapidly emerging high-paid AI specialty)",
        "Configure automated retraining triggers on data drift, quantize LLMs, and manage GPU clusters.",
        "Learn Python, fundamental ML algorithms, and Docker containerization.",
        "Build automated experiment tracking, model registry, and CI/CD pipelines with MLflow.",
        "Deploy large language models (LLMs) at scale using Triton, TensorRT, and Kubernetes."
    );

    /* 6. AI Research Scientist */
    const char* s_aires[] = {"Deep Neural Networks", "Multivariable Calculus", "Probability Theory", "Novel Architectures", "Empirical Research", "Paper Authoring"};
    const char* t_aires[] = {"PyTorch", "JAX", "Hugging Face", "Weights & Biases", "CUDA", "LaTeX"};
    const char* cert_aires[] = {"DeepLearning.AI Deep Learning", "Stanford CS224N", "Stanford CS231N"};
    CareerProfile* c_aires = create_career_profile(
        "AI & Deep Learning Research Scientist", "Artificial Intelligence",
        "Push the boundaries of intelligence, generative neural models, and novel architectures.",
        "Investigates foundational breakthroughs in transformers, diffusion models, and reinforcement learning.",
        "Matches deep mathematical curiosity, algorithmic experimentation, and frontier AI research.",
        s_aires, 6, t_aires, 6, cert_aires, 3,
        "$120,000 - $220,000 / INR 20 - 50+ LPA", "+33% (Intense global competition for research talent)",
        "Formulate novel attention mechanisms, run multi-GPU training benchmarks, and write research papers.",
        "Master advanced calculus, linear algebra, probability, and code algorithms from scratch.",
        "Replicate seminal papers in CNNs, Transformers, Diffusion Models, and RL.",
        "Publish novel architectures at conferences (NeurIPS, ICML), conducting ablation studies."
    );

    /* 7. Quantitative Analyst */
    const char* s_quant[] = {"Stochastic Calculus", "Time-Series Analysis", "Statistical Arbitrage", "Monte Carlo Methods", "Risk Modeling (VaR)", "High-Perf C++"};
    const char* t_quant[] = {"Python (NumPy/SciPy)", "Low-Latency C++", "R", "Bloomberg", "KDB+/q", "Pandas"};
    const char* cert_quant[] = {"CQF (Quantitative Finance)", "CFA Charter", "FRM (Risk Manager)"};
    CareerProfile* c_quant = create_career_profile(
        "Quantitative Analyst (Quant) & Financial Modeler", "Quantitative Finance",
        "Decode financial markets using stochastic calculus, statistical arbitrage, and algorithms.",
        "Builds complex mathematical models for pricing derivatives, risk management, and algorithmic trading.",
        "Matches passion for high-stakes mathematical rigor, probability theory, and financial modeling.",
        s_quant, 6, t_quant, 6, cert_quant, 3,
        "$125,000 - $240,000+ / INR 22 - 60+ LPA", "+19% (Prestigious Wall Street and hedge-fund demand)",
        "Backtest algorithmic trading models against historical tick data and calibrate option pricing.",
        "Build strong proficiency in probability theory, matrix operations, and Python/C++.",
        "Model asset pricing, implement Monte Carlo options simulations, and backtest strategies.",
        "Design ultra-low latency execution engines in C++, market microstructure, and deep RL."
    );

    /* 8. Data Scientist */
    const char* s_data[] = {"Exploratory Data Analysis", "A/B Hypothesis Testing", "Predictive Modeling", "SQL & Data Wrangling", "Storytelling", "Dashboarding"};
    const char* t_data[] = {"SQL", "Python/Pandas", "Tableau/PowerBI", "Scikit-Learn", "Snowflake", "dbt"};
    const char* cert_data[] = {"Google Advanced Data Analytics", "Microsoft PowerBI Analyst", "AWS Data Analytics"};
    CareerProfile* c_data = create_career_profile(
        "Data Scientist & Business Intelligence Lead", "Data Science & Analytics",
        "Transform massive datasets into strategic executive insights and predictive algorithms.",
        "Extracts patterns from data, builds predictive regression/classification models, and builds dashboards.",
        "Matches passion for finding insights in data, statistical inference, and business storytelling.",
        s_data, 6, t_data, 6, cert_data, 3,
        "$92,000 - $155,000 / INR 11 - 27 LPA", "+28% (Critical role across finance, retail, and tech)",
        "Extract cohorts via SQL, run multivariate A/B tests on user retention, and present forecasts.",
        "Master advanced SQL querying, data manipulation in Pandas, and inferential statistics.",
        "Build interactive dashboards in PowerBI/Tableau and deploy predictive Scikit-Learn models.",
        "Design enterprise A/B test experiments, causal inference models, and automated dbt pipelines."
    );

    /* 9. UX Researcher */
    const char* s_ux[] = {"User Interviewing", "Usability Testing", "Heuristic Audit", "Qualitative Synthesis", "Journey Mapping", "Cognitive Psychology"};
    const char* t_ux[] = {"Figma", "UserTesting", "Miro", "Dovetail", "Optimal Workshop", "Hotjar"};
    const char* cert_ux[] = {"NN/g UX Master Certified", "Interaction Design Foundation", "Google UX Certificate"};
    CareerProfile* c_ux = create_career_profile(
        "UX Researcher & Usability Specialist", "UX & Human Factors",
        "Champion user empathy through behavioral observation, psychology, and usability testing.",
        "Conducts qualitative user interviews, usability audits, and field studies to guide product intuition.",
        "Matches focus on human psychology, user empathy, ethnographic study, and software ergonomics.",
        s_ux, 6, t_ux, 6, cert_ux, 3,
        "$85,000 - $145,000 / INR 10 - 25 LPA", "+16% (Essential as software complexity increases)",
        "Interview participants on prototype usability, synthesize thematic findings, and present to engineers.",
        "Study cognitive psychology, human-computer interaction (HCI) heuristics, and qualitative protocols.",
        "Run real usability testing sessions, construct journey maps, and document detailed case studies.",
        "Lead mixed-methods research combining telemetry analytics with ethnographic discovery."
    );

    /* 10. UI Designer */
    const char* s_ui[] = {"Visual Hierarchy", "Design Systems & Tokens", "Typography & Color", "Prototyping & Motion", "Responsive Layouts", "Accessibility (WCAG)"};
    const char* t_ui[] = {"Figma", "Adobe CC", "Framer", "Storybook", "Principle", "Tokens Studio"};
    const char* cert_ui[] = {"Google UX Design Certificate", "CalArts Graphic Design Specialization", "Interaction Design"};
    CareerProfile* c_ui = create_career_profile(
        "UI / Visual Design & Design Systems Architect", "UI & Visual Design",
        "Craft pixel-perfect design systems, typography, and captivating modern interfaces.",
        "Builds component libraries, design token systems, responsive layouts, and micro-interactions.",
        "Matches love for visual aesthetics, typography, design consistency, and component systems.",
        s_ui, 6, t_ui, 6, cert_ui, 3,
        "$82,000 - $140,000 / INR 9 - 24 LPA", "+15% (High demand across digital agencies and startups)",
        "Define reusable multi-state button tokens in Figma, test contrast for WCAG, and sync with frontend.",
        "Master grid systems, visual hierarchy, typography rules, and Figma auto-layout components.",
        "Create scalable multi-brand design systems with responsive variants and design tokens.",
        "Master advanced micro-interactions, accessibility compliance, and developer token handoff."
    );

    /* 11. XR Spatial Designer */
    const char* s_xr[] = {"Spatial UI/UX Design", "3D Ergonomics", "Spatial Audio", "Gesture & Gaze Control", "3D Prototyping", "Spatial Storytelling"};
    const char* t_xr[] = {"Unity", "Unreal Engine", "Blender", "ShapesXR", "Figma", "Reality Composer"};
    const char* cert_xr[] = {"Unity Certified XR Developer", "Circuit Stream XR Design", "Meta AR Creator"};
    CareerProfile* c_xr = create_career_profile(
        "XR / Spatial Computing & AR/VR Experience Designer", "Immersive Computing",
        "Pioneer 3D spatial computing, augmented reality, and virtual immersive environments.",
        "Crafts spatial interfaces, 3D interaction ergonomics, and gesture controls for Apple Vision Pro & Quest.",
        "Matches passion for 3D visual design combined with immersive augmented and virtual reality.",
        s_xr, 6, t_xr, 6, cert_xr, 3,
        "$95,000 - $165,000 / INR 12 - 30 LPA", "+25% (Surging field driven by Apple Vision Pro & Meta Quest)",
        "Prototype spatial window ergonomics in ShapesXR and test hand-tracking gestures in headset.",
        "Learn 3D modeling basics in Blender and understand human field-of-view and spatial depth.",
        "Build interactive AR/VR prototypes in Unity using OpenXR and ShapesXR.",
        "Design spatial interaction paradigms combining gaze, eye-tracking, and hand gestures."
    );

    /* 12. Motion Graphics Director */
    const char* s_motion[] = {"Kinetic Typography", "Motion Design", "Brand Storytelling", "Video Post-Production", "Color Grading", "Art Direction"};
    const char* t_motion[] = {"After Effects", "Cinema 4D", "Premiere Pro", "Illustrator", "DaVinci Resolve", "Blender"};
    const char* cert_motion[] = {"Adobe Certified Professional (After Effects)", "School of Motion", "Maxon C4D Certified"};
    CareerProfile* c_motion = create_career_profile(
        "Digital Brand & Motion Graphics Art Director", "Creative Media & Motion",
        "Electrify brand narratives with kinetic typography, 3D animation, and motion design.",
        "Produces high-impact brand identities, commercial video animations, and title sequences.",
        "Matches artistic expression, animation timing, cinematic video, and brand aesthetic direction.",
        s_motion, 6, t_motion, 6, cert_motion, 3,
        "$75,000 - $135,000 / INR 8 - 22 LPA", "+14% (Consistent demand in entertainment and advertising)",
        "Keyframe a 3D product launch reveal in After Effects, grade commercial video, and direct campaigns.",
        "Master the 12 principles of animation, vector illustration in Illustrator, and timeline editing.",
        "Produce kinetic typography, logo reveals, and motion design packages in After Effects.",
        "Incorporate 3D motion design in Cinema 4D and lead creative art direction for campaigns."
    );

    /* 13. Tech Strategy Consultant */
    const char* s_cons[] = {"Digital Transformation", "Enterprise Architecture", "Business Case & ROI", "Executive Communication", "Change Management", "Market Analysis"};
    const char* t_cons[] = {"PowerPoint/Keynote", "Excel Financial Models", "Miro/Lucidchart", "Gartner Research", "Tableau", "Jira Align"};
    const char* cert_cons[] = {"TOGAF Enterprise Architecture", "PMP Project Management", "CISA Information Systems"};
    CareerProfile* c_cons = create_career_profile(
        "Technology Strategy & Management Consultant", "Tech Strategy & Advisory",
        "Advise executive leadership on digital transformation, cloud migrations, and tech ROI.",
        "Guides Fortune 500 leadership on IT roadmaps, enterprise architecture, and AI adoption strategy.",
        "Matches high-level strategic vision, business acumen, communication skills, and advisory problem-solving.",
        s_cons, 6, t_cons, 6, cert_cons, 3,
        "$115,000 - $190,000 / INR 18 - 42 LPA", "+20% (High corporate demand navigating digital disruption)",
        "Build cost-benefit models for legacy-to-cloud transitions and facilitate workshops with CIOs.",
        "Understand software architectures, technology stacks, corporate finance, and structured problem solving.",
        "Learn consulting frameworks (SWOT, Porter's Five Forces, MECE) and executive presentations.",
        "Lead enterprise digital transformation roadmaps, technology risk governance, and C-suite engagements."
    );

    /* 14. Technical PM */
    const char* s_pm[] = {"Product Vision & Roadmap", "Agile & Scrum Methodologies", "Feature Prioritization", "User Story Specs", "Data-Driven Decisions", "Stakeholder Alignment"};
    const char* t_pm[] = {"Jira", "Notion", "Linear", "Figma", "Mixpanel/Amplitude", "Productboard"};
    const char* cert_pm[] = {"Certified Scrum Product Owner (CSPO)", "Product School PMC", "Pragmatic Institute Certified"};
    CareerProfile* c_pm = create_career_profile(
        "Technical Product Manager (TPM)", "Product Leadership",
        "Steer product vision from zero to one, uniting engineering, design, and business goals.",
        "Defines product requirements, manages backlogs, aligns cross-functional teams, and ships value.",
        "Matches desire to operate at the intersection of technology, users, and business strategy.",
        s_pm, 6, t_pm, 6, cert_pm, 3,
        "$105,000 - $175,000 / INR 15 - 36 LPA", "+21% (Critical cornerstone role in software companies)",
        "Analyze product retention metrics in Mixpanel, lead sprint planning with tech leads, and write PRDs.",
        "Learn agile frameworks, technical literacy (APIs, DBs, cloud basics), and customer interviewing.",
        "Write comprehensive PRDs, run sprint ceremonies, and analyze engagement metrics (DAU, CAC).",
        "Lead multi-team 0-to-1 product launches, manage product portfolio roadmaps, and drive growth."
    );

    /* 15. DevRel Advocate */
    const char* s_devrel[] = {"Technical Writing", "Public Keynote Speaking", "Demo App Engineering", "Community Management", "Feedback Synthesis", "Video Production"};
    const char* t_devrel[] = {"GitHub", "Markdown", "Obsidian", "OBS Studio", "Discord/Discourse", "YouTube"};
    const char* cert_devrel[] = {"GitHub Foundations Certified", "AWS Technical Evangelist", "Google Cloud Developer"};
    CareerProfile* c_devrel = create_career_profile(
        "Developer Relations (DevRel) & Technical Advocate", "Developer Advocacy",
        "Inspire global developers through technical tutorials, open-source repos, and keynote talks.",
        "Acts as the voice of external developers, creating tutorials, sample applications, and SDK guides.",
        "Matches love for public speaking, writing technical blogs, coding demos, and open-source community.",
        s_devrel, 6, t_devrel, 6, cert_devrel, 3,
        "$95,000 - $160,000 / INR 12 - 30 LPA", "+22% (Essential for developer-first SaaS and API platforms)",
        "Write blog posts explaining new SDK features, build open-source sample repos, and host developer Q&As.",
        "Build strong technical writing skills and maintain an active GitHub profile with clean code.",
        "Speak at local tech meetups, produce video walkthroughs, and contribute to open-source libraries.",
        "Deliver keynote talks at international developer conferences and shape product DX (Developer Experience)."
    );

    /* 16. EdTech Specialist */
    const char* s_edtech[] = {"Instructional Design (ADDIE)", "Adult Learning Principles", "Curriculum Architecture", "Assessment Design", "Interactive Media", "Gamification"};
    const char* t_edtech[] = {"Articulate 360", "Canvas LMS", "Notion", "Loom", "Figma", "Kahoot"};
    const char* cert_edtech[] = {"ATD Master Instructional Designer", "Coursera Learning Design", "Instructional Design Institute"};
    CareerProfile* c_edtech = create_career_profile(
        "EdTech Instructional Designer & Learning Specialist", "Education & Learning Tech",
        "Reimagine how the world learns through cognitive science, interactive curricula, and tech.",
        "Creates interactive e-learning modules, university curricula, and corporate training programs.",
        "Matches deep passion for educational pedagogy, cognitive learning, teaching, and mentorship.",
        s_edtech, 6, t_edtech, 6, cert_edtech, 3,
        "$75,000 - $130,000 / INR 8 - 20 LPA", "+17% (Rapid growth across online academies and corporate L&D)",
        "Structure modular cybersecurity curricula, build knowledge checks in Articulate, and review metrics.",
        "Study cognitive learning theories, Bloom's Taxonomy, and the ADDIE instructional model.",
        "Author interactive e-learning courses with branch quizzes, multimedia lessons, and simulations.",
        "Design scalable enterprise corporate learning ecosystems, university programs, and gamification."
    );

    /* --- LEVEL 4 DECISION NODES --- */
    DecisionNode* n_4a = create_decision_node(
        "Do you enjoy defending networks and hunting vulnerabilities more than designing scalable cloud infrastructure?",
        "Yes -> Cybersecurity & Ethical Hacking | No -> Cloud Solutions & DevOps",
        create_leaf_node(c_cyber, "leaf_cyber"),
        create_leaf_node(c_cloud, "leaf_cloud"),
        "n_4a"
    );

    DecisionNode* n_4b = create_decision_node(
        "Do you prefer creating interactive games, 3D engines, and real-time physics over building full-stack web and mobile apps?",
        "Yes -> Game Dev & 3D Tech | No -> Full Stack Software Engineering",
        create_leaf_node(c_game, "leaf_game"),
        create_leaf_node(c_full, "leaf_full"),
        "n_4b"
    );

    DecisionNode* n_4c = create_decision_node(
        "Do you prefer operationalizing, scaling, and deploying AI models (MLOps) over researching novel mathematical architectures?",
        "Yes -> MLOps Platform Engineering | No -> AI & Deep Learning Research",
        create_leaf_node(c_mlops, "leaf_mlops"),
        create_leaf_node(c_aires, "leaf_aires"),
        "n_4c"
    );

    DecisionNode* n_4d = create_decision_node(
        "Are you interested in quantitative mathematical finance and algorithmic trading over business intelligence and data science?",
        "Yes -> Quantitative Finance & Modeling | No -> Data Science & Business Intelligence",
        create_leaf_node(c_quant, "leaf_quant"),
        create_leaf_node(c_data, "leaf_data"),
        "n_4d"
    );

    DecisionNode* n_4e = create_decision_node(
        "Do you enjoy conducting user interviews, usability audits, and psychological research more than crafting pixel-perfect visual design systems?",
        "Yes -> UX Research & Usability | No -> UI Design & Design Systems",
        create_leaf_node(c_ux, "leaf_ux"),
        create_leaf_node(c_ui, "leaf_ui"),
        "n_4e"
    );

    DecisionNode* n_4f = create_decision_node(
        "Do you want to pioneer immersive AR/VR virtual spaces and spatial computing rather than commercial brand motion graphics?",
        "Yes -> Spatial Computing & XR Design | No -> Digital Brand & Motion Graphics",
        create_leaf_node(c_xr, "leaf_xr"),
        create_leaf_node(c_motion, "leaf_motion"),
        "n_4f"
    );

    DecisionNode* n_4g = create_decision_node(
        "Do you prefer high-level technology strategy and enterprise advisory consulting over hands-on product feature execution?",
        "Yes -> Tech Strategy & Advisory Consulting | No -> Technical Product Management (TPM)",
        create_leaf_node(c_cons, "leaf_cons"),
        create_leaf_node(c_pm, "leaf_pm"),
        "n_4g"
    );

    DecisionNode* n_4h = create_decision_node(
        "Do you enjoy public developer community advocacy, keynote speaking, and demos more than structured educational curriculum design?",
        "Yes -> Developer Relations (DevRel) | No -> EdTech Instructional Design",
        create_leaf_node(c_devrel, "leaf_devrel"),
        create_leaf_node(c_edtech, "leaf_edtech"),
        "n_4h"
    );

    /* --- LEVEL 3 DECISION NODES --- */
    DecisionNode* n_3a = create_decision_node(
        "Are you more drawn to backend architecture, cloud infrastructure, and security than to interactive user applications and games?",
        "Evaluates preference between infrastructure/foundations vs application-layer engineering.",
        n_4a, n_4b, "n_3a"
    );

    DecisionNode* n_3b = create_decision_node(
        "Are you primarily interested in cutting-edge deep learning and neural models rather than applied analytics and quantitative finance?",
        "Evaluates frontier deep learning vs applied data analytics and financial mathematics.",
        n_4c, n_4d, "n_3b"
    );

    DecisionNode* n_3c = create_decision_node(
        "Are you fascinated by user psychology, wireframing, and intuitive app interfaces over visual storytelling, 3D motion, and multimedia?",
        "Evaluates software interface & ergonomics vs artistic/spatial digital media.",
        n_4e, n_4f, "n_3c"
    );

    DecisionNode* n_3d = create_decision_node(
        "Do you prefer defining product vision, business strategy, and roadmaps over empowering people, teaching, and developer advocacy?",
        "Evaluates product management/business strategy vs human mentorship, advocacy, and education.",
        n_4g, n_4h, "n_3d"
    );

    /* --- LEVEL 2 DECISION NODES --- */
    DecisionNode* n_2a = create_decision_node(
        "Do you prefer building software architectures, systems, and platforms rather than analyzing data patterns and AI algorithms?",
        "Distinguishes core software systems from data science, machine learning, and quantitative finance.",
        n_3a, n_3b, "n_2a"
    );

    DecisionNode* n_2b = create_decision_node(
        "Do you lean more toward visual, interactive design, and sensory digital experiences rather than business leadership and product strategy?",
        "Distinguishes visual/creative interface craft from product management, strategy, and education.",
        n_3c, n_3d, "n_2b"
    );

    /* --- LEVEL 1 ROOT DECISION NODE --- */
    DecisionNode* root = create_decision_node(
        "Do you prefer technical, analytical, and systems-oriented problem solving over creative, design, or human-centric strategy?",
        "The fundamental root split: Engineering, Data & Systems vs Design, Product Strategy & People.",
        n_2a, n_2b, "root"
    );

    return root;
}

/* --- DEPTH-FIRST SEARCH (DFS) WITH BACKTRACKING --- */
int find_path_to_career(DecisionNode* root, const char* target_title,
                        DecisionNode* path_nodes[], int path_answers[], int* path_len) {
    if (!root) return 0;

    path_nodes[*path_len] = root;

    if (is_leaf(root)) {
        if (root->career && strcasecmp(root->career->title, target_title) == 0) {
            (*path_len)++;
            return 1;
        }
        return 0;
    }

    /* Try Yes (left branch) */
    path_answers[*path_len] = 1;
    (*path_len)++;
    if (find_path_to_career(root->yes, target_title, path_nodes, path_answers, path_len)) {
        return 1;
    }
    (*path_len)--; /* Backtrack! */

    /* Try No (right branch) */
    path_answers[*path_len] = 0;
    (*path_len)++;
    if (find_path_to_career(root->no, target_title, path_nodes, path_answers, path_len)) {
        return 1;
    }
    (*path_len)--; /* Backtrack! */

    return 0;
}

/* --- BREADTH-FIRST SEARCH (BFS) / LEVEL-ORDER TRAVERSAL --- */
void print_bfs_traversal(DecisionNode* root) {
    if (!root) return;
    Queue q;
    queue_init(&q);
    queue_enqueue(&q, root, 0);

    int current_level = -1;
    printf("\n=== BREADTH-FIRST SEARCH (LEVEL-ORDER) TRAVERSAL ===\n");
    printf("Uses a FIFO Queue to visit all nodes layer-by-layer:\n\n");

    while (!queue_is_empty(&q)) {
        int lvl = 0;
        DecisionNode* curr = queue_dequeue(&q, &lvl);
        if (lvl != current_level) {
            current_level = lvl;
            printf("\n--- LEVEL %d ---\n", current_level);
        }

        if (is_leaf(curr)) {
            printf("  [LEAF] %s (%s)\n", curr->career->title, curr->career->category);
        } else {
            char short_q[55];
            strncpy(short_q, curr->question, 50);
            short_q[50] = '\0';
            strcat(short_q, "...");
            printf("  [DECISION] %s\n", short_q);
            if (curr->yes) queue_enqueue(&q, curr->yes, lvl + 1);
            if (curr->no) queue_enqueue(&q, curr->no, lvl + 1);
        }
    }
    queue_free(&q);
    printf("\nTotal nodes traversed: 31 (15 internal + 16 leaves)\n");
}

/* --- PRE-ORDER DFS TRAVERSAL (Root -> Left -> Right) --- */
void print_preorder_traversal(DecisionNode* root, int depth) {
    if (!root) return;
    int i;
    for (i = 0; i < depth; i++) printf("  ");
    if (is_leaf(root)) {
        printf("|-- [LEAF] %s\n", root->career->title);
    } else {
        char short_q[45];
        strncpy(short_q, root->question, 40);
        short_q[40] = '\0';
        strcat(short_q, "...");
        printf("|-- [DECISION L%d] %s\n", depth, short_q);
        print_preorder_traversal(root->yes, depth + 1);
        print_preorder_traversal(root->no, depth + 1);
    }
}

/* --- IN-ORDER DFS TRAVERSAL (Left -> Root -> Right) --- */
void print_inorder_traversal(DecisionNode* root, int depth) {
    if (!root) return;
    if (root->yes) print_inorder_traversal(root->yes, depth + 1);
    int i;
    for (i = 0; i < depth; i++) printf("  ");
    if (is_leaf(root)) {
        printf("|-- [LEAF] %s\n", root->career->title);
    } else {
        printf("|-- [DECISION L%d]\n", depth);
    }
    if (root->no) print_inorder_traversal(root->no, depth + 1);
}

/* --- RECURSIVE ASCII HIERARCHICAL TREE VISUALIZER --- */
void print_ascii_tree(DecisionNode* root, int depth, const char* prefix, int is_left) {
    if (!root) return;

    printf("%s", prefix);
    printf(is_left ? "|-- [YES] " : "\\-- [NO]  ");

    if (is_leaf(root)) {
        printf("\033[1;32m[MATCH: %s]\033[0m\n", root->career->title);
    } else {
        char short_q[50];
        strncpy(short_q, root->question, 46);
        short_q[46] = '\0';
        strcat(short_q, "...");
        printf("\033[1;34m(Q: %s)\033[0m\n", short_q);

        char new_prefix[256];
        snprintf(new_prefix, sizeof(new_prefix), "%s%s", prefix, is_left ? "|   " : "    ");
        print_ascii_tree(root->yes, depth + 1, new_prefix, 1);
        print_ascii_tree(root->no, depth + 1, new_prefix, 0);
    }
}

/* --- LIFO STACK IMPLEMENTATION --- */
void stack_init(NodeStack* s) {
    s->top = -1;
}

int stack_push(NodeStack* s, DecisionNode* node, int answer) {
    if (s->top >= STACK_CAPACITY - 1) return 0;
    s->top++;
    s->nodes[s->top] = node;
    s->answers[s->top] = answer;
    return 1;
}

DecisionNode* stack_pop(NodeStack* s, int* answer) {
    if (stack_is_empty(s)) return NULL;
    if (answer) *answer = s->answers[s->top];
    DecisionNode* node = s->nodes[s->top];
    s->top--;
    return node;
}

DecisionNode* stack_peek(const NodeStack* s) {
    if (stack_is_empty(s)) return NULL;
    return s->nodes[s->top];
}

int stack_is_empty(const NodeStack* s) {
    return s->top < 0;
}

/* --- FIFO QUEUE IMPLEMENTATION --- */
void queue_init(Queue* q) {
    q->front = NULL;
    q->rear = NULL;
    q->size = 0;
}

void queue_enqueue(Queue* q, DecisionNode* node, int level) {
    QueueNode* new_node = (QueueNode*)malloc(sizeof(QueueNode));
    if (!new_node) return;
    new_node->tree_node = node;
    new_node->level = level;
    new_node->next = NULL;
    if (q->rear == NULL) {
        q->front = q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
    q->size++;
}

DecisionNode* queue_dequeue(Queue* q, int* level) {
    if (queue_is_empty(q)) return NULL;
    QueueNode* temp = q->front;
    DecisionNode* node = temp->tree_node;
    if (level) *level = temp->level;
    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;
    free(temp);
    q->size--;
    return node;
}

int queue_is_empty(const Queue* q) {
    return q->front == NULL;
}

void queue_free(Queue* q) {
    while (!queue_is_empty(q)) {
        queue_dequeue(q, NULL);
    }
}

/* --- REPORT EXPORTER --- */
int export_career_dossier(const CareerProfile* c, DecisionNode* path_nodes[], 
                          const int path_answers[], int path_len, const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (!fp) return 0;

    fprintf(fp, "================================================================================\n");
    fprintf(fp, "               CAREERTREE ADVISORY REPORT: %s\n", c->title);
    fprintf(fp, "================================================================================\n\n");
    fprintf(fp, "Domain Category:        %s\n", c->category);
    fprintf(fp, "Market Compensation:    %s\n", c->salary_range);
    fprintf(fp, "Industry Demand:        %s\n\n", c->growth_outlook);
    fprintf(fp, "Tagline:\n  \"%s\"\n\n", c->tagline);
    fprintf(fp, "Role Overview:\n  %s\n\n", c->overview);
    fprintf(fp, "Why this matches you:\n  %s\n\n", c->why_match);
    fprintf(fp, "Decision Traversal Path (%d Steps):\n", path_len - 1);

    int i;
    for (i = 0; i < path_len - 1; i++) {
        fprintf(fp, "  %d. %s\n     -> Choice: %s\n", i + 1, path_nodes[i]->question, path_answers[i] ? "YES" : "NO");
    }

    fprintf(fp, "\nKey Competencies:\n");
    for (i = 0; i < c->skill_count; i++) {
        fprintf(fp, "  - %s\n", c->skills[i]);
    }

    fprintf(fp, "\nIndustry Toolchain:\n");
    for (i = 0; i < c->tool_count; i++) {
        fprintf(fp, "  - %s\n", c->tools[i]);
    }

    fprintf(fp, "\n3-Stage Career Roadmap:\n");
    fprintf(fp, "  1. Foundational Stage:\n     %s\n", c->roadmap_foundational);
    fprintf(fp, "  2. Intermediate Stage:\n     %s\n", c->roadmap_intermediate);
    fprintf(fp, "  3. Advanced Stage:\n     %s\n", c->roadmap_advanced);

    fprintf(fp, "\n================================================================================\n");
    fprintf(fp, "Generated by CareerTree (C Implementation) - Pure Binary Decision Tree Engine\n");
    fclose(fp);
    return 1;
}
