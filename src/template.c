#include "../c-lib-stack/src/stack.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Placeholder macro definitions (to be replaced by the assembler, `basm.py`)
#define NUM_CAPTURES 0
#define NUM_EPSSETS  0

#define basm_line(i) basm_line_##i

#define kill(thread)       \
    do {                   \
        free(thread);      \
        thread = NULL;     \
        goto control_unit; \
    } while (0)

typedef char byte;

typedef struct thread {
    const char *sp;
    byte       *pc;
    const char *saved_sps[NUM_CAPTURES];
} Thread;

/**
 * @brief Create a new thread.
 *
 * @param sp A pointer to the current position in the input string.
 * @param pc A pointer to the current position in the program.
 */
Thread *new_Thread(const char *sp, byte *pc)
{
    Thread *thread = malloc(sizeof(Thread));
    *thread        = (Thread){ .sp = sp, .pc = pc };
    for (size_t i = 0; i < NUM_CAPTURES; i++) thread->saved_sps[i] = NULL;
    return thread;
}

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <text>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *text = argv[1];
    const char *eps_sps[NUM_EPSSETS];
    for (size_t i = 0; i < NUM_EPSSETS; i++) eps_sps[i] = NULL;
    const char *codepoint    = NULL;
    vp_stack_t *thread_stack = vp_stack_new();
    Thread     *thread       = new_Thread(text, &&basm_start);

    vp_stack_push(thread_stack, thread);

control_unit:
    thread = vp_stack_pop(thread_stack);
    if (thread)
        goto * thread->pc;
    else
        goto basm_no_match;
basm_start:

    // CODE HERE

basm_no_match:
    printf("No match\n");
basm_end:
    return EXIT_SUCCESS;
}
