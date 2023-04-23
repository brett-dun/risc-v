// Engineer: Brett Duncan
//
// Create Date: 10/27/2022 09:23:58 PM
// Module Name: riscv_top


`include "riscv_internal.v"

module riscv_top(
    output [15:0] leds,
    input clk,
    input btn,
    input rst
    );

// outputs
wire [9:0] pc;
wire mem_start;
wire decode_start;
wire [31:0] inst;
wire [4:0] rs1;
wire [4:0] rs2;
wire [4:0] rd;
wire read_en;
wire [2:0] alu_code;
wire [31:0] r1;
wire [31:0] r2;
wire [31:0] reg31;
wire [31:0] alu_result;
wire result_ready;

assign leds[15:0] = reg31[15:0];

riscv_internal cpu(pc, mem_start, decode_start, inst, rs1, rs2, rd, read_en, alu_code, r1, r2, reg31, alu_result, result_ready, clk, btn, rst);

endmodule

