%ifndef COLON_INC
%define COLON_INC

%ifndef COLON_prev_entry
%define COLON_prev_entry dict_start
%endif

%macro colon 2

%2:
dq COLON_prev_entry
db %1, 0   ; dict entry key

%xdefine COLON_prev_entry %2

%endmacro

%endif
