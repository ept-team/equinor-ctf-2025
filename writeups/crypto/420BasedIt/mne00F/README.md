# Writeup: 420BasedIt
## Team: mne00F
**Author:** Mheara

## Challenge
Decode this string:
`4'S\WyZP[/H5lb.63dR#0<\F?Sr[*,!WAi\Hty3}hvOtlb-u>V$E=<6)yymg@YZ}K42#%6]OKvIRS*3r8:^7I^Y{g<Rg=#6eEyR!]Wcg)1RcVGlu.h%kY5][\Zf^@2DP@?:NYM2vbCE1`

## Process

Given the challenge name, 420BasedIt, it was likely a base encoding task and the numbers would likely add up to 420 - as there does not seem to be a base420 encoding (trust me, I tried). So either test various combinations, check a cipher identifier (like [dcode's](https://www.dcode.fr/cipher-identifier)). I tested various combinations, with some assumptions to cut down on available combinations: It would likely be sorted from high to low, it would likely have 6 base encodings, where one high base encoding would appear twice, and that it would have base92 and base64. This gave the starting point of `92 + 85 + 85 + 64 = 326`, which leaves `420 - 326 = 94` - so with 2 assumed bases left, only 62 and 32 would work here. Putting this into [CyberChef](https://gchq.github.io/CyberChef/), resulted in:

```
base92 -> base85 -> base85 -> base64 -> base62 -> base32

4'S\WyZP[/H5lb.63dR#0<\F?Sr[*,!WAi\Hty3}hvOtlb-u>V$E=<6)yymg@YZ}K42#%6]OKvIRS*3r8:^7I^Y{g<Rg=#6eEyR!]Wcg)1RcVGlu.h%kY5][\Zf^@2DP@?:NYM2vbCE1
...
EPT{I5_th3_Ch3f_1n_yet?}
```


