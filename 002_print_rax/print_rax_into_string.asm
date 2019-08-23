section .data
codes: db '0123456789ABCDEF'

section .bss
output: resb 18     ; to hold the output string plus newline

section .text
global _start
_start:

    mov rax, 0x1122334455667788

    mov rcx, 64
    xor rdx, rdx
.loop:
    push rax
    sub rcx, 4
    shr rax, cl
    and rax, 0xf

    mov sil, [codes + rax]
    mov [output + rdx], sil
    inc rdx

    pop rax
    test rcx, rcx
    jnz .loop

    mov byte [output + rdx], 10  ; \n
    inc rdx

    ; write to stdout (rdx contains the number of symbols to output)
    mov rax, 1
    mov rdi, 1
    mov rsi, output
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
