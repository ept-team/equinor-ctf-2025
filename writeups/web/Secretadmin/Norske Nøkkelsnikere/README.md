# 'Secretadmin' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

There is no handout for the challenge, so I started by starting the instance. The website is very basic, you can register, login, and see the flag. To see the flag you need to be an admin. The challenge description mentions cookies, so we can start by investigating how the website uses cookies. After logging in, there is a `role` cookie set to `user`. What would happen if we changed the role to admin?

1. Open the instance in Firefox
2. Register an account and login
3. Go to the admin page, and notice not having permission to view the flag
4. Open the devtools and navigate to the "Storage" tab. Open cookies
5. Set the value of the `role` cookie to `admin` by double-clicking on it
6. Refresh the page

The flag will be displayed: `EPT{Cookies_4_the_Win!!}`

In real world applications, this is very unlikely to be possible. Most applications use JSON Web Tokens (JWTs) to store authentication data such as user id and role. These tokens are cryptographically signed such that manipulation by the client will be detected. There can of course be weaknesses in these tokens, such as in the "Hackermon" challenge.
