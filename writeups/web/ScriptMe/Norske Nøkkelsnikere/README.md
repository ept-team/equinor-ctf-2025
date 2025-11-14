# 'ScriptMe' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

The challenge description states that it might be useful to look at what the browser is doing, so I started by focusing on that. There is no handout. The website has buttons for seeing the flag, registering and logging in. The flag page requires being logged in. After registering you will fail to login:

> You need to have a magic passord. So no secret for you.

Going into the code of the login page we see the following code:

```js
if (res.status === 200) {
  const keyres = await fetch('/key', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  const key = await keyres.text();
  const expectedKey = toBase64(password.trim());
}
```

This suggests that our password must be the value returned by `/key` after base64 decoding it. I used the network tab to find the request, and checked the response. It was `VGhpcyBpcyB0aGUgbWFnaWMgcGFzc3dvcmQh`. After using [CyberChef](<https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=VkdocGN5QnBjeUIwYUdVZ2JXRm5hV01nY0dGemMzZHZjbVFo>) to base64 decode it, we get the secret password: `This is the magic password!`.

I created a new account with that as the password, and tried logging in again, which worked. The flag was presented on the screen: `EPT{Javascript_can_b3_fun_4_all!}`.

In real world web applications going into the frontend source code can often be a valuable insight. There have been many cases of things being leaked there, for example sensitive API keys.
