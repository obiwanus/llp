section .text

exit:
    ; Accepts rdi as the exit code
    mov rax, 60
    syscall


string_length:
    xor rax, rax
.loop:
    cmp byte [rdi + rax], 0
    je .end
    inc rax
    jmp .loop
.end:
    ret


print_string:
    call string_length
    mov rdx, rax    ; save string length

    mov rax, 1
    mov rsi, rdi
    mov rdi, 1
    syscall
    ret


print_char:
    xor rax, rax
    ret


print_newline:
    xor rax, rax
    ret


print_uint:
    xor rax, rax
    ret


print_int:
    xor rax, rax
    ret

string_equals:
    xor rax, rax
    ret


read_char:
    xor rax, rax
    ret

read_word:
    ret

; rdi points to a string
; returns rax: number, rdx : length
parse_uint:
    xor rax, rax
    ret

; rdi points to a string
; returns rax: number, rdx : length
parse_int:
    xor rax, rax
    ret


string_copy:
    ; accepts a pointer to a string (rdi), a pointer to a buffer (rsi), and the buffer's length (rdx).
    ; if the string doesn't fit into the buffer, then zero is returned, otherwise
    ; the destination address is returned
    call string_length
    inc rax     ; make sure we have the space for the zero at the end
    cmp rax, rdx
    jg .doesntfit

    push rsi    ; save buffer pointer
.loop:
    mov al, [rdi]
    test al, al
    jz .end
    mov [rsi], al
    inc rdi
    inc rsi
    jmp .loop

.end:
    mov byte [rsi], 0   ; null-terminate
    pop rax     ; pop the old buffer pointer into rax
    ret

.doesntfit:
    xor rax, rax
    ret
