// Engineer: Brett Duncan
//
// Create Date: 10/27/2022 02:13:22 PM
// Module Name: program_counter


module program_counter(
    output reg [9:0] addr,
    output reg start,
    input clk,
    input nxt,
    input override_en,
    input [9:0] override_pc
    );

// Set outputs to start with a known value
initial addr = 0;
initial start = 0;

// Register used to prevent incrementing pc multiple times on a single button
// press
reg last = 0;

always @(posedge clk) begin
    if (nxt & ~last) begin
        if (override_en) begin
            addr <= override_pc;
	end else begin
	    // only addressable every 4 bytes
	    addr <= addr + 4;
	end
	start <= 1;
    end else begin
        start <= 0;
    end
    last <= nxt;
end

endmodule

