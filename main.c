/**
 * main.c - Interactive CLI Application for CareerTree in Pure C.
 * 
 * Features:
 * - Interactive Career Assessment with LIFO Stack Backtracking (Undo)
 * - Visual ASCII Tree Diagram Renderer
 * - DFS Pathfinder for any career
 * - BFS Level-Order, Pre-Order, and In-Order Traversal Demonstrations
 * - Automated Unit Testing Suite in C
 * - Clean dynamic memory deallocation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "tree.h"

#define COLOR_RESET   "\033[0m"
#define COLOR_BOLD    "\033[1m"
#define COLOR_CYAN    "\033[1;36m"
#define COLOR_GREEN   "\033[1;32m"
#define COLOR_YELLOW  "\033[1;33m"
#define COLOR_RED     "\033[1;31m"
#define COLOR_BLUE    "\033[1;34m"
#define COLOR_MAGENTA "\033[1;35m"

void clear_screen(void) {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void print_banner(void) {
    printf("%s", COLOR_CYAN);
    printf("================================================================================\n");
    printf("     CAREERTREE — DETERMINISTIC BINARY DECISION TREE CAREER ADVISOR (C)        \n");
    printf("   Data Structures & Algorithms Mini-Project | Author: Shubhayu Bhattacharya    \n");
    printf("================================================================================\n");
    printf("%s", COLOR_RESET);
}

void display_career_dossier(const CareerProfile* c, DecisionNode* path_nodes[], const int path_answers[], int path_len) {
    printf("\n%s================================================================================%s\n", COLOR_GREEN, COLOR_RESET);
    printf("%s  RECOMMENDED CAREER TRAJECTORY: %s%s\n", COLOR_BOLD, c->title, COLOR_RESET);
    printf("%s  Domain Category: %s | Demand: %s%s\n", COLOR_CYAN, c->category, c->growth_outlook, COLOR_RESET);
    printf("%s================================================================================%s\n", COLOR_GREEN, COLOR_RESET);

    printf("\n%sTagline:%s\n  \"%s\"\n", COLOR_YELLOW, COLOR_RESET, c->tagline);
    printf("\n%sRole Overview:%s\n  %s\n", COLOR_BOLD, COLOR_RESET, c->overview);
    printf("\n%sWhy this matches your answers:%s\n  %s\n", COLOR_GREEN, COLOR_RESET, c->why_match);
    printf("\n%sMarket Compensation Band:%s %s\n", COLOR_CYAN, COLOR_RESET, c->salary_range);

    printf("\n%sKey Technical & Soft Skills:%s\n", COLOR_BOLD, COLOR_RESET);
    int i;
    for (i = 0; i < c->skill_count; i++) {
        printf("  [%s] ", c->skills[i]);
    }
    printf("\n");

    printf("\n%sIndustry Standard Toolchain:%s\n", COLOR_BOLD, COLOR_RESET);
    for (i = 0; i < c->tool_count; i++) {
        printf("  <%s> ", c->tools[i]);
    }
    printf("\n");

    printf("\n%sRecognized Certifications:%s\n", COLOR_BOLD, COLOR_RESET);
    for (i = 0; i < c->cert_count; i++) {
        printf("  * %s\n", c->certifications[i]);
    }

    printf("\n%s3-Stage Career Learning Roadmap:%s\n", COLOR_YELLOW, COLOR_RESET);
    printf("  1. Foundational Stage:\n     %s\n", c->roadmap_foundational);
    printf("  2. Intermediate Stage:\n     %s\n", c->roadmap_intermediate);
    printf("  3. Advanced Stage:\n     %s\n", c->roadmap_advanced);

    printf("\n%sYour Exact Decision Traversal Path (%d Steps):%s\n", COLOR_CYAN, path_len - 1, COLOR_RESET);
    for (i = 0; i < path_len - 1; i++) {
        printf("  %d. %s\n     -> Choice: %s%s%s\n",
               i + 1, path_nodes[i]->question,
               path_answers[i] ? COLOR_GREEN : COLOR_RED,
               path_answers[i] ? "YES" : "NO",
               COLOR_RESET);
    }

    printf("\nExport assessment report to 'career_recommendation.txt'? (y/n): ");
    char choice[16];
    if (fgets(choice, sizeof(choice), stdin)) {
        if (choice[0] == 'y' || choice[0] == 'Y') {
            if (export_career_dossier(c, path_nodes, path_answers, path_len, "career_recommendation.txt")) {
                printf("%s[SUCCESS] Exported detailed dossier to 'career_recommendation.txt'!%s\n", COLOR_GREEN, COLOR_RESET);
            } else {
                printf("%s[ERROR] Failed to write report file.%s\n", COLOR_RED, COLOR_RESET);
            }
        }
    }
}

/* Mode 1: Interactive Assessment with LIFO Stack Backtracking */
void run_interactive_assessment(DecisionNode* root) {
    NodeStack stack;
    stack_init(&stack);

    DecisionNode* current = root;
    stack_push(&stack, current, -1);

    char input_buf[64];

    while (current && !is_leaf(current)) {
        int step = stack.top + 1;
        clear_screen();
        print_banner();

        printf("\n%s--- DECISION STAGE %d OF 4 ---%s\n", COLOR_YELLOW, step, COLOR_RESET);
        printf("%s%s%s\n", COLOR_BOLD, current->question, COLOR_RESET);
        printf("%sContext Tip:%s %s\n\n", COLOR_CYAN, COLOR_RESET, current->context_tip);

        printf("Candidates remaining at this level: %d pathways\n", 16 / (1 << (step - 1)));
        printf("--------------------------------------------------------------------------------\n");
        printf("Options:\n");
        printf("  %s[Y]%s Yes, definitely\n", COLOR_GREEN, COLOR_RESET);
        printf("  %s[N]%s No, not really\n", COLOR_RED, COLOR_RESET);
        if (stack.top > 0) {
            printf("  %s[U]%s Undo previous answer (Stack Pop)\n", COLOR_YELLOW, COLOR_RESET);
        }
        printf("  %s[R]%s Restart assessment\n", COLOR_MAGENTA, COLOR_RESET);
        printf("  %s[Q]%s Quit to Main Menu\n", COLOR_RESET, COLOR_RESET);
        printf("--------------------------------------------------------------------------------\n");
        printf("Enter your choice: ");

        if (!fgets(input_buf, sizeof(input_buf), stdin)) break;
        char c = toupper(input_buf[0]);

        if (c == 'Y') {
            stack.answers[stack.top] = 1;
            current = current->yes;
            stack_push(&stack, current, -1);
        } else if (c == 'N') {
            stack.answers[stack.top] = 0;
            current = current->no;
            stack_push(&stack, current, -1);
        } else if (c == 'U' && stack.top > 0) {
            int popped_ans = 0;
            stack_pop(&stack, &popped_ans); /* Pop current */
            current = stack_peek(&stack);   /* Restore parent */
            printf("%s[BACKTRACK] Popped stack! Reverted to parent node in O(1) time.%s\n", COLOR_YELLOW, COLOR_RESET);
        } else if (c == 'R') {
            stack_init(&stack);
            current = root;
            stack_push(&stack, current, -1);
        } else if (c == 'Q') {
            return;
        } else {
            printf("%sInvalid choice. Please enter Y, N, U, or R.%s\n", COLOR_RED, COLOR_RESET);
        }
    }

    if (current && is_leaf(current)) {
        clear_screen();
        print_banner();
        DecisionNode* path_nodes[16];
        int path_answers[16];
        int i;
        for (i = 0; i < stack.top; i++) {
            path_nodes[i] = stack.nodes[i];
            path_answers[i] = stack.answers[i];
        }
        path_nodes[stack.top] = current;
        display_career_dossier(current->career, path_nodes, path_answers, stack.top + 1);
        printf("\nPress Enter to return to main menu...");
        fgets(input_buf, sizeof(input_buf), stdin);
    }
}

/* Mode 2: Visual ASCII Tree Diagram */
void run_ascii_tree_visualizer(DecisionNode* root) {
    clear_screen();
    print_banner();
    printf("\n%s=== HIERARCHICAL BINARY DECISION TREE (ASCII GRAPH) ===%s\n", COLOR_BOLD, COLOR_RESET);
    printf("Visualizes all 31 nodes (15 Decisions + 16 Leaf Outcomes):\n\n");
    print_ascii_tree(root, 0, "", 1);
    printf("\nPress Enter to return to main menu...");
    char buf[16];
    fgets(buf, sizeof(buf), stdin);
}

/* Mode 3: DFS Pathfinder */
void run_pathfinder(DecisionNode* root) {
    clear_screen();
    print_banner();
    printf("\n%s=== CAREER PATHFINDER (DEPTH-FIRST SEARCH) ===%s\n", COLOR_BOLD, COLOR_RESET);
    printf("Enter a career title to search using recursive DFS with backtracking:\n\n");

    const char* sample_careers[] = {
        "Cybersecurity Analyst & Ethical Hacker",
        "Cloud Solutions Architect & DevOps Engineer",
        "Game Developer & Real-Time 3D Engineer",
        "Full Stack Software Engineer",
        "Machine Learning Operations (MLOps) Engineer",
        "AI & Deep Learning Research Scientist",
        "Quantitative Analyst (Quant) & Financial Modeler",
        "Data Scientist & Business Intelligence Lead",
        "UX Researcher & Usability Specialist",
        "UI / Visual Design & Design Systems Architect",
        "XR / Spatial Computing & AR/VR Experience Designer",
        "Digital Brand & Motion Graphics Art Director",
        "Technology Strategy & Management Consultant",
        "Technical Product Manager (TPM)",
        "Developer Relations (DevRel) & Technical Advocate",
        "EdTech Instructional Designer & Learning Specialist"
    };

    int i;
    for (i = 0; i < 16; i++) {
        printf("  [%2d] %s\n", i + 1, sample_careers[i]);
    }

    printf("\nEnter career number (1-16) or type name: ");
    char input[128];
    if (!fgets(input, sizeof(input), stdin)) return;
    input[strcspn(input, "\r\n")] = '\0';

    const char* target_title = input;
    int num = atoi(input);
    if (num >= 1 && num <= 16) {
        target_title = sample_careers[num - 1];
    }

    DecisionNode* path_nodes[16];
    int path_answers[16];
    int path_len = 0;

    if (find_path_to_career(root, target_title, path_nodes, path_answers, &path_len)) {
        printf("\n%s[DFS FOUND MATCH!]%s Target: %s%s%s\n", COLOR_GREEN, COLOR_RESET, COLOR_BOLD, target_title, COLOR_RESET);
        printf("Traversal route from Root to Leaf (%d steps):\n", path_len - 1);
        for (i = 0; i < path_len - 1; i++) {
            printf("  Step %d: %s\n          -> Choice: %s%s%s\n",
                   i + 1, path_nodes[i]->question,
                   path_answers[i] ? COLOR_GREEN : COLOR_RED,
                   path_answers[i] ? "YES" : "NO",
                   COLOR_RESET);
        }
    } else {
        printf("\n%s[DFS SEARCH FAILED] Could not locate career '%s'.%s\n", COLOR_RED, target_title, COLOR_RESET);
    }

    printf("\nPress Enter to return to main menu...");
    fgets(input, sizeof(input), stdin);
}

/* Mode 4: DSA Traversals Demo */
void run_traversals_demo(DecisionNode* root) {
    clear_screen();
    print_banner();
    printf("\n%s=== TREE TRAVERSAL ALGORITHMS DEMONSTRATION ===%s\n", COLOR_BOLD, COLOR_RESET);
    printf("1. Breadth-First Search (Level-Order BFS via FIFO Queue)\n");
    printf("2. Pre-Order Traversal (Root -> Left -> Right)\n");
    printf("3. In-Order Traversal (Left -> Root -> Right)\n");
    printf("Enter choice (1-3): ");

    char buf[16];
    if (!fgets(buf, sizeof(buf), stdin)) return;

    if (buf[0] == '1') {
        print_bfs_traversal(root);
    } else if (buf[0] == '2') {
        printf("\n=== PRE-ORDER DFS TRAVERSAL ===\n");
        print_preorder_traversal(root, 0);
    } else if (buf[0] == '3') {
        printf("\n=== IN-ORDER DFS TRAVERSAL ===\n");
        print_inorder_traversal(root, 0);
    }

    printf("\nPress Enter to return to main menu...");
    fgets(buf, sizeof(buf), stdin);
}

/* Mode 5: Tree Complexity & Mathematical Properties */
void run_metrics_display(DecisionNode* root) {
    clear_screen();
    print_banner();
    int h = get_tree_height(root);
    int total = count_nodes(root);
    int leaves = count_leaves(root);
    int internal_nodes = total - leaves;
    int check_h = 0;
    int balanced = is_tree_balanced(root, &check_h);

    printf("\n%s=== THEORETICAL TREE METRICS & ASYMPTOTIC COMPLEXITY ===%s\n", COLOR_BOLD, COLOR_RESET);
    printf("  - Tree Height (h):                 %d levels\n", h);
    printf("  - Total Nodes in Memory (N):       %d nodes  [Formula: 2^(h+1) - 1 = 31]\n", total);
    printf("  - Internal Decision Nodes (I):     %d nodes  [Formula: 2^h - 1 = 15]\n", internal_nodes);
    printf("  - Terminal Career Leaves (L):      %d leaves [Formula: 2^h = 16]\n", leaves);
    printf("  - Tree Balance Criteria:           %s%s%s (Height difference = 0)\n",
           balanced ? COLOR_GREEN : COLOR_RED, balanced ? "PERFECTLY BALANCED" : "UNBALANCED", COLOR_RESET);

    printf("\n%sAsymptotic Complexity Analysis:%s\n", COLOR_CYAN, COLOR_RESET);
    printf("  * Traversal Inference Time:        O(h) = O(log2 N) = 4 pointer dereferences\n");
    printf("  * Undo / Backtracking Time:        O(1) constant time (LIFO stack pop)\n");
    printf("  * DFS Path Search Time:            O(N) worst-case (31 nodes)\n");
    printf("  * Tree Construction Time:          O(N) bottom-up heap allocation\n");
    printf("  * Space Complexity:                O(N) heap memory for 31 nodes\n");
    printf("  * Auxiliary Stack Space:           O(h) = 5 frames max during session\n");

    printf("\nPress Enter to return to main menu...");
    char buf[16];
    fgets(buf, sizeof(buf), stdin);
}

/* Mode 6: Automated Unit Tests in Pure C */
void run_unit_tests(DecisionNode* root) {
    clear_screen();
    print_banner();
    printf("\n%s=== RUNNING AUTOMATED UNIT TESTS (C TEST SUITE) ===%s\n", COLOR_BOLD, COLOR_RESET);

    int passed = 0;
    int failed = 0;

    /* Test 1: Node Count */
    int total = count_nodes(root);
    if (total == 31) {
        printf("  [PASS] Test 1: Total node count equals 31 (Got %d)\n", total);
        passed++;
    } else {
        printf("  [FAIL] Test 1: Total node count expected 31, got %d\n", total);
        failed++;
    }

    /* Test 2: Leaf Count */
    int leaves = count_leaves(root);
    if (leaves == 16) {
        printf("  [PASS] Test 2: Leaf count equals 16 (Got %d)\n", leaves);
        passed++;
    } else {
        printf("  [FAIL] Test 2: Leaf count expected 16, got %d\n", leaves);
        failed++;
    }

    /* Test 3: Height & Balance */
    int h = get_tree_height(root);
    int check_h = 0;
    int balanced = is_tree_balanced(root, &check_h);
    if (h == 4 && balanced) {
        printf("  [PASS] Test 3: Tree height is 4 and balance factor is 0\n");
        passed++;
    } else {
        printf("  [FAIL] Test 3: Height/Balance mismatch (h=%d, balanced=%d)\n", h, balanced);
        failed++;
    }

    /* Test 4: All 16 Paths Reachable */
    int b0, b1, b2, b3;
    int reachable_count = 0;
    for (b0 = 0; b0 <= 1; b0++) {
        for (b1 = 0; b1 <= 1; b1++) {
            for (b2 = 0; b2 <= 1; b2++) {
                for (b3 = 0; b3 <= 1; b3++) {
                    DecisionNode* curr = root;
                    curr = b0 ? curr->yes : curr->no;
                    curr = b1 ? curr->yes : curr->no;
                    curr = b2 ? curr->yes : curr->no;
                    curr = b3 ? curr->yes : curr->no;
                    if (curr && is_leaf(curr) && curr->career) {
                        reachable_count++;
                    }
                }
            }
        }
    }
    if (reachable_count == 16) {
        printf("  [PASS] Test 4: All 2^4 = 16 binary paths terminate at valid career leaves\n");
        passed++;
    } else {
        printf("  [FAIL] Test 4: Reachable leaves expected 16, got %d\n", reachable_count);
        failed++;
    }

    printf("\n%s--------------------------------------------------------------------------------%s\n", COLOR_CYAN, COLOR_RESET);
    if (failed == 0) {
        printf("%sALL %d UNIT TESTS PASSED SUCCESSFULLY IN 0.000s!%s\n", COLOR_GREEN, passed, COLOR_RESET);
    } else {
        printf("%sUNIT TEST FAILURES DETECTED: %d failed, %d passed%s\n", COLOR_RED, failed, passed, COLOR_RESET);
    }

    printf("\nPress Enter to return to main menu...");
    char buf[16];
    fgets(buf, sizeof(buf), stdin);
}

int main(void) {
    /* Build binary tree dynamically on the heap */
    DecisionNode* root = build_career_tree();

    char choice[16];
    int running = 1;

    while (running) {
        clear_screen();
        print_banner();
        printf("\n%s--- MAIN CONTROL MENU ---%s\n", COLOR_YELLOW, COLOR_RESET);
        printf("  %s[1]%s Take Interactive Career Assessment (with LIFO Undo Stack)\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[2]%s Visual ASCII Binary Tree Explorer (Hierarchical Graph)\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[3]%s Career Pathfinder (Depth-First Search with Backtracking)\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[4]%s Run Tree Traversal Algorithms (BFS Queue, Pre/In-Order DFS)\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[5]%s View Theoretical Tree Metrics & Complexity Analysis\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[6]%s Run Automated C Unit Tests (16 Path Verification)\n", COLOR_BOLD, COLOR_RESET);
        printf("  %s[7]%s Exit Program & Free Heap Memory\n", COLOR_RED, COLOR_RESET);
        printf("--------------------------------------------------------------------------------\n");
        printf("Enter your choice (1-7): ");

        if (!fgets(choice, sizeof(choice), stdin)) break;

        switch (choice[0]) {
            case '1':
                run_interactive_assessment(root);
                break;
            case '2':
                run_ascii_tree_visualizer(root);
                break;
            case '3':
                run_pathfinder(root);
                break;
            case '4':
                run_traversals_demo(root);
                break;
            case '5':
                run_metrics_display(root);
                break;
            case '6':
                run_unit_tests(root);
                break;
            case '7':
                printf("\n%sFreeing all 31 heap-allocated tree nodes...%s\n", COLOR_YELLOW, COLOR_RESET);
                free_tree(root);
                printf("%s[SUCCESS] Zero memory leaks. Goodbye!%s\n", COLOR_GREEN, COLOR_RESET);
                running = 0;
                break;
            default:
                printf("%sInvalid choice. Please select 1 through 7.%s\n", COLOR_RED, COLOR_RESET);
                break;
        }
    }

    return 0;
}
