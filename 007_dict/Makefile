main.o: main.asm
	nasm -felf64 main.asm

dict.o: dict.asm
	nasm -felf64 dict.asm

dict.out:  main.o dict.o
	ld -o dict.out main.o dict.o

clean:
	rm -rf *.out
	rm -rf *.o
