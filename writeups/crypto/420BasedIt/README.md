# 420BasedIt
Author: surprior

## Description
```
I was gonna write a crypto challenge, but then I got high...

Anyway, what's cooking **chef**? #420BasedIt!
```

## Provided challenge files
* [enc.txt](enc.txt)

You can solve the challenge by using several decryption algorithms using CyberChef.

First you can identify the algorithm used to encrypt the string by using this tool `https://www.dcode.fr/cipher-identifier` 

First it identifies the string as Base91 encoding. Use cyberchef and choose Base92 as it does not have Base91. Reiterate to find the cipher used for the new string. 

After some of these iterations, you find that by using : `From Base92 -> From Base85 -> From Base85 -> From Base64 -> From Base62 -> From Base32` it returns the flag.

Flag: `EPT{I5_th3_Ch3f_1n_yet?}`

Link to [CyberChef showing these steps.](https://gchq.github.io/CyberChef/#recipe=From_Base92()From_Base85('!-u',true,'z')From_Base85('!-u',true,'z')From_Base64('A-Za-z0-9%2B/%3D',true,false)From_Base62('0-9A-Za-z')From_Base32('A-Z2-7%3D',true)&input=NCdTXFd5WlBbL0g1bGIuNjNkUiMwPFxGP1NyWyosIVdBaVxIdHkzfWh2T3RsYi11PlYkRT08Nil5eW1nQFlafUs0MiMlNl1PS3ZJUlMqM3I4Ol43SV5Ze2c8Umc9IzZlRXlSIV1XY2cpMVJjVkdsdS5oJWtZNV1bXFpmXkAyRFBAPzpOWU0ydmJDRTE&oeol=NEL)



