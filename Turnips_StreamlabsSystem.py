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
Version = "1.0.1"
SpecialThanks = "https://www.twitch.tv/hypherius"
Website = ""

settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")

JsonFile = os.path.join(os.path.dirname(__file__), "turnips.json")
PriceTimer = 15 * 60 * 1000 # 15 minutes

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

def Init():

    global ScriptSettings
    ScriptSettings = Settings(settingsfile)

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
            Parent.SendStreamMessage("You are on cooldown for this command for another: " + str(cooldown) + " second"  + ("s." if cooldown != 1 else "."))
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
        secondsUntilUpdate = int(math.floor((nextUpdate - currentTime) / 1000))
        minutesUntilUpdate = int(math.floor(secondsUntilUpdate / 60))
        secondsUntilUpdate = secondsUntilUpdate - minutesUntilUpdate * 60

        if (data.GetParam(1) == "") or (data.GetParam(1).lower() == "help"):
            Parent.SendStreamMessage(ScriptSettings.HelpMessage)

        elif (data.GetParam(1).lower() == "balance"):
            Parent.SendStreamMessage("You have " + str(turnipBalance) + " turnip" + ("s." if cooldown != 1 else "."));

        elif (data.GetParam(1).lower() == "price") or (data.GetParam(1).lower() == "value"):
            Parent.SendStreamMessage("Turnips are currently worth " + str(turnipPrice) + " Trashbucks! The price will update in: " + str(minutesUntilUpdate) + "m " + str(secondsUntilUpdate) + "s ");

        elif data.GetParam(1).lower() == "buy":
            if data.GetParam(2).lower() == "max":
                quantity = int(math.floor(userBalance / turnipPrice))
            else:
                try:
                    if int(data.GetParam(2)) < 1:
                        Parent.SendStreamMessage("That is not a valid amount.")
                    else:
                        quantity = int(data.GetParam(2))
                except:
                    Parent.SendStreamMessage("That is not a valid amount.")
                    return

            price = turnipPrice * quantity
            if userBalance >= price:
                jsonData["userBalances"][data.User] += quantity
                writeJson(jsonData)
                Parent.RemovePoints(data.User, data.UserName, price)
                Parent.SendStreamMessage("Successfully purchased " + str(quantity) + (" turnips for " if quantity != 1 else " turnip for ") + str(price) + " Trashbucks!")
            else:
                Parent.SendStreamMessage("You cannot afford that many turnips.")

        elif data.GetParam(1).lower() == "sell":
            if data.GetParam(2).lower() == "all":
                quantity = userBalance
            else:
                try:
                    if int(data.GetParam(2)) < 1:
                        Parent.SendStreamMessage("That is not a valid amount.")
                    else:
                        quantity = int(data.GetParam(2))
                except:
                    Parent.SendStreamMessage("That is not a valid amount.")
                    return

            value = turnipPrice * quantity
            if userBalance >= quantity:
                jsonData["userBalances"][data.User] -= quantity
                writeJson(jsonData)
                Parent.AddPoints(data.User, data.UserName, value)
                Parent.SendStreamMessage("Successfully sold " + str(quantity) + " turnips for " + str(value) + "!")
        return

def Tick():
    currentTime = int(round(time.time() * 1000))
    jsonData = readJson()
    if currentTime - jsonData["turnips"]["lastUpdated"] > PriceTimer:
        jsonData["turnips"]["price"] = random.randint(50, 500)
        jsonData["turnips"]["lastUpdated"] = currentTime
        writeJson(jsonData)
        Parent.SendStreamMessage("Turnip prices have updated! New price: " + str(jsonData["turnips"]["price"]) + " Trashbucks.")
    pass
