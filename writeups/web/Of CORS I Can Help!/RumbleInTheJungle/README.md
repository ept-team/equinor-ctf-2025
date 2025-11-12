# Of CORS I Can Help!

Writeup by: `snerk312`

On line 173 in main.py, there is a check for whether the path starts with "/flag". This both indicated where the flag was, and told us why Jenny wont give us the flag when just sending:

```
https://rumbleinthejungle-619799cf-ofcors.ept.gg/static/flag
```

To bypass this, we added a "/" to the path before "/flag", which in the end is interpreted as the same file regardless of the extra "/".

```
https://rumbleinthejungle-619799cf-ofcors.ept.gg/static//flag
```

Flag: `EPT{CORS_t0tally_trU5t5_y0u}`