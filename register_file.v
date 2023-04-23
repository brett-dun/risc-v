// Engineer: Brett Duncan
//
// Create Date: 10/27/2022 02:50:28 PM
// Module Name: register_file


module register_file(
    output reg [31:0] r1,
    output reg [31:0] r2,
    output [31:0] reg31,
    input clk,
    input [4:0] rs1,
    input [4:0] rs2,
    input [4:0] rd,
    input [31:0] dest_val,
    input read_en,
    input write_en,
    input rst
    );

// Set outputs to start with a known value
initial r1 = 0;
initial r2 = 0;

// 32 x 32-bit wide registers are available
reg [31:0] registers [0:31];

// seeing what is in reg31 will be helpful for week 2 of the lab
assign reg31 = registers[31];

integer i;
initial begin
    // initialize registers to the value of their index
    for (i=0; i < 32; i = i + 1) begin
        registers[i] = i;
    end
end

always @(posedge clk) begin
    // Reset to the value equal to the register index
    if (rst) begin
        registers[0] <= 0;
	registers[1] <= 1;
	registers[2] <= 2;
	registers[3] <= 3;
	registers[4] <= 4;
	registers[5] <= 5;
	registers[6] <= 6;
	registers[7] <= 7;
	registers[8] <= 8;
	registers[9] <= 9;
	registers[10] <= 10;
	registers[11] <= 11;
	registers[12] <= 12;
	registers[13] <= 13;
	registers[14] <= 14;
	registers[15] <= 15;
	registers[16] <= 16;
	registers[17] <= 17;
	registers[18] <= 18;
	registers[19] <= 19;
	registers[20] <= 20;
	registers[21] <= 21;
	registers[22] <= 22;
	registers[23] <= 23;
	registers[24] <= 24;
	registers[25] <= 25;
	registers[26] <= 26;
	registers[27] <= 27;
	registers[28] <= 28;
	registers[29] <= 29;
	registers[30] <= 30;
	registers[31] <= 31;
    end
    // Read the values at the given addresses
    if (read_en) begin
        r1 <= registers[rs1];
	r2 <= registers[rs2];
    end else begin
        r1 <= 0;
	r2 <= 0;
    end
    // Write to the destination
    if (write_en) begin
        registers[rd] <= dest_val;
    end
end

endmodule

