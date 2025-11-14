# 'LOUD CRM' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

## Source code analysis

I started by downloading the provided source code handout. I quickly looked through the code, and noticed authentication did some strange things with capitalisation of usernames. Specifically I noticed the following code during the registration process:

```python
if username == username.upper() and auth.user_exists_upper(username):
  flash("That handle already exists. Choose a different one.")
  return render_template("register.html", form=request.form)
```

The code checks if the inputted username is the same after being converted to uppercase (effectively if the username is in uppercase), and if there is already a user with that username. That means that we can register a "taken" username by not using full uppercase letters. This works because when registering, the username is turned into uppercase.

```python
def register_user(...) -> UserRecord:
    username_upper = username.upper()
```

## Attack

As specified in the challenge description, our goal is to login as Alice who has the flag.

1. Start an instance and open it in your browser
2. Go to registration. We know that Alice has the flag, so use that as the handle. Use whatever displayname and passphrase you wish
3. Open the Firefox devtools and go to the network tab
4. Press "create access" to create an account
5. Notice error as the username is already taken
6. Right click the request, press "Edit and Resend"
7. Update the body to have the username Alice not be in full uppercase
8. Resend the request
9. Login as Alice with the password you set

You will be shown the flag: `EPT{LOUD_HANDLE_OVERRIDE}`
