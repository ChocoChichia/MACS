.data
prompt:
    .asciiz "Please enter n and m: \n"
sum_msg:
    .asciiz "Minimum steps: "
queue:
    .space 40000  # queue with 1000 int space

.text
.globl main

main:
    
    li $v0, 4
    la $a0, prompt
    syscall
    
    # n into t0
    li $v0, 5 # Read integer
    syscall # $v0 = value read
    addiu $t0, $v0, 0
    
    #m into t1
    li $v0, 5 # Read integer
    syscall # $v0 = value read
    addiu $t1, $v0, 0

    # queues vqmni aq 
    li $t2, 0   # front = 0 , frot itterator basically
    li $t3, 0   # rear = 0 , itterator at the end 
    li $t4, 0   # steps = 0 , answer 

    # queue[rear] = n and rear++ 
    la $t5, queue
    sw $t0, 0($t5)   # queue[rear] = n
    addiu $t3, $t3, 4 # rear++

bfs_loop:
    # if front < rear vcheqavt, if front == rear means we didn't add any element
    bge $t2, $t3, end_program

    #  queue size = rear - front 
    # previous elements we don't care about
    # so in t6 we write number of elements we have to parse
    sub $t6, $t3, $t2

    #  i = 0 for inner loop to parse trhough current queue elements
    li $t7, 0

for_loop:
    # if i >= size break
    bge $t7, $t6, increment_steps

    #  curr = queue[front]
    la $t5, queue
    # in t8 i write address to queue[front} which is queue + front 
    add $t8, $t5, $t2  
    # in t9 i write queue[front]
    lw $t9, 0($t8)     

    # front++ , so now front points to next offset in queue
    addiu $t2, $t2, 4

    # if curr == m thenn we found our answerrr
    beq $t9, $t1, print_result

    # we add  curr * 2 in the queue
    mul $t8, $t9, 2
    la $t5, queue
    # in t5 we write address to queue[rear]
    add $t5, $t5, $t3
    # we store curr*2
    sw $t8, 0($t5)
    # rear++ so now rear points to next offfset too
    addiu $t3, $t3, 4

    # if curr >= 1 then we add curr - 1 to queue, same logic as above
    blez $t9, skip_subtract
    sub $t8, $t9, 1
    la $t5, queue
    add $t5, $t5, $t3
    sw $t8, 0($t5)
    addiu $t3, $t3, 4

skip_subtract:
    # i++
    addiu $t7, $t7, 4
    j for_loop

increment_steps:
    # steps++
    addiu $t4, $t4, 1
    j bfs_loop

print_result:
    li $v0, 4
    la $a0, sum_msg
    syscall
	
    li $v0, 1
    #steps are in t4
    move $a0, $t4
    syscall

end_program:
    li $v0, 10
    syscall
