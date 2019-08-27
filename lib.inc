section .data
ascii_digits: db '0123456789ABCDEF'

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
    mov rax, 1
    push rdi
    mov rsi, rsp    ; save pointer to char
    mov rdi, 1
    mov rdx, 1
    syscall
    pop rdi
    ret


print_newline:
    mov rdi, 10
    call print_char
    ret


print_uint:
    ; print the value of rdi as decimal unsigned int
    push rbp
    mov rbp, rsp

    mov rcx, rsp
    sub rsp, 24  ; allocate a buffer for output string
    dec rcx
    mov byte [rcx], 0   ; null-terminate preventively

    mov rax, rdi
    xor rdx, rdx
    mov rdi, 10
.loop:
    div rdi     ; rdx:rax / 10 -> rax, rdx
    mov dl, [ascii_digits + rdx]
    dec rcx
    mov [rcx], dl
    xor rdx, rdx
    test rax, rax
    jnz .loop

    mov rdi, rcx
    call print_string

    leave
    ret


print_int:
    cmp rdi, 0
    jge .nonnegative
    ; We don't handle the case of max negative int to simplify the code
    push rdi
    mov rdi, '-'
    call print_char
    pop rdi
    neg rdi
.nonnegative:
    call print_uint
    ret


string_equals:
    xor rax, rax
    ret


read_char:
    ; Reads one char from stdin and returns it
    mov rax, 0      ; read
    mov rdi, 0      ; stdin
    sub rsp, 1      ; buffer to read into
    lea rsi, [rsp]
    mov rdx, 1      ; number of bytes to read
    syscall
    cmp rax, 1      ; should've read 1 byte
    jne .error
    mov rax, [rsp]  ; return the char
    jmp .end
.error:
    xor rax, rax
.end:
    add rsp, 1
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
