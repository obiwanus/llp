global _start

section .data
message: db 'hello, world!', 10

section .text

_start:
    mov     rax, 1  ; `write` system call number
    mov     rdi, 1  ; file descriptor
    mov     rsi, message
    mov     rdx, 14 ; size of the message
    syscall         ; write(1, message, 14)

    mov     rax, 60 ; `exit syscall number
    xor     rdi, rdi
    syscall
