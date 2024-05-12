# Luminar Banking discord bot
An economy discord bot made in python, if you want to check out the <a href="https://discord.gg/K8tHJChJ2v">discord</a>

# Features
#### Slash commands
* `/fee` - Slash command, allows users to calculate the current withdraw fee
* `/interest` - Slash command, allows users to calculate the current interest rate
* `/bal` - Slash command, shows user his personal balance
* `/flex` - Slash command, shows users his personal balance and his username along side it
* `/pay` - Slash command, allows user to pay another user via there username
* `/withdraw` - Slash command, allows user to withraw (sends the funds to the Owner's balance)
#### Ctx commands (admin commands)
* `allbalance` - All balance ctx command, sums up all balances, except for the owner's balance, and gives an entire bank balance amount (admin only)
* `logs` - Logging ctx command, for logging the `Bal.json` file manually, it is logged automaticlly every week before and after interest payment (admin only)
* `pay_interest` - Paying interest ctx command, for mannually paying interest, it is done automaticlly every week (admin only)

# Setup
### To setup the bot properly, make sure to specify all of the below:
#### Settings
* `TOKEN = ""` - Put in your discord bot token, you can get yours <a href="https://discord.com/developers/applications">here</a>
* `OWNER` - Put owner discord id here (int)
* `co_OWNER` - Put co-owner discord id here (int)
* `bank_name` - Put your desired bank name here (str)
* `interest_rate` - Put your desired the interest rate here % (float)
* `withdraw_fee` - Put your desired withdraw fee rate % (float)
* `emoji` - Put your desired emoji here, used to mark withdrawl messages in withdraws channel
* `colour_stripe` - Discord message embed stripe color (discord.Colour() object)
#### Channels (all int)
* `withdraws` - Withraw discord channel id
* `log` - Logs discord channel id
* `allbal` - All balance command discord channel id
* `Console_channel` - Console discord channel id
* `interest_channel` - Interest discord channel id
* `error_channel` - Errors discord channel id
* `server_id` - Discord server id
#### `Bal.json`
```
{
    "accounts": [
        {
            "user_id": (int),
            "balance": (int)
        },
        {
            "user_id": (int),
            "balance": (int)
        }
]
}
```

# Files and miscellaneous
* `main.py` - Main python discord bot file, defines the roles and channels it uses, handles the frontend and makes all commands
* `responses.py` - Backend python file, holds and manipulates all balances
* `Bal.json` - Stores all user ids and there respective balances

## Libraries used:
* `discord.py` - Python discord bot
* `datetime` - Time handiling
* `pytz` - For timezones
* `asyncio` - Discord bot reconnection loop
* `time` - For unix time handling
* `json` - Allows you to interect and manipulate json files
* `datetime` - For time log handling
* `calendar` - For unix time handling
#### To install all libraries, do:
```
pip install -r requirements. txt
```

# License
This repository is licensed under the Unlicense license.

See LICENSE for details.