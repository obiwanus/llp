%include "colon.inc"

%ifndef WORDS_INC
%define WORDS_INC
section .data

colon "vodka", w1
db "something that people drink", 0

colon "vodka vodka", w2
db "something I heard from RWJ", 0

colon "boris yeltsin", w3
db "former Russian president who liked vodka, apparently", 0

%endif
