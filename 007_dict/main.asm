%include "words.inc"

section .data
err_input_too_large: db "Input string is too large", 10, 0
err_input_empty: db "Input was empty", 10, 0
err_key_not_found: db "Key not found in the dictionary", 10, 0

section .bss
input_buffer: resb 256

section .text

global _start
; Reads a string from input (at most 255 chars)
; Tries to find a value in the dict by that string as a key
; Prints the value if found, otherwise prints an error message
_start:

    ; read from stdin into buffer
    mov rdi, input_buffer
    mov rsi, 255
    call read_string

    test rax, rax
    jz .err_input_too_large
    test rdx, rdx
    jz .err_input_empty

    ; TODO: finish
    jmp .err_key_not_found

.err_input_too_large:
    mov rdi, err_input_too_large
    call print_string
    call exit

.err_input_empty:
    mov rdi, err_input_empty
    call print_string
    call exit

.err_key_not_found:
    mov rdi, err_key_not_found
    call print_string
    call exit
