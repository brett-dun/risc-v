// Engineer: Brett Duncan
//
// Create Date: 11/07/2022 04:27:44 PM
// Module Name: decode


module decode(
    output reg [4:0] rs1,
    output reg [4:0] rs2,
    output reg [4:0] rd,
    output reg read_en,
    output reg [2:0] alu_code,
    input clk,
    input start,
    input [31:0] inst
    );

// Set outputs to start with a known value
initial rs1 = 0;
initial rs2 = 0;
initial rd = 0;
initial read_en = 0;
initial alu_code = 0;

// Instruction opcodes
localparam R = 7'b0110011;
localparam I = 7'b0010011;
localparam S = 7'b0100011;
localparam SB = 7'b1100011;
localparam UJ = 7'b1101111;

// ALU Instructions
localparam ADD = 3'h1;
localparam SUB = 3'h3;
localparam AND = 3'h3;
localparam OR  = 3'h4;
localparam SLL = 3'h5;
localparam SRL = 3'h6;
localparam NOP = 3'h0;

// Registers used for implementing a delayed output
reg [2:0] alu_code_1 = 0;
reg [4:0] rd_1 = 0;
reg [4:0] rd_2 = 0;

// Wires for R-type instructions
wire [6:0] opcode = inst[6:0];
wire [4:0] R_rd = inst[11:7];
wire [2:0] R_funct3 = inst[14:12];
wire [4:0] R_rs1 = inst[19:15];
wire [4:0] R_rs2 = inst[24:20];
wire [6:0] R_funct7 = inst[31:25];

always @(posedge clk) begin

    // 1 cycle behind
    rs1 <= start ? R_rs1 : 0;
    rs2 <= start ? R_rs2 : 0;
    read_en <= start;
    
    // 2 cycles behind
    if (start) begin
        case (opcode)
            R: begin
                case (R_funct3)
                    3'h0: begin
                        alu_code_1 <= (R_funct7 == 7'h00) ? ADD : SUB;
                    end
		    3'h7: begin
			alu_code_1 <= AND;
		    end
		    3'h6: begin
			alu_code_1 <= OR;
		    end
		    3'h1: begin
		        alu_code_1 <= SLL;
		    end
		    3'h5: begin
			alu_code_1 <= SRL;
		    end
		    default begin
	                alu_code_1 <= 0;
		    end
		endcase
	    end
	    default begin
	        alu_code_1 <= 0;
	    end
	endcase
    end else begin
        alu_code_1 <= 0;
    end
    alu_code <= alu_code_1;

    // 3 cycles behind
    rd_2 <= start ? R_rd : 0;
    rd_1 <= rd_2;
    rd <= rd_1;

end

endmodule

