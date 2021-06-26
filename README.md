# email-bot
A bot designed to quickly and autonomously reply to emails which meet one or more certain criteria

## Use case
1) A user wishes to rapidly and autonomously reply to an email which matches sender criteria
2) A user wishes to rapidly and autonomously reply to an email which matches subject line criteria
3) A user wishes to rapdily and autonomously reply to an email which matches message body criteria

## Program Requirements
1) Program must run autonomously and automatically
2) Program must monitor a given email at all times without the need for the user to host the program
3) Program must be accessible from both Apple and Windows machines

## End User Requirements
1) User must have the ability to create or modify a reply message
2) User must have the ability to specify the desired sender, subject line, and/or message body criteria
3) User must have the ability to enter personal email credentials without those credentials being compromised

## Python Environment Setup
From within Linux environment:  
```sudo apt-get update```

From the `email-bot` directory:  
```python3 -m venv pyenv```  
```source pyenv/bin/activate```  
```python3 -m pip install -r pyenv/requirements.txt```

## Environment Variable Setup
* The `email-dot/emailHandler` directory contains a file called `.env.example`. Copy this file and rename it to `.env`.
** Note: The `.gitignore` file ignores .env files, so there is no risk of accidentally commiting credentials to the repo.
* Fill in credentials for `USERNAME` and `PASS` within the `.env` file, and Voilà!

## Setup for Gmail (Not yet working)
Gmail is quite secure, you'll need to enable 'Less Secure App Access'  
https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4NULCpvZyDMav0aPPVtnzCgGlmwCE8ejYSYlK4GogISJv4SlFyBovsOdbcNXsI-Qi19WnBGdfTi02htCGvYVZY7u-sEHA
