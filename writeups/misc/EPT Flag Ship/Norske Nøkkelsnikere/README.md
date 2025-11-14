# 'EPT Flag Ship' writeup

**Writeup author**: piprett (Norske Nøkkelsnikere)

As usual I started by downloading and analyzing the handout. It is a pretty simple HTTP service. The user inputs an e-mail address, and the program will send the flag there. There is only one condition: the e-mail address must end in `@ept.gg`. I don't have an `@ept.gg` e-mail address, so we will have to find another way.

The sending of the e-mail happens using AWS SES using the `boto3` python library. Our initial thoughts were to try finding some seperator that would send the e-mail to multiple people. For example we tried using `example@nnsctf.no;example@ept.gg`. This did not work.

Not having any obvious ideas, I tried reading the documentation for the `boto3` library. I found the [reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/client/send_email.html) for the `send_mail` function:

> ToAddresses (list) –
> The recipients to place on the To: line of the message.
> (string) –

This doesn't really help us. I thought about the format for e-mail addresses and remembered that you can do `Display Name <example@nnsctf.no>`. What if we did this in the opposite order? `<example@nnsctf.no> Display Name`. Then we could set our display name to end in `@ept.gg`. This worked. Our final payload became `<example@nnsctf.no> example@ept.gg`. The flag was received in our spam folder.

It is generally not a good practice to just check the end of e-mail addresses or URLs. Instead one should use a proper parser, check the domain, and then use the output of the parser when sending the e-mail.
