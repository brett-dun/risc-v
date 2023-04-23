// Engineer: Brett Duncan
//
// Create Date: 10/27/2022 02:05:47 PM
// Module Name: instruction_memory


module instruction_memory(
    output reg [31:0] inst,
    output reg start,
    input clk,
    input [9:0] pc,
    input read_en
    );

// Set outputs to start with a known value
initial inst = 0;
initial start = 0;

// 128 x 32-bit wide memory
reg [31:0] memory [0:127];

wire [6:0] addr;
assign addr = pc[9:2]; // Memory is only addressable every 4 bytes;

initial begin
    $readmemh("week2_demo.mem", memory, 0, 127);
end

always @(posedge clk) begin
    if (read_en) begin
        inst <= memory[addr];
    end
    start <= read_en;
end

endmodule

