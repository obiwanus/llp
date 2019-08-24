section .data
newline_char: db 10
codes: db '0123456789ABCDEF'

section .bss
output: resb 16

section .text
global _start

print_newline:
    mov rax, 1
    mov rdi, 1
    mov rsi, newline_char
    mov rdx, 1
    syscall
    ret

print_hex:
    mov rax, rdi
    mov rcx, 64
    xor rdx, rdx
.loop:
    push rax
    sub rcx, 4
    shr rax, cl
    and rax, 0xF

    mov sil, [codes + rax]
    mov [output + rdx], sil
    inc rdx

    pop rax
    test rcx, rcx
    jnz .loop

    mov rax, 1
    mov rdi, 1
    mov rsi, output
    ; rdx already contains the number of chars to output
    syscall

    ret

_start:
    mov rdi, 0xdeadbeef
    call print_hex
    call print_newline

    mov rax, 60
    xor rdi, rdi
    syscall
