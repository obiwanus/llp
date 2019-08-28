%define O_RDONLY 0
%define PROT_READ 0x1
%define MAP_PRIVATE 0x2

%include "../lib.inc"

section .data
filename: db "input.txt", 0
msg_file_contents: db "File contents: ", 0
msg_factorial: db "Factorial: ", 0

section .text
global _start

_start:

    ; open
    mov rax, 2
    mov rdi, filename
    mov rsi, O_RDONLY
    mov rdx, 0
    syscall

    ; mmap
    mov r8, rax     ; descriptor
    mov rax, 9
    mov rdi, 0
    mov rsi, 4096
    mov rdx, PROT_READ
    mov r10, MAP_PRIVATE
    mov r9, 0       ; offset within the file
    syscall

    mov r12, rax    ; save pointer to the mapped region

    mov rdi, msg_file_contents
    call print_string

    mov rax, r12
    mov rdi, rax
    call print_string
    call print_newline

    mov rdi, r12
    call parse_uint
    mov r12, rax    ; save parsed number

    mov rdi, msg_factorial
    call print_string

    mov rdi, r12
    call factorial

    mov rdi, rax
    call print_int
    call print_newline

    call exit


factorial:
    mov rax, 1
    mov rcx, 1
.loop:
    mul rcx
    inc rcx
    cmp rcx, rdi
    jle .loop
    ret
