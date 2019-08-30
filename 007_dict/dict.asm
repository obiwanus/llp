section .text

global find_word
extern string_equals

; rdi - a pointer to a null-terminated key
; rsi - a pointer to the start of the "dict" linked list
; returns 0 if key not found, or the value address otherwise
find_word:
    test rsi, rsi
    jz .key_not_found

    push rdi
    push rsi
    lea rsi, [rsi + 8]
    call string_equals
    pop rsi
    pop rdi

    test rax, rax
    jz .mismatch

    ; key found
    lea rax, [rsi + 8 + rax + 1]  ; value
    ret

.mismatch:
    lea rsi, [rsi]
    jmp find_word   ; optimized call

.key_not_found:
    xor rax, rax
    ret
