%define O_RDONLY 0
%define PROT_READ 0x1
%define MAP_PRIVATE 0x2

%include "../lib.inc"

section .data
filename: db "input.txt", 0
msg_file_contents: db "File contents: ", 0

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

    push rax

    mov rdi, msg_file_contents
    call print_string

    pop rax
    mov rdi, rax
    call print_string

    call exit
