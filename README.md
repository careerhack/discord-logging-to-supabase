# discord-logging-to-supabase
Discord bot for streaming data from an authorized channel within a server and logging to Supabase.

## Database
This particular flavor uses [Supabase](https://supabase.com/pricing) to log messages from Discord channels.

Server and channel IDs need to be MANUALLY ADDED via connection to the database. In the future this will be handled via an API.


## Python dev setup
Set up a virtual environment by running
```
python3 -m virtualenv .
```
This will initalize a virtual environment in this directory.

To enter the virtual environment, run
```
source bin/activate
```

To install library dependencies, run
```
pip install -r requirements.txt
```

## Bot tokens
A token for the bot can be retrieved from the [Discord Developer Applications panel](https://discord.com/developers/applications/). You may save it to a file named `config.json`, styled like so:
```
{
    "token":"<bot token>",
    "client_id":"<client id>",
    "client_secret":"<client secret>"
}
```
This page has more info on how to add the bot to the server: [https://discordpy.readthedocs.io/en/stable/discord.html](https://discordpy.readthedocs.io/en/stable/discord.html).

Adding the bot to your server will depend on authorizing it via the Discord OAuth2 url generated here:
`https://discord.com/api/oauth2/authorize?client_id=928752486817341460&permissions=1374389738496&scope=bot`



## API Server
Use the [Supabase REST API](https://supabase.com/docs/reference/javascript/supabase-client) to interact with the database.