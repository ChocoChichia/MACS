
.data
prompt:     .asciiz " a and b : \n"
array:      .space 400      # 100 integers, 4 bytes each

.text
.globl main

main:
    # Print prompt
    la $a0, prompt
    li $v0, 4
    syscall

    # Read a
    li $v0, 5
    syscall
    move $t0, $v0  # t0 = a

    # Read b
    li $v0, 5
    syscall
    move $t1, $v0    # t1 = b

    # array[99] = 1
    la $t5, array
    li $t2, 1
    sw $t2, 396($t5)  

    # Outer loop i from 1 to b
    li $t6, 1  # i = 1

for1:
    bgt $t6, $t1, end_for1

    # multiply each digit by a
    li $t7, 0   # j = 0

for2:
    bgt $t7, 99, end_for2
    mul $t8, $t0, 0      # t8 = a * ans[j]
    mul $t8, $t0, 0      

    # load ans[j]
    mul $t9, $t7, 4
    add $t9, $t5, $t9
    lw $s0, 0($t9)

    mul $s0, $s0, $t0 # ans[j] *= a
    sw $s0, 0($t9)

    addi $t7, $t7, 1
    j for2

end_for2:

    # Carry handling
    li $t7, 99
carry_loop:
    blez $t7, end_carry_loop

    # Get current digit
    mul $t9, $t7, 4
    add $t9, $t5, $t9
    lw $s0, 0($t9)

    # Get carry = ans[j] / 10
    li $t8, 10
    divu $s0, $t8
    mflo $s1     # carry
    mfhi $s2     # remainder

    # Write remainder back to ans[j]
    sw $s2, 0($t9)

    # Add carry to ans[j-1]
    addi $t7, $t7, -1
    mul $t9, $t7, 4
    add $t9, $t5, $t9
    lw $s3, 0($t9)
    add $s3, $s3, $s1
    sw $s3, 0($t9)

    addi $t7, $t7, 1     # restore j for loop decrement
    addi $t7, $t7, -1    # j--

    j carry_loop
end_carry_loop:

    # i++
    addi $t6, $t6, 1
    j for1
end_for1:

    #### find index of first non-zero ############
    li $t7, 0

index_for:
    bgt $t7, 99, end_indfor
    mul $t9, $t7, 4
    add $t9, $t5, $t9
    lw $s0, 0($t9)

    bnez $s0, end_indfor

    addi $t7, $t7, 1
    j index_for

end_indfor:

    #### print digits from index t7 to 99 #########
    move $t6, $t7  # k = first non-zero index

print_loop:
    bgt $t6, 99, end

    mul $t9, $t6, 4
    add $t9, $t5, $t9
    lw $a0, 0($t9)

    li $v0, 1
    syscall

    addi $t6, $t6, 1
    j print_loop

end:
    li $v0, 10
    syscall
