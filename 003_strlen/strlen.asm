section .data
teststring: db "xXx", 0

section .text
global _start

strlen:
    mov rsi, -1
.loop:
    inc rsi
    mov al, [rdi + rsi]
    test al, al
    jnz .loop

    mov rax, rsi
    ret

_start:
    mov rdi, teststring
    call strlen

    mov rdi, rax  ; save result into exit code
    mov rax, 60
    syscall
