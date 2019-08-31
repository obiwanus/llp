section .data
ascii_digits: db '0123456789'

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


; rdi - pointer to string
print_string_ascii_values:
.loop:
    xor rax, rax
    mov al, [rdi]   ; read one byte
    test al, al
    jz .end
    inc rdi
    push rdi
    mov rdi, rax
    call print_uint
    mov rdi, ' '
    call print_char
    pop rdi
    jmp .loop
.end:
    ret


print_newline:
    mov rdi, 10
print_char:
    mov rax, 1
    push rdi
    mov rsi, rsp    ; save pointer to char
    mov rdi, 1
    mov rdx, 1
    syscall
    pop rdi
    ret


print_int:
    cmp rdi, 0
    jge print_uint
    ; We don't handle the case of max negative int to simplify the code
    push rdi
    mov rdi, '-'
    call print_char
    pop rdi
    neg rdi
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
    xor rax, rax
    mov al, [rsp]  ; return the char
    jmp .end
.error:
    xor rax, rax
.end:
    add rsp, 1
    ret


; Attempts to read a word into buffer. If too big, returns 0, otherwise buffer address
; rdi - address of a buffer, rsi - buffer size
read_word:
    xor rcx, rcx
.loop:
    cmp rcx, rsi
    jge .out_of_space

    ; attempt to read a char
    push rsi
    push rcx
    push rdi
    call read_char
    pop rdi
    pop rcx
    pop rsi

    ; check for whitespace
    cmp rax, 0x20
    je .whitespace
    cmp rax, 0x9
    je .whitespace
    cmp rax, 0x10
    je .whitespace
    cmp rax, 0      ; maybe nothing was read
    je .whitespace

    ; write into buffer
    mov [rdi + rcx], al
    inc rcx
    jmp .loop
.whitespace:
    mov byte [rdi + rcx], 0     ; null-terminate
    mov rax, rdi
    mov rdx, rcx
    ret
.out_of_space:
    xor rax, rax
    xor rdx, rdx
    ret


; Tries to read a null-terminated string from stdin into buffer
; rdi - buffer address
; rsi - buffer size
; returns rax - if input too big then 0, otherwise buffer address
; returns rdx - number of bytes read
read_string:
    xor rcx, rcx
.loop:
    cmp rcx, rsi
    jge .out_of_space

    ; attempt to read a char
    push rsi
    push rcx
    push rdi
    call read_char
    pop rdi
    pop rcx
    pop rsi

    ; write into buffer
    mov [rdi + rcx], al

    ; check for null-terminator or if nothing was read
    test rax, rax
    jz .null

    inc rcx
    jmp .loop
.null:
    mov rax, rdi
    mov rdx, rcx
    ret
.out_of_space:
    xor rax, rax
    xor rdx, rdx
    ret


; rdi points to a string
; returns rax: number, rdx : length
parse_uint:
    push rbx
    xor rax, rax    ; result
    xor rbx, rbx    ; length
    mov rsi, 10     ; to multiply with

.loop:
    ; try to parse a digit
    xor rcx, rcx
    mov cl, [rdi + rbx]
    cmp cl, '0'
    jb .no_digit
    cmp cl, '9'
    ja .no_digit

    sub cl, '0' ; now cl contains the digit we want
    mul rsi     ; rdx:rax = rax * 10
    add rax, rcx

    test rdx, rdx   ; check if we spilled to rdx
    jnz .overflow

    inc rbx
    jmp .loop

.no_digit:
    ; rax should now contain the number we want
    mov rdx, rbx
    pop rbx
    ret
.overflow:
    xor rax, rax
    xor rdx, rdx
    ret

; rdi points to a string
; returns rax: number, rdx : length
parse_int:
    xor rcx, rcx    ; 0 if positive, -1 if negative
    mov al, [rdi]   ; check for a minus sign
    cmp al, '-'
    jne .parse
    mov rcx, -1
    inc rdi
.parse:
    push rcx
    call parse_uint
    pop rcx
    test rdx, rdx
    jz .end         ; failed to parse
    cmp rcx, -1
    jne .end
    neg rax         ; overflow is not handled
    inc rdx         ; sign adds 1 to the length
.end:
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


; rdi - pointer to string1
; rsi - pointer to string2
; returns string len if strings are equal, 0 otherwise
global string_equals
string_equals:
    xor rax, rax
    xor rcx, rcx
.loop:
    mov al, [rdi + rcx]
    cmp al, [rsi + rcx]
    jne .not_equal
    test al, al
    jz .equal
    inc rcx
    jmp .loop
.equal:
    mov rax, rcx
    ret
.not_equal:
    xor rax, rax
    ret
