// Engineer: Brett Duncan
//
// Create Date: 11/07/2022 09:23:58 PM
// Module Name: riscv_internal


`include "program_counter.v"
`include "instruction_memory.v"
`include "decode.v"
`include "register_file.v"
`include "alu.v"

module riscv_internal(
    output [9:0] pc,
    output mem_start,
    output decode_start,
    output [31:0] inst,
    output [4:0] rs1,
    output [4:0] rs2,
    output [4:0] rd,
    output read_en,
    output [2:0] alu_code,
    output [31:0] r1,
    output [31:0] r2,
    output [31:0] reg31,
    output [31:0] alu_result,
    output result_ready,
    input clk,
    input btn,
    input rst
    );

// things that won't change
reg [9:0] override_pc = 0; // don't worry about override

program_counter Counter(pc, mem_start, clk, btn, rst, override_pc);

instruction_memory ProgramMemory(inst, decode_start, clk, pc, mem_start);

decode Decode(rs1, rs2, rd, read_en, alu_code, clk, decode_start, inst);

register_file RegisterFile(r1, r2, reg31, clk, rs1, rs2, rd, alu_result, read_en, result_ready, rst);

alu ALU(alu_result, result_ready, clk, r1, r2, alu_code);

endmodule

