# Turnips
**Turnips script for Streamlabs Chatbot**  
*(special thanks to twitch.tv/hypherius for the idea)*

## Command Usage

**!turnips help** - Links you here! (*EX: !turnips help **OR** !turnips*)  
**!turnips balance** - Tells you how many turnips you have. (*EX: !turnips balance*)  
**!turnips price** - Tells you how much turnips are worth. (*EX: !turnips price **OR** !turnips value*)  
**!turnips buy [num/max]** - Buys the given number of turnips. (*EX: !turnips buy 10*)  
**!turnips sell [num/all]** - Sells the given number of turnips. (*EX: !turnips sell 10*)

## Customization  
*In order to be useful to as many people as possible, I have made many parts of the bot customizable*  
  
### Basics  
  
**Command** - The command with which you use the bot.  
**Currency Name** - The name of your "turnips" (Note: this value is designed to be singular, not plural).  
**Cooldown** - How many seconds users have to wait to use the command again.  

### Custom Message Variables
*Custom variables are used using the following format: **${variable}**

**${user}** - Gives the username of the user (EX: "Octatypes")
**${currencyName}** - Gives the name of your Streamlabs Chatbot's currency (EX: "Coins")
**${customCurrencyName}** - Gives the name of your custom Turnips currency (EX: "Turnip")
**${cooldown}** - Gives the user's cooldown (EX: "5 seconds")
**${turnipValue}** - Gives the current turnip price (EX: "27 Coins")
**${userTurnipBalance}** - Gives the user's turnip balance (EX: "5 Turnips")
**${timeUntilPriceUpdate}** - Gives the time until the next price update (EX: "5h 37m 21s")
**${quantity}** - Gives the number of turnips that are being bought/sold (EX: "5 Turnips")
**${price}** - Gives the cost of the turnips that are being bought (EX: "37 Coins")
**${value}** - Gives the value of the turnips that are being sold (EX: "82 Coins")

*Note: Be sure to pay attention to the examples, as many of these variables include units*
*Note 2: cooldown, turnipValue, userTurnipBalance, quantity, price, and value will have units automatically pluralized by adding an "s" to the end.
  
### Custom Messages  
  
**Help Message** - The message displayed when the user uses *!turnips help* or *!turnips*.  
*Compatible Variables: user, currencyName, customCurrencyName*

**Cooldown Message** - The message displayed when the user is still on cooldown.
*Compatible Variables: user, currencyName, customCurrencyName, cooldown*

**Balance Check Message** - The message displayed when the user uses *!turnips balance*
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate*

**Turnip Value Message** - The message displayed when the user uses *!turnips value*.  
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate*

**Turnip Buy Message** - The message displayed when the user successfully uses *!turnips buy*.  
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate, quantity, price*

**Too Expensive Message** - The message displayed when the user tries to buy more turnips than they can afford.  
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate*

**Sell Message** - The message displayed when the user successfully uses *!turnips sell*.  
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate, quantity, value*

**Not Enough Turnips Message** - The message displayed when the user tries to sell more turnips than they have.  
*Compatible Variables: user, currencyName, customCurrencyName, turnipValue, userTurnipBalance, timeUntilPriceUpdate*

**Invalid Amount Message** - The message displayed when the user inputs an invalid number amount like *-1* or *asdf*.  
*Compatible Variables: user, currencyName, customCurrencyName*

**Price Update Message** - The message displayed when the turnip price updates.  
*Compatible Variables: turnipValue*
