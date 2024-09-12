"""An assembler for the BRU symbolic regex virtual machine assembly language (BRU Assembly)"""


def get_instr_c_lines(instr_kw, line, line_num):
    c_lines = []
    match instr_kw:
        # Instructions with no operands
        case "noop":
            # TODO
            raise NotImplementedError("Not implemented")
        case "match":
            # TODO
            c_lines = [r'printf("match\n");', "goto basm_end;"]
        case "begin":
            c_lines = ["if (thread->sp != text) kill(thread);"]
            raise NotImplementedError("Not implemented")
        case "end":
            c_lines = ["if (*thread->sp != '\00') kill(thread);"]
            raise NotImplementedError("Not implemented")
        case "state":
            # TODO
            raise NotImplementedError("Not implemented")
        # Instructions with one char operand
        case "char":
            codepoint = line.split()[1]
            c_lines = [
                f'codepoint = "{codepoint}";',
                "if (strncmp(thread->sp, codepoint, strlen(codepoint)) == 0)",
                "    thread->sp += strlen(codepoint);",
                "else",
                "    kill(thread);",
            ]
        # Instructiosn with one int operand
        case "epsreset":
            # TODO
            raise NotImplementedError("Not implemented")
        case "epsset":
            j = line.split()[1]
            c_lines = [f"eps_sps[{j}] = thread->sp;"]
        case "epschk":
            j = line.split()[1]
            c_lines = [f"if (eps_sps[{j}] == thread->sp) kill(thread);"]
        case "inc":
            # TODO
            raise NotImplementedError("Not implemented")
        case "memo":
            j = line.split()[1]
            c_lines = [
                f"memo[{j}][thread->sp - text] ? kill(thread) : memo[{j}][thread->sp - text] = 1;"
            ]
            raise NotImplementedError("Not implemented")
        case "save":
            j = line.split()[1]
            c_lines = [f"thread->saved_sps[{j}] = thread->sp;"]
        case "pred":
            # TODO
            raise NotImplementedError("Not implemented")
        case "jmp":
            dest = line.split()[1]
            c_lines = [
                f"goto basm_line_{dest};",
            ]
        case "gsplit":
            # TODO
            raise NotImplementedError("Not implemented")
        case "lsplit":
            # TODO
            raise NotImplementedError("Not implemented")
        case "split":
            d1, d2 = line.replace(",", "").split()[1:]

            c_lines = [
                f"vp_stack_push(thread_stack, new_Thread(thread->sp, &&basm_line_{d2}));",
                f"goto basm_line_{d1};",
            ]
        case "zwa":
            raise NotImplementedError("Not implemented")
        case "tswitch":
            raise NotImplementedError("Not implemented")
        case "reset":
            raise NotImplementedError("Not implemented")
        case "cmp":
            raise NotImplementedError("Not implemented")
        case _:
            raise NotImplementedError("Not implemented")
    c_lines = [f"basm_line_{line_num}: // {line}"] + list(
        map(lambda x: f"    {x}\n", c_lines)
    )
    return c_lines


def assemble(basm_file_name):
    basm_file = open(basm_file_name, "r")
    prog_c_lines = []
    num_epssets = 0
    num_captures = 0
    for line_num, line in enumerate(basm_file.readlines()):
        instr_kw = line.split()[0]
        if instr_kw == "epsset":
            num_epssets += 1
        elif instr_kw == "save":
            num_captures += 1
        instr_c_lines = get_instr_c_lines(instr_kw, line, line_num)
        prog_c_lines.extend(instr_c_lines)
    basm_file.close()

    prog_c_lines = "".join(prog_c_lines)

    c_file_name = "src/template.c"
    with open(c_file_name, "r") as c_file:
        template = c_file.read()
    c_code = template.replace(
        "// Placeholder macro definitions (to be replaced by the assembler, `basm.py`)\n#define NUM_CAPTURES 0\n#define NUM_EPSSETS 0",
        f"#define NUM_CAPTURES {num_captures}\n#define NUM_EPSSETS {num_epssets}",
    )

    prog_c_lines = "".join(prog_c_lines)
    c_code = c_code.replace("    // CODE HERE\n", prog_c_lines)
    print(c_code)


if __name__ == "__main__":
    import sys

    basm_file_name = sys.argv[1]
    assemble(basm_file_name)
