section .data
newline_char: db 10
codes: db '0123456789ABCDEF'

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
# TODO

_start:
    mov rdi, 0xdeadbeef
    call print_hex
    call print_newline

    mov rax, 60
    xor rdi, rdi
    syscall
