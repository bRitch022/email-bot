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
```apt-get install python3.10 python3.10-dev python3.10-venv```  

Ensure `python` is a link that points to python3.10  
```ls -l `which python`*```

If it is not:  
Assuming `python` is in `/usr/bin/`  
```rm /usr/bin/python```  
```ln -s /usr/bin/python3.10 /usr/bin/python```  

From the `email-bot` directory:  
```python -m venv pyenv```  
```source pyenv/bin/activate```  
```python -m pip install -r requirements.txt```

## Environment Variable Setup
* The `email-dot/emailHandler` directory contains a file called `.env.example`. Copy this file and rename it to `.env`.
** Note: The `.gitignore` file ignores .env files, so there is no risk of accidentally commiting credentials to the repo.
* Fill in credentials for `USERNAME` and `PASS` within the `.env` file, and Voilà!

## Setup for Gmail (Depricated)
Gmail is quite secure, you'll need to enable 'Less Secure App Access'  
https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4NULCpvZyDMav0aPPVtnzCgGlmwCE8ejYSYlK4GogISJv4SlFyBovsOdbcNXsI-Qi19WnBGdfTi02htCGvYVZY7u-sEHA

Actually, we are now using OAuth2, and a `credentials.json` file containing the API key and secret is required to be in the `emailHandler` directory 
