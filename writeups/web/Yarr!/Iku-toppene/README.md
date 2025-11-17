# 🔥 Yarr! 🔥
### Team: Iku-toppene 🐮
**Author:** Shirajuki

```
Ahoy! I made a service t' host all me fav'rit pirate games from me youth.
But arr, they were nah as jolly as I remembered 'em. Could ye help me find me treasure?
Remember dat X marks the spot.
```

### Challenge overview

Ahoy! In dis CTF challenge, we be handed a wee web service dat proxies requests to a set o' pirate-themed games.

The frontend exposes a URL o' the form: `https://ikutoppene-xxxxxxxx-yarr.ept.gg/<game>/`.
Below deck, the backend grabs the `<game>` name 'an fetches `http://<game>.games.ept:80/`.

Thar be a handful o' honest games (like treasure, barrels, kraken), but there also be a hidden virtual host:
```
server_name x.marks.the.spot.ept;
root /app/secrets/;
```

Dis hidden host serves `/flag.txt`, the treasure we crave.

The grand plan be:
- We command the `game` part o' the hostname.
- We can nah directly set the path ('tis always `/` in the backend).
- We must twist this control so the internal service fetches `/flag.txt` from `x.marks.the.spot.ept`.

### Source code analysis

Relevant parts o' `main.py`:
```py
def filter_bad_characters(text):
    for forbidden_char in ";<=>?@":
        text = text.replace(forbidden_char, ".")
    return text

async def fetch_game(request):
    game = filter_bad_characters(request.match_info["game"])
    print(f"http://{game}.games.ept:80/", flush=True)

    connector = TCPConnector(ssl=False)

    async with ClientSession(connector=connector) as session:
        try:
            async with session.get(f"http://{game}.games.ept:80/") as response:
                text = await response.text()
                return web.Response(text=text, content_type="text/html")
        except Exception as e:
            return web.Response(text=f"Error fetching game '{game}': {str(e)}", status=500)
```

Key observations fer the crew:
- We hold full sway over `game` (aside from the proxy regex an' sanitizer), an' it be interpolated directly straight into the URL. Tryin' to escape with `@`, `/` or `#` fails cause o' the sanitizer an' the proxy normalizes the path clean also.
- The sanitizer be a soggy biscuit: it swaps forbidden characters fer `.` instead o' scuttlin' 'em, lettin' us reshape the host to taste.
- The backend always asks fer `/` from the chosen host, so shoutin' `x.marks.the.spot.ept/flag.txt` as the game ain't possible'; the `game` slice becomes part o' the host while the path stays nailed at `/`.
- `aiohttp`'s `ClientSession.get` follows redirects (`allow_redirects=True`), so any matey that answers with `3XX Location: http://x.marks.the.spot.ept/flag.txt` will have the backend fetch the booty fer us.


Dat be the key: we do nah needs to steer n' control the path directly, we jus' needs an intermediate host dat redirects t' the correct path.

### IPv6

Another crucial detail o' the challenge be dat URLs support literal IPv6 addresses inside square brackets, as defined in [RFC 2732](https://datatracker.ietf.org/doc/html/rfc2732#section-2).

Another interestin' quirk be dat `aiohttp` / `yarl` ignores everythin' aft the closin' `]` when determinin' the connection target. So if the backend constructs `http://[::ffff:3.123.45.67].games.ept:80/`, `aiohttp` parses dis as jus' `http://[::ffff:3.123.45.67]:80/`.

As a result, the appended `.games.ept` ain't part o' the hostname at all. Dis lets us make the backend connect directly t' an arbitrary IPv6 address we fancy.

### Redirect for flag

Since we can make the backend connect t' our server (via dis IPv6 trick), 'n 'cause it follows redirects, the final exploit chain be:

1. We run a wee HTTP server on our own box that always redirects t' the flag: `http://x.marks.the.spot.ept/flag.txt`.
2. We point the `<game>` t' our server usin' the IPv6 address trick.
3. The backend fetches `http://[<our-server>].games.ept/`.
4. Our server returns a `301 Location: http://x.marks.the.spot.ept/flag.txt`.
5. `aiohttp` follows dis redirect 'n fetches `/flag.txt` from the internal Nginx vhost `x.marks.the.spot.ept`.
6. The response (containin' the flag) be sent back t' us by the challenge app.

An example server fer the job sits in [server.py](./server.py).

Run it on a host the challenge can reach (i.e., from the EPT box). Make sure the host's network be flyin' the colors o' IPv6. Fire the payload an' the flag comes rushin' back like treasure on the tide!
```sh
$ sudo python3 server.py &
$ nslookup ikutoppene-9297aa7d-eptbox.eptc.tf
Server:         10.255.255.254
Address:        10.255.255.254#53

Non-authoritative answer:
Name:   ikutoppene-xxxxxxxx-eptbox.eptc.tf
Address: 3.123.45.67

$ curl 'https://ikutoppene-xxxxxxxx-yarr.ept.gg/[::ffff:3;123;45;67]/' --path-as-is
EPT{yarl!_t1me_f0r_s0m3_gr0g_4ft3r_4ll_th4t_p1ll4g1ng}
```
