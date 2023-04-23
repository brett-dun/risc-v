// Engineer: Brett Duncan
//
// Create Date: 11/07/2022 03:58:32 PM
// Module Name: alu


module alu(
    output reg [31:0] result,
    output reg ready,
    input clk,
    input [31:0] op1,
    input [31:0] op2,
    input [2:0] alu_code
    );

// Set outputs to start with a known value
initial result = 0;
initial ready = 0;

// ALU Instructions
localparam ADD = 3'h1;
localparam SUB = 3'h2;
localparam AND = 3'h3;
localparam OR  = 3'h4;
localparam SLL = 3'h5;
localparam SRL = 3'h6;
localparam NOP = 3'h0;

always @(posedge clk) begin
    case (alu_code)
        ADD: begin
            result <= op1 + op2;
	    ready <= 1;
	end
	SUB: begin
            result <= op1 - op2;
	    ready <= 1;
	end
	AND: begin
            result <= op1 & op2;
	    ready <= 1;
	end
	OR: begin
            result <= op1 | op2;
	    ready <= 1;
	end
        SLL: begin
            result <= op1 << op2;
	    ready <= 1;
	end
	SRL: begin
            result <= op1 >> op2;
	    ready <= 1;
        end
	NOP: begin
	    result <= 0;
	    ready <= 0;
        end
    endcase
end

endmodule

