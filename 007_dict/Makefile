lib.o: lib.asm
	nasm -felf64 lib.asm

main.o: main.asm
	nasm -felf64 main.asm

dict.o: dict.asm
	nasm -felf64 dict.asm

dict.out: lib.o main.o dict.o
	ld -o dict.out lib.o main.o dict.o

clean:
	rm -rf *.out
	rm -rf *.o
