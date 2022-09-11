Portuguese COVID statistics telegram Bot
=

This is a simple telegram bot that retrieves some data from Our World in Data (OWID) datasets about COVID in Portugal.

There's just a single `/stats` command that causes the bot to retrieve statistics and output the result to the caller.

Local Usage
-
You can test locally by invoking:


```
source .venv/Scripts/activate
python local-invoke.py
```

Which should print the result to the console.

Deployment with Heroku
- 

This bot was written for the Heroku cloud. It requires two
configuration environment variables to work on telegram/Heroku:
* `WEB_HOOK_URL`
* `TG_TOKEN`

These can be set with:

`heroku config:set --remote origin  WEB_HOOK_URL="https://XXXXXX.herokuapp.com/" TG_TOKEN="XXXXX"`