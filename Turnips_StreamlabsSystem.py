import json
import random
import math
import time
import os

ScriptName = "Turnips"
Description = "Adds the stock market to your bot"
Creator = "Octahedron#5752"
Version = "1.0.0"
SpecialThanks = "https://www.twitch.tv/hypherius"
Website = ""

JsonFile = os.path.join(os.path.dirname(__file__), "turnips.json")
PriceTimer = 15 * 60 * 1000 # 15 minutes

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
    pass

def Execute(data):
    if not data.IsChatMessage():
        return

    command = data.GetParam(0).lower()

    if (command == "!turnips") or (command == "!turnip"):
        jsonData = readJson()
        verifyTurnipBalance(data.User)
        turnipBalance = json.dumps(jsonData['userBalances'][data.User])
        userBalance = Parent.GetPoints(data.User)
        turnipPrice = json.dumps(jsonData["turnips"]["price"])
        lastUpdated = jsonData["turnips"]["lastUpdated"]
        nextUpdate = lastUpdated + PriceTimer
        currentTime = int(round(time.time() * 1000))
        secondsUntilUpdate = int(math.floor((nextUpdate - currentTime) / 1000))
        minutesUntilUpdate = int(math.floor(secondsUntilUpdate / 60))
        secondsUntilUpdate = secondsUntilUpdate - minutesUntilUpdate * 60

        if (data.GetParam(1).lower() == "balance"):
            Parent.SendStreamMessage("You have " + turnipBalance + " turnips!");

        elif (data.GetParam(1).lower() == "price") or (data.GetParam(1).lower() == "value"):
            Parent.SendStreamMessage("Turnips are currently worth " + turnipPrice + " Trashbucks! The price will update in: " + str(minutesUntilUpdate) + "m " + str(secondsUntilUpdate) + "s ");

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
                Parent.SendStreamMessage("Successfully purchased " + str(quantity) + " turnips for " + str(price) + " Trashbucks!")
            else:
                Parent.SendStreamMessage("You cannot afford that many turnips.")

        elif data.GetParam(2).lower() == "sell":
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

def Tick():
    currentTime = int(round(time.time() * 1000))
    jsonData = readJson()
    if currentTime - jsonData["turnips"]["lastUpdated"] > PriceTimer:
        jsonData["turnips"]["price"] = random.randint(50, 500)
        jsonData["turnips"]["lastUpdated"] = currentTime
        writeJson(jsonData)
        Parent.SendStreamMessage("Turnip prices have updated! New price: " + str(jsonData["turnips"]["price"]) + " Trashbucks.")
    pass
