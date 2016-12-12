use std::io::{self, BufRead};

type Register = usize;

enum Value {
    Register(Register),
    Value(isize),
}

enum Instruction {
    Copy(Value, Register),
    Increment(Register),
    Decrement(Register),
    JumpNotZero(Value, Value),
}

fn parse_register(part: &str) -> Register {
    return (part.chars().next().unwrap() as usize) - 97;
}

fn parse_value(part: &str) -> Value {
    match part.parse::<isize>() {
        Ok(val) => Value::Value(val),
        Err(_) => Value::Register(parse_register(part)),
    }
}

fn parse(line: &str) -> Instruction {
    let parts = line.split(" ").collect::<Vec<_>>();

    match parts[0] {
        "cpy" => Instruction::Copy(parse_value(parts[1]), parse_register(parts[2])),
        "inc" => Instruction::Increment(parse_register(parts[1])),
        "dec" => Instruction::Decrement(parse_register(parts[1])),
        "jnz" => Instruction::JumpNotZero(parse_value(parts[1]), parse_value(parts[2])),
        _ => panic!(),
    }
}

fn execute(ins: &Instruction, registers: &mut [isize], pc: usize) -> usize {
    let val = |regs: &[isize], val| {
        match val {
            &Value::Register(idx) => regs[idx],
            &Value::Value(v) => v,
        }
    };

    match ins {
        &Instruction::Copy(ref from, to) => registers[to] = val(registers, from),
        &Instruction::Increment(reg) => registers[reg] += 1,
        &Instruction::Decrement(reg) => registers[reg] -= 1,
        &Instruction::JumpNotZero(ref cnd, ref tgt) => {
            if val(registers, cnd) != 0 {
                return (pc as isize + val(registers, tgt)) as usize;
            }
        }
    }
    return pc + 1;
}

fn main() {
    let stdin = io::stdin();

    let instructions = stdin.lock().lines().filter_map(|s| s.ok()).take_while(|x| !x.is_empty()).map(|x| parse(&x)).collect::<Vec<_>>();

    let mut regs = [0; 4];
    let mut pc = 0;
    while pc < instructions.len() {
        pc = execute(&instructions[pc], &mut regs, pc);
    }
    println!(" - The value of register a is {} -", regs[0]);
    
    regs = [0, 0, 1, 0];
    pc = 0;
    while pc < instructions.len() {
        pc = execute(&instructions[pc], &mut regs, pc);
    }
    println!(" - The value of register a (with c=1) is {} -", regs[0]);
}
