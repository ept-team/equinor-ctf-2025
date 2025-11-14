# PKCSTIMING: Bleichbacher PKCS#1 chosen-ciphertext timing attack

```
Team: coldboots (https://ctftime.org/team/144114/)
Author: @ciphr
Date: 12.11.2025
```


# Challenge

Description:
```
You've discovered a misconfigured oracle. During your investigation, you've intercepted a message—along with its corresponding public key.

By poking around, you've managed to connect to the oracle using the connection helper. However, you haven't yet figured out the correct message size required to communicate with it properly.

Hint: The key to solving this lies in the timing. Strongly recommend utalizing the pwnbox for the best performance.
```

Handouts: `public.pem`, `message.txt` (ciphertext) and a `connection_helper.py` (see at the bottom)

# TL;DR

This is a textbook `Bleichbacher attack` (`RSA with PKCS#1`) described here: https://archiv.infsec.ethz.ch/education/fs08/secsem/bleichenbacher98.pdf in particular pay attention to `4.3 A Timing Attack`.

- We will perform a `CCA: chosen-ciphertext-attack` and use remote as an Oracle.
- By carefully selecting a `threshold` we will determine if `PKCS valid or invalid`.
- It is based on the assumption that the oracle spends `a measurable different time` when PKCS decode is `valid compared to invalid`. If this assumption does not hold, our attack will not work.
- I found an online code that implemented this attack, and modified it to use timing rather than local PKCS#1 decode to act as the oracle:

> **NOTE** `Timing attacks are sensitive` in particular over networks and even moar in particular if you try it over **the Internjet**. As the challenge description states; `use the eptbox, or you are doomed`.

# PKCS#1
When **encoding** PKCS we pad data using the format `\x00 \x02 <random non-zero bytes> \x00 <data>`

When **decoding** PKCS we check that the string starts with `\x00 \x02` and that we have a `\x00` from position 10 and onwards. It strips all the random bytes until it hits that last `\x00` and returns **data**. 

- PKCS is `valid` if the above is true.
- PKCS is `invalid` if it doesn't find either the starting `\x00 \x02` or the `\x00` prefixing **data**. 

When remote received our tampered `ct' = ct*s mod n` it first performs the RSA decrypt `m' = ct'^d mod n` then it tries to PKCS decode `m'` as described above.

# Using remote as a Oracle: Finding a threshold
We need to find a **threshold** to differentiate responses into **PKCS valid** or **PKCS invalid**. I found my threshold after running two tests using `ct = <message.txt>` as I assume this is a valid encrypted message (as stated in the challange description).

It seems my assumption was correct, when i send:
- `ct`: i assume this is `valid PKCS` and get `roughly always >= 0.12s`
- `ct' = ct*s mod n` where i selected `s=3` i assume this is `invalid PKCS` and get `rougly < 0.005s`

(See log at bottom for these numbers)

> Why `s=3`? Paper describes the initial s as being atleast `>= n/(3*B)` to get valid PKCS, so any lower s would suffice to get an invalid PKCS.

I set my oracle threshold to `True if time >= 0.1 else False`.

As my code demonstrates, I only care about timing the request+response:
```python
THRESHOLD = 0.1 

def oracle(payload, verbose:bool=False):    
    global ssl_sock
    assert isinstance(payload, bytes) == True    
    start = time.time()
    ssl_sock.sendall(payload)    
    ssl_sock.recv(64)    
    diff = time.time() - start
    if verbose:
        print(f"[+] took={diff}s") 
    return True if diff > THRESHOLD else False
```

# A short explaination on the attack
We want to find a `s` so that `ct' = (m*s)^d mod n` decodes to valid PKCS which means `m = (ct'* s^-1) mod n` holds. The paper describes how we find such an `s`. It works like this (in short):

We keep sending `ct' = ct*s^e mod n` and Oracle responds true|false PKCS decode was OK.
- `valid decode`: Remote did `m' = ct'^d mod n = (ct*s)^d mod n = (m*s) mod n` and we then know that `(m*s)[0:2] == \x00\x02`.
- This is the base foundation for all the calls done in the algorithm.

> The overall trick is to keep finding an increasinly larger `s` while PKCS unpad is still valid.

Let's define `B = 2^(8*(k-2))` as a bounds and `k = bytes of n => k=128`. We subtract `-2` because we already know the prefix part of **m** = `\x00\x02`. 
- When `m*s` valid PKCS  we know that `2*B <= (m*s) (mod n) < 3*B`.

The initial s, **s0**, is minimum **n/(3*B)** which in our case is `12225`. We search for s0 by `+1` until we get valid PKCS. I found `s0=32783`, and it holds for every time we send the same ct. If we send a different ct, we will get a different s0, even if we encode the same m since PKCS#1 will add diffeernt random bytes to the padding. With our s0=32783 we know that `(m*s0)[0:2] == \x00\x02`, and `we have successfully leaked the first two bytes! yay!`

When we have a new `s` we can update our intervals `M` which defines the `upper and lower bounds for m` as a function of `s` and the previous intervals `M`. As `s` grows in size, the interval decrease. The goal is to get the interval down to zero, which means we have `upper-lower == 0` and we found `m`.

We iteratively try to find a better and new `si` which is within the bounds of the previous s, and we test these si's until we find one that yields valid PKCS alike the equations above: `ct' = (ct*si)^e mod`. When we find such an `si` we now have found the `new s` and we update the intervals `M`.

When we hit `upper-lower == 0` we have `found the flag`.

# flag
See `solve.py` at bottom.

`EPT{17_15_4LL_4B0U7_71M1NG}`

took ~2.5minutes to solve on eptbox.


# public.pem
```
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPQJc4NNEA0uvCTFZ5N/EJxyl1
bAbO3+nYYe8eXyG6rQtMhn1yBDprlc5bkttXxVdroh+UJOpWtnaFvsQ4pu/rXOh3
QgiYWt5qN+DV/A4ZW0KVj2zfONn/PFaXYFk7ZpeAWNV0yy6ajV9RulfmI1cVfRmi
sT4A8fmNhJzqfkNHdQIDAQAB
-----END PUBLIC KEY-----
```

# message.txt
```
770382871fa49bf54d4ff3985d248e9de94258f773a105556b3782e8b4669f0f5f93f3d64c8e0c3e17d9316df7851da568b997348f308fee3f3854c60c8b0179c0dd12c4af057b3c6aca5fec7a305c9d8822b51f2ffdf78233e04a5f57b802cd473a508e0e4e738d3578cf63af54b125d4643635df70de70017a4f157600bc8b
```

# connection_helper.py
```python
import socket
import ssl

HOST = "<host>"  
PORT = <port>  
k = 1  # Insert the correct modulus length

def send_test(test: bytes) -> bytes:
    # Create an SSL context
    context = ssl.create_default_context()

    # Establish a secure connection 
    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssl_sock:
            ssl_sock.sendall(test)

            # Receive the response (up to 64 bytes)
            response = ssl_sock.recv(64)

    return response

if __name__ == "__main__":
    # Example message:
    test = b"\x00" * k
    response = send_test(test)
    print("Oracle response:", response)
```


# solve.py
Cudos to the work of: https://github.com/alexandru-dinu/bleichenbacher/tree/master/src

I only modified and added timings for the Oracle. Rest of the code is written by someone else.

> **DISCLAIMER** I can't be sure if the code above is the original author, or if this also is a copy from someone else.


```python
import random 
import socket
import ssl
from Crypto.Util.number import * 

from collections import namedtuple
Interval = namedtuple("Interval", ["lower_bound", "upper_bound"])

import time
t_start = time.perf_counter()
global queries
queries = 0


########## My code ###########

n = 0x8F40973834D100D2EBC24C567937F109C729756C06CEDFE9D861EF1E5F21BAAD0B4C867D72043A6B95CE5B92DB57C5576BA21F9424EA56B67685BEC438A6EFEB5CE8774208985ADE6A37E0D5FC0E195B42958F6CDF38D9FF3C569760593B66978058D574CB2E9A8D5F51BA57E62357157D19A2B13E00F1F98D849CEA7E434775
assert n == 100595191255958449419356035287212557374710947929647772010402817022906215816543195662901193178696535924404931509225920109839401795911182152549426416551273126491882854062518254773452094431333481281327065682985918209933025132065240283938063039096533596849232166709146143349179519427108005680525647980548122167157
e = 65537
k = 1024 // 8 # k is length of n in bytes

THRESHOLD = 0.1 

LOCAL = False
HOST = "coldboots-f118eaf5-bleichenbacher.ept.gg"  
PORT = 1337
context = ssl.create_default_context()
sock = socket.create_connection((HOST, PORT))
ssl_sock = context.wrap_socket(sock, server_hostname=HOST)       

def oracle(payload, verbose:bool=False):    
    global ssl_sock
    assert isinstance(payload, bytes) == True    
    start = time.time()
    ssl_sock.sendall(payload)    
    ssl_sock.recv(64)    
    diff = time.time() - start
    if verbose:
        print(f"[+] took={diff}s") 
    return True if diff > THRESHOLD else False

########## My code ###########


# Step 2.A.
def find_smallest_s(lower_bound, c):
    """
    Find the smallest s >= lower_bound,
    such that (c * s^e) (mod n) decrypts to a PKCS conforming string
    """
    s = lower_bound

    while True:
        attempt = (c * pow(s, e, n)) % n
        attempt = long_to_bytes(attempt)        
        if oracle(attempt):
            return s
        s += 1


# Step 2.C.
def find_s_in_range(a, b, prev_s, B, c):
    """
    Given the interval [a, b], reduce the search
    only to relevant regions (determined by r)
    and stop when an s value that gives
    a PKCS1 conforming string is found.
    """
    ri = ceil(2 * (b * prev_s - 2 * B), n)

    while True:
        si_lower = ceil(2 * B + ri * n, b)
        si_upper = ceil(3 * B + ri * n, a)

        for si in range(si_lower, si_upper):
            attempt = (c * pow(si, e, n)) % n
            attempt = long_to_bytes(attempt)
            
            if oracle(attempt):
                return si
        ri += 1


def safe_interval_insert(M_new, interval):
    """
    Deal with interval overlaps when adding a new one to the list
    """

    for i, (a, b) in enumerate(M_new):

        # overlap found, construct the larger interval
        if (b >= interval.lower_bound) and (a <= interval.upper_bound):
            lb = min(a, interval.lower_bound)
            ub = max(b, interval.upper_bound)

            M_new[i] = Interval(lb, ub)
            return M_new

    # no overlaps found, just insert the new interval
    M_new.append(interval)

    return M_new


# Step 3.
def update_intervals(M, s, B):
    """
    After found the s value, compute the new list of intervals
    """

    M_new = []

    for a, b in M:
        r_lower = ceil(a * s - 3 * B + 1, n)
        r_upper = ceil(b * s - 2 * B, n)

        for r in range(r_lower, r_upper):
            lower_bound = max(a, ceil(2 * B + r * n, s))
            upper_bound = min(b, floor(3 * B - 1 + r * n, s))

            interval = Interval(lower_bound, upper_bound)

            M_new = safe_interval_insert(M_new, interval)

    M.clear()

    return M_new

def floor(a, b):
    return a // b


def ceil(a, b):
    return a // b + (a % b > 0)


def bleichenbacher(ciphertext):
    """
    Perform Bleichenbacher attack as described in his paper.
    """

    # Step 1 can be skipped if c is already PKCS conforming (i.e., when c is an encrypted message). In that case, we set s0 ← 1

    # integer value of ciphertext
    c = bytes_to_long(ciphertext)

    B = 2 ** (8 * (k - 2))

    M = [Interval(2 * B, 3 * B - 1)]

    # Step 2.A.
    
    # s = find_smallest_s(ceil(n, 3 * B), c)        
    s = 32783
    print(f"[+] found s0={s}")
    
    M = update_intervals(M, s, B)

    while True:
        # Step 2.B.
        if len(M) >= 2:
            s = find_smallest_s(s + 1, c)
            print("[!] new s=", s)

        # Step 2.C.
        elif len(M) == 1:
            a, b = M[0]
            diff = abs(a-b)
            bits = int(diff).bit_length()
            print(f"[🏴] interval bits left bits={bits} progress={100 - (bits/1024*100)}%%")
            # Step 4.
            if a == b:
                print("[🏴] Success! Flag=", a)
                return long_to_bytes(a % n)

            s = find_s_in_range(a, b, s, B, c)
            print("[!] new s=", s)

        M = update_intervals(M, s, B)




if __name__ == "__main__":
    secret = bytes.fromhex("770382871fa49bf54d4ff3985d248e9de94258f773a105556b3782e8b4669f0f5f93f3d64c8e0c3e17d9316df7851da568b997348f308fee3f3854c60c8b0179c0dd12c4af057b3c6aca5fec7a305c9d8822b51f2ffdf78233e04a5f57b802cd473a508e0e4e738d3578cf63af54b125d4643635df70de70017a4f157600bc8b")    

    # When I measured PKCS unpad = OK and not OK
    if True:
        print("[+] PKCS valid")
        for _ in range(10):
            oracle(secret, verbose=True)

        print("[+] PKCS in-valid")
        secret_ = long_to_bytes( (bytes_to_long(secret) * 3)%n)
        for _ in range(10):
            oracle(secret_, verbose=True)
        
        input("done gogo>")
            
    flag = bleichenbacher(secret)
    flag = flag[flag.index(b"\00")+1:] # PKCS1 decode
    print(flag.decode())
```

# Flag

Here we see that I have `~0.12` for valid padding and `<0.005` for invalid padding.

```
$ time python3 solve.py
[+] PKCS valid
[+] took=0.1734166145324707s                   
[+] took=0.12491631507873535s      
[+] took=0.12483334541320801s
[+] took=0.12487387657165527s
[+] took=0.1251358985900879s
[+] took=0.12495279312133789s
[+] took=0.12501764297485352s     
[+] took=0.12502646446228027s 
[+] took=0.12475252151489258s
[+] took=0.1251082420349121s
[+] PKCS in-valid
[+] took=0.004628896713256836s
[+] took=0.004582881927490234s
[+] took=0.004770040512084961s
[+] took=0.004670619964599609s
[+] took=0.004673957824707031s
[+] took=0.004614830017089844s
[+] took=0.004629373550415039s
[+] took=0.004938364028930664s
[+] took=0.004459381103515625s
[+] took=0.00459599494934082s
done gogo>   
[+] found s0=32783
[🏴] interval bits left bits=993 progress=3.02734375%%                                         
[!] new s= 376992             
[🏴] interval bits left bits=990 progress=3.3203125%%                                          
[!] new s= 770374             
[🏴] interval bits left bits=989 progress=3.41796875%%                                         
[!] new s= 1721047            
[🏴] interval bits left bits=988 progress=3.515625%%                                           
[!] new s= 3458484                            
[🏴] interval bits left bits=987 progress=3.61328125%%
[!] new s= 7015312     
[🏴] interval bits left bits=985 progress=3.80859375%%                                         
[!] new s= 14047014
[🏴] interval bits left bits=985 progress=3.80859375%%                                         
[!] new s= 28143200                            
[🏴] interval bits left bits=983 progress=4.00390625%%                                         
[!] new s= 56417526
[🏴] interval bits left bits=983 progress=4.00390625%%                                         
[!] new s= 112949787
[🏴] interval bits left bits=982 progress=4.1015625%%                                          
[!] new s= 225932355
...
[!] new s= 2309664895091638100581031063164154958803560477191114924515095113699375086399289927053157183987791220572385688985907229936293448198220223119607011371711975867641886175503507286648902701652643224150375056020780767315530668806686551356277163452766013315596240634064486717022536250320626050047535838572820151
[🏴] interval bits left bits=0 progress=100.0%%
[🏴] Success! Flag= 6137253440445042345129640036530083641050944170524107668085082031153067874765437884157647264968832794783110419287933129083774537702476262722149691357403226810036460488679872520177973169163686708254934227476637571079971066967172243872955014354863348836798185108617310588354994902618172270009125398773647229
EPT{17_15_4LL_4B0U7_71M1NG}


real    153.89s
user    2.08s
sys     0.49s
cpu     1%
"""

```