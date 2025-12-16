
################### Data segment ###################
.data

input_prompt:
.asciiz "Enter expression  \n"

newline:
.asciiz "\n"

buffer:
.space 1000

################### Code segment ###################
.text
.globl main

main:
    # print input prompt
    la $a0, input_prompt
    li $v0, 4
    syscall

    # read string input into buffer
    la $a0, buffer
    li $a1, 1000
    li $v0, 8
    syscall

    # initialize variables
    li $t0, 0          # result
    li $t1, 0          # last
    li $t2, 0          # num
    li $t3, '+'        # op
    la $t4, buffer     # pointer to input
    li $t5, 0          # temp char

parse_loop:
    lb $t5, 0($t4)    
    beqz $t5, apply_final  

    # check if digit
    li $t6, '0'
    li $t7, '9'
    blt $t5, $t6, not_digit
    bgt $t5, $t7, not_digit

    # num = num * 10 + (c - '0')
    li $t8, 10
    mul $t2, $t2, $t8
    sub $t8, $t5, $t6
    add $t2, $t2, $t8
    j next_char

not_digit:

    li $t6, ','
    beq $t5, $t6, next_char

    li $t6, '+'
    beq $t3, $t6, op_add
    li $t6, '-'
    beq $t3, $t6, op_sub
    li $t6, '*'
    beq $t3, $t6, op_mul
    li $t6, '/'
    beq $t3, $t6, op_div

op_add:
    add $t0, $t0, $t1
    move $t1, $t2
    j op_done
op_sub:
    add $t0, $t0, $t1
    sub $t1, $zero, $t2
    j op_done
op_mul:
    mul $t1, $t1, $t2
    j op_done
op_div:
    div $t1, $t2
    mflo $t1
    j op_done

op_done:
    move $t3, $t5      
    li $t2, 0          

next_char:
    addi $t4, $t4, 1
    j parse_loop

apply_final:
    add $t0, $t0, $t1  

    # print result
    move $a0, $t0
    li $v0, 1
    syscall

    # newline
    la $a0, newline
    li $v0, 4
    syscall

    li $v0, 10
    syscall
