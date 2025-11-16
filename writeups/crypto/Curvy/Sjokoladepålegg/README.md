# Writeup: Curvy  
**Author:** Seppuku_FF1+4 (SamiFF1+4)  
**Team:** Sjokoladepålegg  
**Category:** Crypto  

## Challenge Text

>Still haven't gotten a good grip on elliptic curves? Here's a chance to learn!
>Combine the solutions from each challenge, in order, to create the flag.

## What This Challenge Tests
- Understanding EC point addition/subtraction
- Using SageMath to reverse EC transformations
- Knowing when Pohlig–Hellman applies (smooth curve order)
- Recognizing anomalous curves and the built-in (Nigel's) SMART attack in Sage

## About The Environment
I ran everything in SageMath on WSL (Ubuntu 22.04) because the online SageMathCell kept melting. 
Thanks to readme.txt for the recommendation!
[SageMath installation guide here](https://doc.sagemath.org/html/en/installation/index.html)

# Introduction
When I opened the Curvy folder, I instantly knew this was going to be one of "those" challenges. The ones where you pretend you remember ECC.

We get three subfolders, each containing a `.sage` script:

```
crypto-ell-1/
crypto-ell-2/
crypto-ell-3/
```
Each produces one part of the final flag, which must be concatenated as:

```
<part1><part2><part3>
```
# Part 1. Ell-1 Flag

The first script (`ell-1.sage`) defines a NIST curve, takes the hidden 6-byte flag, turns it into an x-coordinate of a point `P`, generates a random point `Q`, and outputs:

The script then prints:

`Q=`  
`R=`  

Here's an example of how the sage files output:

![Sage Ell-1 Test](img_1.png)

So the challenge gives us the final output, and we need to reverse it.

Here’s the most important part:

```python
# Encode the flag as the X coordinate of a point
P = E.lift_x(Integer(flag.hex(), 16))

# Random point
Q = E.random_point()

# Mix them together
R = P + Q

print(f"{Q=}")
print(f"{R=}")
```

If the script does:

`R = P + Q`

We simply do:

`P = R - Q`

A reversal script will solve the issue:

```python
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = p - 3
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
q = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

E = EllipticCurve(GF(p), [a, b])
E.set_order(q)

Q = E(43913347275644785153464449863125855125379958083706430882296801761478476592419,
      87918631137632055279958341837479029765235140217346982045811500319683853700187)

R = E(104815116867883818417432576260090330353182680342988101131628182143341649757099,
      47754550443389744842102740890992438457952225542439338525446667288370728104693)

P = R - Q
x = int(P[0])
flag = x.to_bytes((x.bit_length() + 7)//8, "big").decode()
print(flag)
```

Running it gives us the first part of the flag:

![Sage Ell-1 Flag](img_2.png)

# Part 2. Ell-2 Flag

Things get more interesting, and took me quite a while. The order factorization is a hint toward Pohlig–Hellman. SageMath’s builtin log() already uses it, but understanding why is part of the challenge. ell-2.sage defines a curve whose order looks like this:

```
2^2 * 3 * 18479537^2 * 785027357 * 2045936509 *
2067106871 * 2477515409 * 2952556279^2 * 3393346153^2
```

Smooth order = small prime factors = a nightmare. See references on the bottom.

This script does:

`P = G * k`

Where:

`k = int(flag_bytes.hex(), 16)`

Our job is basically; Given G and P, find k.

Here is where Pohlig-Hellman algorithm can help us. 

The solver ends up like this:

```python
Fp = GF(3383548089654669391553203464102735171188512652843421334636584693433923760273487421671271923)
E  = EllipticCurve(Fp, [1, 0])

order = (2^2 * 3 * 18479537^2 * 785027357 * 2045936509 *
         2067106871 * 2477515409 * 2952556279^2 * 3393346153^2)
E.set_order(order)

G = E.gens()[0]
P = E(1281118003088691942395276660159286361906554886534524987631212446305199953978223477605046101,
      2234211546389151676823620323130996132849234235234456998130554403469861833832111773630470326)

k = P.log(G)        # Pohlig–Hellman under the hood

flag = bytes.fromhex(k.hex()).decode()
print(flag)
```

Running it in Sage:

![Sage Ell-2 Flag](img_3.png)

# Part 3. Ell-3 Flag

For this one, the third script hints:

“since you’re so SMART…”

A subtle reference to Nigel Smart’s attack on anomalous elliptic curves!

This script again does:

`P = G * k`

But the curve parameters are chosen such that P.log(G) becomes much easier than it should be.

Fortunately for us, SageMath already knows how to handle this.
Calling .log() triggers the correct algorithm internally.

The solver:

```python
p = 0xcd2f8f8881c7953d8439dde00b7d82002c2257aa400a3965d4a4e7f62c85dca1
a = 0x27f99f93bcf80afc8a7cb4a9659c3cb4857b081cceea0e7ae883c7ac27167ffa
b = 0x94b0a239ba09589d7d433c378af909311145623c138d001574a25dd43e0e7ee2

E = EllipticCurve(GF(p), [a, b])

G = E(0x5d9312f4e40090425dbc2879c4d3a4c8e300c1aefd4c74406b0d866380921929,
      0xaf06cb0cd32376072b1aee0cd04cb7f643fb13dcfb44ec3ccb13a7b0e1067db3)

P = E(46149471738217762494682535578618395972032151610828362576737479435252149474916,
      37982107063220654423079127989899636852928253416608021485195608149289400914538)

k = P.log(G)    # SMART attack magic inside Sage

flag = bytes.fromhex(k.hex()).decode()
print(flag)
```

There we go, the third part:

![Sage Ell-3 Flag](img_4.png)

Now for the full flag, I spliced the scripts together and voila:

![Sage Ell-123 Full Flag](img_5.png)

This was a brilliant challenge, and I was pleased to both learn and try out SageMath. 
I definitely got a tighter grip on elliptic curves after this headscratcher. 

References:

[SageMath installation guide here](https://doc.sagemath.org/html/en/installation/index.html)

[Smooth numbers](https://en.wikipedia.org/wiki/Smooth_number)

[Discrete Logarithm](https://en.wikipedia.org/wiki/Discrete_logarithm)

[Pohlig-Hellman algorithm](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)

[SageMath Elliptic Curves Documentation](https://doc.sagemath.org/html/en/reference/arithmetic_curves/index.html)

[Nigel Smart](https://scholarship.claremont.edu/cgi/viewcontent.cgi?article=1633&context=scripps_theses)
