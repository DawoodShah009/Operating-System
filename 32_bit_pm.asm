[org 0x7c00]
mov [BOOT_DISK], dl

CODE_SEG equ code_descriptor - GDT_Start
DATA_SEG equ data_descriptor - GDT_Start  ;equ is used to set constants

cli 
lgdt [GDT_Descriptor]
; change last bit of cr0 to 1
mov eax, cr0
or eax, 0x1
mov cr0, eax ; 32 bit mode....

; far jump (jump to other segment)
jmp CODE_SEG: start_protected_mode

;jmp $

GDT_Start:
    null_descriptor:
        dd 0x0 ; 4 times 00000000
        dd 0x0 ; 4 times 00000000    fffff hex = 4bits = 4 x5 = 20bits
    code_descriptor:
        dw 0xffff
        dw 0x0 ; 16 bits + 
        db 0x0 ; 8 bits = 24
        db 10011010b ; p,p,t, type flags
        db 11001111b ; other flags  + limit(last four bits)
        db 0x0 ; base last 8 bits 
    data_descriptor:
        dw 0xffff
        dw 0x0 ; 16 bits + 
        db 0x0 ; 8 bits = 24
        db 10010010b ; p,p,t, type flags
        db 11001111b ; other flags  + limit(last four bits)
        db 0x0 ; base last 8 bits 
GDT_End:

GDT_Descriptor:
    dw GDT_End - GDT_Start - 1  ; size   16 bits
    dd GDT_Start                ; start   32bits(address)


[bits 32]
start_protected_mode:

    mov al, 'A'
    mov ah, 0x0f ; white on black

    mov [0xb8000], ax  ; move to video memory location
    hlt
    jmp $

BOOT_DISK: db 0x0

times 510-($-$$) db 0x0
dw 0xaa55


