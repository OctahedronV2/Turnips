#---------------------------
#   Import Libraries
#---------------------------

import json
import random
import math
import time
import os
import sys
import codecs
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Turnips"
Description = "Adds the stock market to your bot."
Creator = "Octahedron"
Version = "1.1.0"
SpecialThanks = "https://www.twitch.tv/hypherius"
Website = "https://github.com/OctahedronV2/Turnips"

settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

JsonFile = os.path.join(os.path.dirname(__file__), "turnips.json")

class Settings(object):
    """ Load in saved settings file if available else set default values. """
    def __init__(self, settingsfile=None):
        Parent.Log(ScriptName, "Creating Settings Object")
        if settingsfile and os.path.isfile(settingsfile):
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        else:
            Parent.Log(ScriptName, "Setting To Default")
            self.Command = "!turnips"
            self.Cooldown = 4
            self.HelpMessage = "Check out the Turnips readme: https://github.com/OctahedronV2/Turnips/blob/main/README.md!"
            self.CurrencyName = "turnips"
            self.PriceUpdateFrequency = 2
            self.PriceUpdateUnit = "Hours"
            self.MinValue = 5
            self.MaxValue = 50
            self.HelpMessage = "Hey ${user}, check out the Turnips readme for help: https://github.com/OctahedronV2/Turnips/blob/main/README.md"
            self.CooldownMessage = "You are on cooldown for this command for another: ${cooldown}"
            self.BalanceMessage = "You have ${userTurnipBalance}."
            self.ValueMessage = "Turnips are currently worth ${turnipValue}! This price will update in: ${timeUntilPriceUpdate}"
            self.BuyMessage = "Successfully purchased ${quantity} for ${price}!"
            self.TooExpensiveMessage = "You cannot afford that many turnips."
            self.SellMessage = "Successfully sold ${quantity} for ${value}!"
            self.NotEnoughTurnipsMessage = "You do not have that many turnips."
            self.InvalidAmountMessage = "That is not a valid amount."
            self.PriceUppdateMessage = "Turnip prices have updated! New price: ${turnipValue}"

	def Reload(self, jsondata):
		""" Reload settings from Streamlabs user interface by given json data. """
		self.__dict__ = json.loads(jsondata, encoding="utf-8")

	def Save(self, settingsfile):
		""" Save settings contained within to .json and .js settings files. """
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")

def readJson():
    with open(JsonFile) as json_file:
        data = json.load(json_file)
        return data

def writeJson(jsonData):
    with open(JsonFile, 'w') as writefile:
        json.dump(jsonData, writefile, indent=2)

def verifyTurnipBalance(user):
    jsonData = readJson()
    if user not in jsonData['userBalances']:
        jsonData['userBalances'][user] = 0
        writeJson(jsonData)

def SendMessage(data, Message):
    Message = Message.replace("${user}", data.UserName)
    Message = Message.replace("${currencyName}", Parent.GetCurrencyName())
    Message = Message.replace("${customCurrencyName}", ScriptSettings.CurrencyName)
    Message = Message.replace("${cooldown}", str(Parent.GetUserCooldownDuration(ScriptName, ScriptSettings.Command, data.User)) + " second" + ("s" if Parent.GetUserCooldownDuration(ScriptName, ScriptSettings.Command, data.User) != 1 else ""))
    Parent.SendStreamMessage(Message)

def Init():

    global ScriptSettings
    ScriptSettings = Settings(settingsfile)

    global PriceTimer

    # time stuff
    timeUnit = ScriptSettings.PriceUpdateUnit
    timeAmount = ScriptSettings.PriceUpdateFrequency
    if timeUnit == "Seconds":
        PriceTimer = timeAmount * 1000
    elif timeUnit == "Minutes":
        PriceTimer = timeAmount * 1000 * 60
    elif timeUnit == "Hours":
        PriceTimer = timeAmount * 1000 * 60 * 60
    elif timeUnit == "Days":
        PriceTimer = timeAmount * 1000 * 60 * 60 * 24
    else:
        PriceTimer = timeAmount
    return

def ReloadSettings(jsondata):

    Init()

    return

def Execute(data):
    if not data.IsChatMessage():
        return

    command = data.GetParam(0).lower()

    if command == ScriptSettings.Command:
        if Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User):
            cooldown = Parent.GetUserCooldownDuration(ScriptName, ScriptSettings.Command, data.User)
            SendMessage(data, ScriptSettings.CooldownMessage)
            return
        Parent.AddUserCooldown(ScriptName, ScriptSettings.Command, data.User, ScriptSettings.Cooldown)
        jsonData = readJson()
        verifyTurnipBalance(data.User)
        turnipBalance = jsonData['userBalances'][data.User]
        userBalance = Parent.GetPoints(data.User)
        turnipPrice = jsonData["turnips"]["price"]
        lastUpdated = jsonData["turnips"]["lastUpdated"]
        nextUpdate = lastUpdated + PriceTimer
        currentTime = int(round(time.time() * 1000))

        secondsUntilUpdate = int(math.floor((nextUpdate - currentTime) / 1000)) # get in seconds
        Parent.Log(ScriptSettings.Command, str(secondsUntilUpdate))
        secondsUntilUpdate = secondsUntilUpdate % (24 * 3600)
        hoursUntilUpdate = secondsUntilUpdate // 3600
        secondsUntilUpdate %= 3600
        minutesUntilUpdate = secondsUntilUpdate // 60
        secondsUntilUpdate %= 60
        quantity = 0

        if (data.GetParam(1) == "") or (data.GetParam(1).lower() == "help"):
            message = ScriptSettings.HelpMessage

        elif (data.GetParam(1).lower() == "balance"):
            message = ScriptSettings.BalanceMessage
            # Parent.SendStreamMessage("You have " + str(turnipBalance) + " turnip" + ("s." if cooldown != 1 else "."));

        elif (data.GetParam(1).lower() == "price") or (data.GetParam(1).lower() == "value"):
            message = ScriptSettings.ValueMessage

        elif data.GetParam(1).lower() == "buy":
            if data.GetParam(2).lower() == "max" or data.GetParam(2).lower() == "all":
                quantity = int(math.floor(userBalance / turnipPrice))
                if quantity == 0:
                    Parent.SendStreamMessage("You cannot afford any turnips!") # TODO: make this message customizable
                    return
            else:
                try:
                    if int(data.GetParam(2)) < 1:
                        message = ScriptSettings.InvalidAmountMessage
                        SendMessage(data, message)
                        return
                    else:
                        quantity = int(data.GetParam(2))
                except:
                    message = ScriptSettings.InvalidAmountMessage
                    SendMessage(data, message)
                    return

            price = turnipPrice * quantity
            if userBalance >= price:
                jsonData["userBalances"][data.User] += quantity
                writeJson(jsonData)
                Parent.RemovePoints(data.User, data.UserName, price)
                message = ScriptSettings.BuyMessage
            else:
                message = ScriptSettings.TooExpensiveMessage

        elif data.GetParam(1).lower() == "sell":
            if data.GetParam(2).lower() == "all" or data.GetParam(2).lower() == "max":
                if turnipBalance > 0:
                    quantity = turnipBalance
                else:
                    Parent.SendStreamMessage("You do not have any turnips!") # TODO: make this message customizable
                    return
            else:
                try:
                    if int(data.GetParam(2)) < 1:
                        message = ScriptSettings.InvalidAmountMessage
                        SendMessage(data, message)
                        return
                    else:
                        quantity = int(data.GetParam(2))
                except:
                    message = ScriptSettings.InvalidAmountMessage
                    SendMessage(data, message)
                    return

            value = turnipPrice * quantity
            if turnipBalance >= quantity:
                jsonData["userBalances"][data.User] -= quantity
                writeJson(jsonData)
                Parent.AddPoints(data.User, data.UserName, value)
                message = ScriptSettings.SellMessage
            else:
                message = ScriptSettings.NotEnoughTurnipsMessage
        message = message.replace("${turnipValue}", str(turnipPrice) + " " + Parent.GetCurrencyName())
        message = message.replace("${userTurnipBalance}", str(turnipBalance) + " " + ((ScriptSettings.CurrencyName + "s") if turnipBalance != 1 else ScriptSettings.CurrencyName))
        message = message.replace("${timeUntilPriceUpdate}", str(hoursUntilUpdate) + "h " + str(minutesUntilUpdate) + "m " + str(secondsUntilUpdate) + "s ")
        try:
            message = message.replace("${quantity}", str(quantity) + " " + ((ScriptSettings.CurrencyName + "s") if quantity != 1 else ScriptSettings.CurrencyName))
        except:
            pass
        try:
            message = message.replace("${price}", str(price) + " " + Parent.GetCurrencyName())
        except:
            pass
        try:
            message = message.replace("${value}", str(value) + " " + Parent.GetCurrencyName())
        except:
            pass
        SendMessage(data, message)
        return

def Tick():
    try:
        currentTime = int(round(time.time() * 1000))
        jsonData = readJson()
        if currentTime - jsonData["turnips"]["lastUpdated"] > PriceTimer:
            jsonData["turnips"]["price"] = random.randint(ScriptSettings.MinValue, ScriptSettings.MaxValue)
            jsonData["turnips"]["lastUpdated"] = currentTime
            writeJson(jsonData)
            turnipPrice = jsonData["turnips"]["price"]
            message = ScriptSettings.PriceUpdateMessage
            message = message.replace("${turnipValue}", str(turnipPrice) + " " + Parent.GetCurrencyName())
            Parent.SendStreamMessage(message)
    except:
        pass
    pass
