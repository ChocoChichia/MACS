# given a year number, find the minimum year number which is strictly larger than the given one and has only distinct digits.

# Input: The single line contains integer y (1000???y???9000) — the year number.

# Print a single integer — the minimum year number that is strictly larger than y and all it's digits are distinct. It is guaranteed that the answer exists.


################### Data segment ###################

.data

prompt:
.asciiz "Please enter year from 1000 to 9000: \n" 

sum_msg:
.asciiz ": next pretty year :  "

################### Code segment ###################

.text

.globl main

main:

# display first message
la $a0,prompt
li $v0,4
syscall


li $v0,5
# read 1st integer into $t0

syscall

# input year into t0
move $t0,$v0
addi $t0,$t0,1
li $t1, 0  # index of digits in each year

################### start finding the year  ###################


loop_1:
bgt $t0, 9000, end_loop_1

# Check for distinct digits
jal check_distinct_digits
beq $v0, 1, found_year # If digits are distinct returned answer written into v0 will be 1 : 0 

addi $t0, $t0, 1 # next yearrrrrrr  
j loop_1

################### output the answer :  ###################

found_year:

# display second message
la $a0,sum_msg
li $v0,4
syscall

# current year is the answer : ) 
move $a0, $t0
li $v0, 1
syscall  # print the year

end_loop_1:
li $v0, 10 # exit
syscall

################### check_distinct_digits  ###################


check_distinct_digits:
    move $t1, $t0  # Copy year to $t1 
    li $t2, 0      # Reset digit bitmask
    li $t3, 0      # Digit count, there are maaxxx 4 digits in one year

check_loop:
    beq $t3, 4, distinct_digits # check if all 4 digits are : ) 

    div $t1, $t1, 10 # t1 = t1 / 10 (quotient remains in t1)
    mfhi $t4         # t4 = remainder from division above 
    mflo $t1 	     # t1 = t1/10 answer from division aboveee

    # Check if the digit was already seen
    li $t5, 1
    sllv $t5, $t5, $t4 # shift 1 to the digit position, 
    # example of the code above :
    # if we had year 1987 , t4 would have been remainder "7"
    # then we shift number "1" seven times and we get : 001000000
    # so positions of "7" in 8 bit system is marked now
    # we mark every digit with "1"  
    
    # continuing first example, in t6 we write 000000000 and 001000000 
    and $t6, $t2, $t5 # check if the digit bit is set in bitmask
	
    # if this end resutled in random number, nor zero, it means we had 1-s in the same place
    # in t2 ( previous marked number) and in t5 ( marked digit now)
    bne $t6, 0, not_distinct # if it is, not distinct

    # in first example we get : t2 = 000000000 or 00100000 
    # gradually in t2 we mark every digits position
    or $t2, $t2, $t5 # set digit bit in bitmask

    addi $t3, $t3, 1 # increment digit count
    j check_loop

distinct_digits:
    li $v0, 1  # Digits are distinct
    j return_check

not_distinct:
    li $v0, 0  # Digits are not distinct

return_check:
    jr $ra  # Return











