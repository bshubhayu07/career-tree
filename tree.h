/**
 * tree.h - Header file for CareerTree Binary Decision Tree Engine in Pure C.
 * 
 * Defines the core node structures, career profile metadata, LIFO Stack for
 * backtracking, FIFO Queue for BFS traversal, and algorithmic prototypes.
 */

#ifndef TREE_H
#define TREE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TITLE_LEN 128
#define MAX_CATEGORY_LEN 64
#define MAX_TAGLINE_LEN 256
#define MAX_TEXT_LEN 512
#define MAX_SKILLS 6
#define MAX_TOOLS 6
#define MAX_STR_LEN 64
#define STACK_CAPACITY 32

/* Career Profile Metadata Structure (stored in Leaf nodes) */
typedef struct CareerProfile {
    char title[MAX_TITLE_LEN];
    char category[MAX_CATEGORY_LEN];
    char tagline[MAX_TAGLINE_LEN];
    char overview[MAX_TEXT_LEN];
    char why_match[MAX_TEXT_LEN];
    char skills[MAX_SKILLS][MAX_STR_LEN];
    int skill_count;
    char tools[MAX_TOOLS][MAX_STR_LEN];
    int tool_count;
    char certifications[3][MAX_STR_LEN];
    int cert_count;
    char salary_range[MAX_STR_LEN];
    char growth_outlook[MAX_STR_LEN];
    char day_in_the_life[MAX_TEXT_LEN];
    char roadmap_foundational[MAX_TEXT_LEN];
    char roadmap_intermediate[MAX_TEXT_LEN];
    char roadmap_advanced[MAX_TEXT_LEN];
} CareerProfile;

/* Binary Decision Tree Node */
typedef struct DecisionNode {
    char question[MAX_TEXT_LEN];       /* Question string (NULL if leaf) */
    char context_tip[MAX_TEXT_LEN];     /* Guidance tip explaining context */
    struct DecisionNode* yes;          /* Pointer to Left child (Yes choice) */
    struct DecisionNode* no;           /* Pointer to Right child (No choice) */
    CareerProfile* career;             /* Pointer to CareerProfile (NULL if internal) */
    char node_id[32];                  /* Identifier (e.g., 'root', 'leaf_cyber') */
} DecisionNode;

/* LIFO Stack for Session State Backtracking (Undo) */
typedef struct NodeStack {
    DecisionNode* nodes[STACK_CAPACITY];
    int answers[STACK_CAPACITY];       /* 1 for Yes, 0 for No */
    int top;
} NodeStack;

/* FIFO Queue Node for Breadth-First Search (Level-Order BFS) */
typedef struct QueueNode {
    DecisionNode* tree_node;
    int level;
    struct QueueNode* next;
} QueueNode;

/* FIFO Queue for BFS */
typedef struct Queue {
    QueueNode* front;
    QueueNode* rear;
    int size;
} Queue;

/* --- FUNCTION PROTOTYPES --- */

/* Node and Tree Allocation / Deallocation */
DecisionNode* create_decision_node(const char* question, const char* context_tip, 
                                  DecisionNode* yes, DecisionNode* no, const char* node_id);
DecisionNode* create_leaf_node(CareerProfile* career, const char* node_id);
CareerProfile* create_career_profile(
    const char* title, const char* category, const char* tagline, const char* overview,
    const char* why_match, const char* skills[], int skill_count,
    const char* tools[], int tool_count, const char* certs[], int cert_count,
    const char* salary, const char* growth, const char* day_life,
    const char* road_f, const char* road_i, const char* road_a
);
DecisionNode* build_career_tree(void);
void free_tree(DecisionNode* root);

/* Tree Properties & Metrics */
int is_leaf(const DecisionNode* node);
int count_nodes(const DecisionNode* root);
int count_leaves(const DecisionNode* root);
int get_tree_height(const DecisionNode* root);
int is_tree_balanced(const DecisionNode* root, int* height);

/* Search and Traversals */
int find_path_to_career(DecisionNode* root, const char* target_title,
                        DecisionNode* path_nodes[], int path_answers[], int* path_len);
void print_bfs_traversal(DecisionNode* root);
void print_preorder_traversal(DecisionNode* root, int depth);
void print_inorder_traversal(DecisionNode* root, int depth);
void print_ascii_tree(DecisionNode* root, int depth, const char* prefix, int is_left);

/* Stack Operations (LIFO) */
void stack_init(NodeStack* s);
int stack_push(NodeStack* s, DecisionNode* node, int answer);
DecisionNode* stack_pop(NodeStack* s, int* answer);
DecisionNode* stack_peek(const NodeStack* s);
int stack_is_empty(const NodeStack* s);

/* Queue Operations (FIFO) */
void queue_init(Queue* q);
void queue_enqueue(Queue* q, DecisionNode* node, int level);
DecisionNode* queue_dequeue(Queue* q, int* level);
int queue_is_empty(const Queue* q);
void queue_free(Queue* q);

/* Report Generator */
int export_career_dossier(const CareerProfile* career, DecisionNode* path_nodes[], 
                          const int path_answers[], int path_len, const char* filename);

#endif /* TREE_H */
