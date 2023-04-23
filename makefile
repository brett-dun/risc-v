riscv :
	iverilog riscv_top.v -I ./ -o riscv

clean :
	rm -f riscv
