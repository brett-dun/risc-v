`include "alu.v"

module test_alu_add;

    wire [31:0] result;
    wire ready;

    reg clk = 0;
    reg [31:0] op1;
    reg [31:0] op2;
    reg [2:0] alu_code;

    alu ALU(result, ready, clk, op1, op2, alu_code);
    
    always #5 clk = ~clk;

    initial begin
        $dumpfile("test.vcd");
	$dumpvars;

	// set ALU code to add
	alu_code = 3'h1;

        // 0x0 + 0x0 = 0x0
        op1 = 32'h0;
	op2 = 32'h0;
	#10
        if (result != 32'h0) begin
            $display("result%h (expected=%h)", result, 32'h0);
	    $display("FAIlED: test_alu_add");
            $fatal(1);
	end

	// 0x40 + 0x02 = 0x42
	op1 = 32'h40;
	op2 = 32'h02;
	#10
	if (result != 32'h42) begin
            $display("result=%h (expected=%h)", result, 32'h42);
	    $display("FAILED: test_alu_add");
            $fatal(1);
	end

	$display("PASSED: test_alu_add");
        $finish; 
    end

endmodule
