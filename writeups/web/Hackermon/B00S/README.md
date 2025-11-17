# Hackermon Writeup - Team B00S

`Author: Bludsoe`

# Initial thoughts

When playing the game, none of our attacks deal enough damage to kill the enemy before the enemy is able to kill us. This means that we somehow have to be able to do more damage with our attacks, or change the health of our enemy. 

## The Exploit

When choosing an attack the browser sends a POST packet, containing a JWT. If we decode this JWT in BurpSuite we can see some interesting information:

`JWT`:
```JSON
"eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJocFBsYXllciI6MTAwLCJocEVuZW15IjoxMDAsInJvdW5kIjowLCJwbGF5ZXJEYW1hZ2UiOjAsImVuZW15RGFtYWdlIjowLCJzdGFydGVkIjoxNzYzMzI4OTc0MTY5LCJpYXQiOjE3NjMzMjg5NzQsImV4cCI6MTc2MzMzMjU3NH0."
```

A JWT is created by three things, the header, the payload and finally a signature, each being separated by 2 periods. By looking at this JWT, we see that there is no signature at all which we know because there is no content after the second period. We can also see this based on the information in the header of the JWT.

`JWT Header (decode Base64)`:
```JSON
{"alg":"none", "typ":"JWT"}
```
Since the "alg" is set to none, we know that there is no algorithm creating the signature, and so no signature is created at all. This means that we can change the payload of JWT without having to make a new signature and then resend the packet for the round.

`JWT Payload (decode Base64)`:
```JSON
{
 "hpPlayer":100,
 "hpEnemy":100,
 "round":0,
 "playerDamage":0,
 "enemyDamage":0,
 "started":1763328974169,
 "iat":1763328974,
 "exp":1763332574
}
```

In the payload of the JWT, we can see some information about the current game we are playing after we have sent a packet for our attack. For instance we see our HP, the enemy's HP and some more information. We know that to win the game, we have to take out the enemy Pokemon. To do this, we can simply resend the POST packet, where we change the `hpEnemy` field to 0, indicating that the enemy is dead.

We send the packet to the repeater, change the `hpEnemy` field to 0 and then resend the packet:

<img src="./images/resend.gif">

The flag from this task is: `EPT{s1gn1ng_j4wt5_1s_fun}`