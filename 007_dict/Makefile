main.o: main.asm ../lib.inc
	nasm -felf64 -g main.asm

dict.o: dict.asm
	nasm -felf64 -g dict.asm

dict.out:  main.o dict.o
	ld -o dict.out main.o dict.o

clean:
	rm -rf *.out
	rm -rf *.o
