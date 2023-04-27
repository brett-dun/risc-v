riscv :
	iverilog riscv_top.v -I ./ -o riscv

test :
	rm -f test
	iverilog test_alu_add.v -I ./ -o test
	./test
	iverilog test_alu_subtract.v -I ./ -o test
	./test
	rm -f test

clean :
	rm -f riscv
	rm -f test
