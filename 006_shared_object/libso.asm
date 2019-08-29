extern _GLOBAL_OFFSET_TABLE_

global func:function

section .rodata
message: db "A message from a shared object", 10, 0

section .text
func:
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, 31
    syscall
    ret
