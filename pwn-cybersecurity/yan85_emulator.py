import re
import sys

REGISTER_MAP = {
    2: 1024,
    1: 1025,
    4: 1026,
    64: 1027,
    32: 1028,
    8: 1029,
    16: 1030,
}

REGISTER_CHARS = {
    2: 'a',
    1: 'b',
    4: 'c',
    64: 'd',
    32: 's',
    8: 'i',
    16: 'f',
}

REGISTER_KEYS = {
    'a': 2,
    'b': 1,
    'c': 4,
    'd': 64,
    's': 32,
    'i': 8,
    'f': 16,
}

def read_register(mem, reg_code):
    if reg_code not in REGISTER_MAP:
        print(f"Error: Attempted to read unknown register code {reg_code}")
        return 0
    return mem[REGISTER_MAP[reg_code]] % 256

def write_register(mem, reg_code, val):
    if reg_code not in REGISTER_MAP:
        print(f"Error: Attempted to write unknown register code {reg_code} with value {val:02X}")
        return
    mem[REGISTER_MAP[reg_code]] = val % 256

def read_memory(mem, addr):
    if not (0 <= addr < len(mem)):
        print(f"Error: Attempted to read memory out of bounds at address {addr:04X}")
        return 0
    return mem[addr] % 256

def write_memory(mem, addr, val):
    if not (0 <= addr < len(mem)):
        print(f"Error: Attempted to write memory out of bounds at address {addr:04X} with value {val:02X}")
        return
    mem[addr] = val % 256

def interpret_imm(mem, dst_reg_code, imm_value):
    print(f"(IMM) : {REGISTER_CHARS.get(dst_reg_code,'?')} = {imm_value:02X}")
    write_register(mem, dst_reg_code, imm_value)

def interpret_add(mem, dst_reg_code, src_reg_code):
    print(f"(ADD) : {REGISTER_CHARS.get(dst_reg_code,'?')} += {REGISTER_CHARS.get(src_reg_code,'?')}")
    res = (read_register(mem, dst_reg_code) + read_register(mem, src_reg_code)) % 256
    write_register(mem, dst_reg_code, res)

def interpret_stm(mem, addr_reg_code, value_reg_code):
    print(f"(STM) : *{REGISTER_CHARS.get(addr_reg_code,'?')} = {REGISTER_CHARS.get(value_reg_code,'?')}")
    addr = read_register(mem, addr_reg_code)
    value = read_register(mem, value_reg_code)
    write_memory(mem, addr, value)

def interpret_ldm(mem, dst_reg_code, addr_reg_code):
    print(f"(LDM) : {REGISTER_CHARS.get(dst_reg_code,'?')} = *{REGISTER_CHARS.get(addr_reg_code,'?')}")
    addr = read_register(mem, addr_reg_code)
    value = read_memory(mem, addr)
    write_register(mem, dst_reg_code, value)

def interpret_stk(mem, pop_reg_code, push_reg_code):
    print(f"(STK) : pop={REGISTER_CHARS.get(pop_reg_code,'?')} push={REGISTER_CHARS.get(push_reg_code,'?')}")
    if push_reg_code != 0:
        print(f"[s] ... pushing {REGISTER_CHARS.get(push_reg_code,'?')}")
        sp = (read_register(mem, REGISTER_KEYS.get("s")) + 1) % 256
        write_register(mem, REGISTER_KEYS.get("s"), sp)
        push_value = read_register(mem, push_reg_code)
        write_memory(mem, sp, push_value)
    if pop_reg_code != 0:
        print(f"[s] ... popping {REGISTER_CHARS.get(pop_reg_code,'?')}")
        sp = read_register(mem, REGISTER_KEYS.get("s"))
        pop_value = read_memory(mem, sp)
        write_register(mem, pop_reg_code, pop_value)
        write_register(mem, REGISTER_KEYS.get("s"), (sp - 1) % 256)

def describe_flags(flag_byte):
    flag_description = []
    if (flag_byte & 0x08) != 0:
        flag_description.append('L')
    if (flag_byte & 0x01) != 0:
        flag_description.append('G')
    if (flag_byte & 0x04) != 0:
        flag_description.append('E')
    if (flag_byte & 0x10) != 0:
        flag_description.append('N')
    if (flag_byte & 0x02) != 0:
        flag_description.append('Z')
    if not flag_byte:
        flag_description.append('*')
    return "".join(flag_description)

def interpret_cmp(mem, arg1_reg_code, arg2_reg_code):
    print(f"[s] CMP {REGISTER_CHARS.get(arg1_reg_code,'?')} {REGISTER_CHARS.get(arg2_reg_code,'?')}")
    v5_val = read_register(mem, arg1_reg_code)
    v6_val = read_register(mem, arg2_reg_code)
    current_flags = 0
    if v5_val < v6_val:
        current_flags |= 0x08
    if v5_val > v6_val:
        current_flags |= 0x01
    if v5_val == v6_val:
        current_flags |= 0x04
    if v5_val != v6_val:
        current_flags |= 0x10
    if v5_val == 0 and v6_val == 0:
        current_flags |= 0x02
    write_register(mem, REGISTER_KEYS.get("f"), current_flags)

def interpret_jmp(mem, flags_to_check, target_reg_code):
    flags_str = describe_flags(flags_to_check)
    target_reg_char = REGISTER_CHARS.get(target_reg_code, '?')
    print(f"[j] JMP {flags_str} {target_reg_char}")
    current_flags = read_register(mem, REGISTER_KEYS.get("f"))
    jump_taken = False
    if flags_to_check == 0:
        jump_taken = True
    elif (flags_to_check & current_flags) != 0:
        jump_taken = True
    if not jump_taken:
        print("[j] ... NOT TAKEN")
        return False
    else:
        print("[j] ... TAKEN")
        jump_destination_instruction_index = read_register(mem, target_reg_code)
        write_register(mem, REGISTER_KEYS.get("i"), jump_destination_instruction_index)
        return True

def interpret_sys(mem, arg1_value, arg2_value):
    if arg1_value == 0x20:
        print("SYS WRITE")
    if arg1_value == 0x8:
        print("SYS READ")
    if arg2_value == 0x0:
        print("SYS called with arg2=0. Signaling halt.")
        return 88
    else:
        print(f"SYS called with arg2={arg2_value:02X}. Continuing.")
        return 100

INSTR = {
    0x08: interpret_imm,
    0x04: interpret_add,
    0x10: interpret_stm,
    0x20: interpret_ldm,
    0x02: interpret_stk,
    0x80: interpret_cmp,
    0x40: interpret_jmp,
    0x01: interpret_sys,
}

try:
    with open('rame.txt', 'r') as f:
        data = f.read()
except FileNotFoundError:
    print("Error: rame.txt not found.")
    sys.exit(1)

bytes_str = re.findall(r'[0-9A-Fa-f]{2}', data)
code = [int(b, 16) for b in bytes_str]

print(f"Loaded {len(code)} bytes of bytecode.")
memory_size = 2048
memory = [0] * memory_size

write_register(memory, REGISTER_KEYS.get("i"), 0)
write_register(memory, REGISTER_KEYS.get("s"), 0)
write_register(memory, REGISTER_KEYS.get("f"), 0)

iterations = 0
max_iterations = 10000

print("\n--- Starting Emulation ---")

while iterations < max_iterations:
    current_i = read_register(memory, REGISTER_KEYS.get("i"))
    byte_index = current_i * 3
    if byte_index + 2 >= len(code):
        print(f"Halt: Attempted to read instruction {current_i} outside code bounds (byte index {byte_index:04X}). Code size is {len(code)} bytes.")
        break
    b0_arg2 = code[byte_index]
    b1_op = code[byte_index + 1]
    b2_arg1 = code[byte_index + 2]
    next_i = (current_i + 1) % 256
    write_register(memory, REGISTER_KEYS.get("i"), next_i)
    if b1_op not in INSTR:
        print(f"Halt: Unknown opcode {b1_op:02X} at instruction index {current_i} (byte index {byte_index:04X}).")
        break
    handler = INSTR[b1_op]
    if b1_op == 0x40:
        handler(memory, b2_arg1, b0_arg2)
    elif b1_op == 0x01:
        sys_result = handler(memory, b2_arg1, b0_arg2)
        if sys_result == 88:
            print("Halt: SYS command signaled halt.")
            break
    else:
        handler(memory, b2_arg1, b0_arg2)
    iterations += 1

print(f"\n--- Emulation finished after {iterations} iterations ---")

print("\n--- Memory Dump ---")
with open("memory.dump", "w") as f:
    dump_limit = max(max(REGISTER_MAP.values()) + 1, 512)
    dump_limit = min(dump_limit, len(memory))
    for i in range(dump_limit):
        f.write(f"{i:04X}: {memory[i]:02X}\n")
    f.write("\n--- Register Values ---\n")
    sorted_regs = sorted(REGISTER_MAP.items(), key=lambda item: item[1])
    for reg_code, mem_index in sorted_regs:
        reg_char = REGISTER_CHARS.get(reg_code, '?')
        value = memory[mem_index]
        f.write(f"{reg_char} ({reg_code:02X}): {value:02X} (Mem[{mem_index:04X}])\n")

print("Memory and Register state dumped to memory.dump")

