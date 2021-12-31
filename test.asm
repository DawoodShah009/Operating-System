org 0x7c00
bits 16


boot:
    mov ah, 0x02
    mov al, 0x01    ; how many sectors i want to read
    mov ch, 0x00
    mov cl, 0x02    ; sector number
    mov dh, 0x00
    mov dl, 0x80    ;  Disk number
    mov bx, 0x1000
    mov es, bx
    int 0x13
    jc error
    mov ah, 0x0e
    mov al, "H"
    mov bh, 0x0
    int 0x10
    jmp 0x1000:0x00   ;simple hardcoded address for both segment and offset.
error:
    mov ah, 0x0e
    mov al, "!"
    mov bh, 0x0
    int 0x10
    hlt
times (510-($-$$)) db 0x0
dw 0xaa55