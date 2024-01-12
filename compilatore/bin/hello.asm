
section .bss



section .data
    result db 1         ; variabile che rappresenta lo stato di uscita dalla funzione main




section .text
    Global _start

    _start:
        call main
        mov [result], rax


    _exit:
        mov rax, 60
        mov rdi, [result]
        syscall


    main:   push rbp
            mov rbp, rsp


            mov rax, 0
            pop rbp
            ret
