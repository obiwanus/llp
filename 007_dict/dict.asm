section .text

global find_word
; rdi - a pointer to a null-terminated key
; rsi - a pointer to the start of the "dict" linked list
; returns 0 if key not found, or the value address otherwise
find_word:
    ret
