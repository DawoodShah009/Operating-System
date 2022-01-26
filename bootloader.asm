mov ah, 0x0e
mov al, 65
int 0x10

mov cl, al
mov al, " "
int 0x10



loop:
    mov al, cl
    inc al
    mov cl, al
    cmp al, 'Z' + 1
    je exit
    int 0x10
    mov al, " "
    int 0x10
    mov al, cl
    jmp loop 

exit:
jmp $
    
times 510-($-$$) db 0
db 0x55, 0xaa