# 'Hackermon' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

## Source code analysis

I started by downloading the provided source code handout. Here one can quickly find the interesting file, `server/index.js`. I quickly spotted several issues with the JWT-based authentication:

1. The JWT secret `super_secret_key_2024_ctf_hackermon` is hardcoded
2. The verification is done using `jwt.decode`, which doesn't validate the signature (should've used `jwt.verify`)
3. The algorithm used to sign is set to `none`
   - It uses the `CRYPTO_METHOD` variable, which is set to be the base64 decoded text of `bm9uZQ==`
   - After decoding with [CyberChef](<https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=Ym05dVpRPT0>) this becomes `none`

## Attack

There are many ways to solve this challenge. Since the JWT signing already uses the `none` algorithm, I decided it was easiest to modify an existing token.

1. Start an instance and open it in Firefox
2. Open devtools and the network inspector
3. Execute an action to send a request
4. Open the request reponse, and copy out value of the `token` field
   - In my case `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJocFBsYXllciI6NDUsImhwRW5lbXkiOjc5LCJyb3VuZCI6MiwicGxheWVyRGFtYWdlIjoxMCwiZW5lbXlEYW1hZ2UiOjM0LCJzdGFydGVkIjoxNzYyNzkzMzk3Njg2LCJwbGF5ZXJBdHRhY2tOYW1lIjoiUkdCIGxpZ2h0cyIsImVuZW15QXR0YWNrTmFtZSI6IjEwIHNtdXJmcyAoR2V0IGl0PyBHZXQgaXQ_IFRoZXkgYXJlIGJsdWUuLi4gQmx1ZSB0ZWFtLi4uIG52bS4uLikiLCJpYXQiOjE3NjI3OTM0MTEsImV4cCI6MTc2Mjc5NzAxMX0.`
5. Copy the payload part (between the two dots) into [CyberChef](<https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',false,false)&input=ZXlKb2NGQnNZWGxsY2lJNk5EVXNJbWh3Ulc1bGJYa2lPamM1TENKeWIzVnVaQ0k2TWl3aWNHeGhlV1Z5UkdGdFlXZGxJam94TUN3aVpXNWxiWGxFWVcxaFoyVWlPak0wTENKemRHRnlkR1ZrSWpveE56WXlOemt6TXprM05qZzJMQ0p3YkdGNVpYSkJkSFJoWTJ0T1lXMWxJam9pVWtkQ0lHeHBaMmgwY3lJc0ltVnVaVzE1UVhSMFlXTnJUbUZ0WlNJNklqRXdJSE50ZFhKbWN5QW9SMlYwSUdsMFB5QkhaWFFnYVhRX0lGUm9aWGtnWVhKbElHSnNkV1V1TGk0Z1FteDFaU0IwWldGdExpNHVJRzUyYlM0dUxpa2lMQ0pwWVhRaU9qRTNOakkzT1RNME1URXNJbVY0Y0NJNk1UYzJNamM1TnpBeE1YMA&oeol=FF>), and use Base64 decode
6. In [CyberChef](<https://gchq.github.io/CyberChef/#recipe=To_Base64('A-Za-z0-9%2B/%3D')&input=eyJocFBsYXllciI6MTAwLCJocEVuZW15IjoxLCJyb3VuZCI6MiwicGxheWVyRGFtYWdlIjoxMCwiZW5lbXlEYW1hZ2UiOjM0LCJzdGFydGVkIjoxNzYyNzkzMzk3Njg2LCJwbGF5ZXJBdHRhY2tOYW1lIjoiUkdCIGxpZ2h0cyIsImVuZW15QXR0YWNrTmFtZSI6IjEwIHNtdXJmcyAoR2V0IGl0PyBHZXQgaXQgVGhleSBhcmUgYmx1ZS4uLiBCbHVlIHRlYW0uLi4gbnZtLi4uKSIsImlhdCI6MTc2Mjc5MzQxMSwiZXhwIjoxNzYyNzk3MDExfQ&oeol=FF>), copy the output JSON into the input field. Replace the Base64 decode operation with Base64 encode. Modify the JSON data such that we win. For example `hpPlayer` to 100 and `hpEnemy` to 1
7. Copy out the resulting Base64 data. Insert it between the two dots in the original JWT, and remove any padding (`=` at the end)
8. Back in the network tab, right click → Edit and Resend. Modify the token in the body to the new token you created. In my case, `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJocFBsYXllciI6MTAwLCJocEVuZW15IjoxLCJyb3VuZCI6MiwicGxheWVyRGFtYWdlIjoxMCwiZW5lbXlEYW1hZ2UiOjM0LCJzdGFydGVkIjoxNzYyNzkzMzk3Njg2LCJwbGF5ZXJBdHRhY2tOYW1lIjoiUkdCIGxpZ2h0cyIsImVuZW15QXR0YWNrTmFtZSI6IjEwIHNtdXJmcyAoR2V0IGl0PyBHZXQgaXQgVGhleSBhcmUgYmx1ZS4uLiBCbHVlIHRlYW0uLi4gbnZtLi4uKSIsImlhdCI6MTc2Mjc5MzQxMSwiZXhwIjoxNzYyNzk3MDExfQ.`
9. Send the request. The response will pop up, with the flag in the `flag` field: `EPT{s1gn1ng_j4wt5_1s_fun}`
