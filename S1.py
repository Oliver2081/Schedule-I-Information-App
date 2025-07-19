# Schedule I Information Tool
# Version 2.0.3
# Copyright (c) 2025 Oliver2081


import os
import requests
import json
from bs4 import BeautifulSoup
import questionary as q


# ~~~~ Variables ~~~~ #
USERNAME = os.getlogin()
SAVEPATH = f"C:\\Users\\{USERNAME}\\AppData\\LocalLow\\TVGS\\Schedule I\\Saves"

usernames = {}
saveFiles = {}

ranks = ["Street Rat", "Hoodlum", "Peddler", "Hustler", "Bagman", "Enforcer", "Shot Caller", "Block Boss", "Underlord", "Baron", "Kingpin"]

items = {
    "ogkush": "OG Kush",
    "sourdiesel": "Sour Diesel",
    "greencrack": "Green Crack",
    "granddaddypurple": "Granddaddy Purple",
    "meth": "Meth",
    "cocaine": "Cocaine",
    "addy": "Addy",
    "banana": "Banana",
    "battery": "Battery",
    "chili": "Chili",
    "cuke": "Cuke",
    "donut": "Donut",
    "energydrink": "Energy Drink",
    "flumedicine": "Flu Medicine",
    "gasoline": "Gasoline",
    "horsesemen": "Horse Semen",
    "iodine": "Iodine",
    "megabean": "Mega Bean",
    "motoroil": "Motor Oil",
    "mouthwash": "Mouth Wash",
    "paracetamol": "Paracetamol",
    "viagor": "Viagra",
}

mixers = ["addy", "banana", "battery", "chili", "cuke", "donut", "energydrink", "flumedicine", "gasoline", "horsesemen", "iodine", "megabean", "motoroil", "mouthwash", "paracetamol", "viagor"]

effects = {
    "athletic": "Athletic",
    "antigravity": "Anti-Gravity",
    "balding": "Balding",
    "brighteyed": "Bright-Eyed",
    "caloriedense": "Calorie-Dense",
    "calming": "Calming",
    "cyclopean": "Cyclopean",
    "disorienting": "Disorienting",
    "electrifying": "Electrifying",
    "energizing": "Energizing",
    "explosive": "Explosive",
    "euphoric": "Euphoric",
    "focused": "Focused",
    "foggy": "Foggy",
    "gingeritis": "Gingeritis",
    "giraffying": "Long-Faced",
    "glowing": "Glowing",
    "jennerising": "Jennerising",
    "laxative": "Laxative",
    "munchies": "Munchies",
    "paranoia": "Paranoia",
    "refreshing": "Refreshing",
    "schizophrenic": "Schizophrenic",
    "seizure_inducing": "Seizure-Inducing",
    "sedating": "Sedating",
    "shrinking": "Shrinking",
    "smelly": "Smelly",
    "sneaky": "Sneaky",
    "slippery": "Slippery",
    "spicy": "Spicy",
    "thoughtprovoking": "Thought-Provoking",
    "toxic": "Toxic",
    "tropicthunder": "Tropic Thunder",
    "zombifying": "Zombifying",
}


# ~~~~ Functions ~~~~ #
def decodeSteamUserId(steamUserId):
    url = f'https://steamcommunity.com/profiles/{steamUserId}/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            parser = BeautifulSoup(response.text, 'html.parser')
            username = parser.find('span', {'class': 'actual_persona_name'})
            if username:
                return username.text
            else:
                return steamUserId
        else:
            return steamUserId
            
    except Exception as e:
        return steamUserId
    
def decodeSaveName(save):
    with open(f"{save}/Game.json", 'r') as file:
        data = json.load(file)
    
    organisationName = data.get('OrganisationName')
    
    file.close()
    return organisationName
    
def readSaveFile():
    with open(f"Products.json", 'r') as productSaveFile:
        productSaveData = json.load(productSaveFile)
    
    weedData = productSaveData.get("CreatedWeed")
    methData = productSaveData.get("CreatedMeth")
    cocaineData = productSaveData.get("CreatedCocaine")
    
    recipes = productSaveData.get("MixRecipes")
    
    saveData = {
        "weedData": weedData,
        "methData": methData,
        "cocaineData": cocaineData,
        "recipes": recipes,
        }
        
    productSaveFile.close()
    return saveData

def readRank(ranksList):
    romanNumerals = {1:"I", 2:"II", 3:"III", 4:"IV", 5:"V"}
    
    with open(f"Rank.json", 'r') as rankFile:
        rankData = json.load(rankFile)
    
    rank = int(rankData.get("Rank"))
    tier = int(rankData.get("Tier"))
    xp = int(rankData.get("TotalXP"))
    
    rankStr = ranksList[rank]
    tierStr = romanNumerals[tier]
    
    return f"{rankStr} {tierStr}", xp

def findRecipe(saveData, productId, productName):
    finished = False
    recipes = saveData.get("recipes", [])
    process = []
    
    while True:
        for r in recipes:
            if r.get("Output") == productId:
                process.append(r.get("Mixer") if r.get("Mixer") in mixers else r.get("Product")) # Bug which causes mixers and products to occasionally get swapped
                productId = r.get("Product") if r.get("Product") not in mixers else r.get("Mixer") # ^
                
                if productId in ["ogkush", "sourdiesel", "greencrack", "granddaddypurple", "meth", "cocaine"]:
                    process.append(productId)
                    finished = True
                    break
                    
        if finished:
            process.reverse()
            break

    # Replace IDs with names from items dict
    for i, step in enumerate(process):
        if step in items:
            process[i] = items[step]
    
    processStr = " + ".join(process)
    return processStr

def findDrugAmt(drug):
    HOMEDIR = os.getcwd() # Save Current Path
    properties = []
    players = []

    drugAmtRaw = 0
    drugAmtBag = 0
    drugAmtJar = 0
    drugAmtBrick = 0
    
    os.chdir("Properties")
    
    for file in os.listdir():
        properties.append(f"Properties/{file}")
    
    os.chdir(HOMEDIR)
    os.chdir("Businesses")
    
    for file in os.listdir():
        properties.append(f"Businesses/{file}")
    
    os.chdir(HOMEDIR)
    
    os.chdir("Players")
    
    players = [d for d in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), d))]

    for player in players:
        os.chdir(player)
        with open("Inventory.json") as invFile:
            data = json.load(invFile)
            Items = data.get("Items")
            
        for item in Items:
            item = json.loads(item)
                        
            if item.get("ID") == drug: # If item matches drug
                if item.get("PackagingID") == '': # Raw
                    drugAmtRaw += item.get("Quantity")
                elif item.get("PackagingID") == 'baggie': # Bag
                    drugAmtBag += item.get("Quantity")
                elif item.get("PackagingID") == 'jar': # Jar
                    drugAmtJar += item.get("Quantity")
                elif item.get("PackagingID") == 'brick': # Brick
                    drugAmtBrick += item.get("Quantity")

    os.chdir(HOMEDIR)
    
    for p in properties:
        with open(p, "r") as propertyFile:
            propertyData = json.load(propertyFile)
            
            objects = propertyData.get("Objects")

            for o in objects:
                
                Contents = None
                BaseData = json.loads(o.get('BaseData').replace('\n', '').replace(' ', ''))
                ItemString = json.loads(BaseData["ItemString"])
                
                
                if ItemString.get("ID") in ["smallstoragerack", "mediumstoragerack", "largestoragerack"]:
                    Contents = BaseData["Contents"]
                    
                    Items = Contents.get("Items")
                    
                    for item in Items:
                        item = json.loads(item)
                        
                        if item.get("ID") == drug: # If item matches drug
                            if item.get("PackagingID") == '': # Raw
                                drugAmtRaw += item.get("Quantity")
                            elif item.get("PackagingID") == 'baggie': # Bag
                                drugAmtBag += item.get("Quantity")
                            elif item.get("PackagingID") == 'jar': # Jar
                                drugAmtJar += item.get("Quantity")
                            elif item.get("PackagingID") == 'brick': # Brick
                                drugAmtBrick += item.get("Quantity")

    propertyFile.close()
    os.chdir(HOMEDIR)            
    
    totalAmt = drugAmtRaw + drugAmtBag + (drugAmtJar * 5) + (drugAmtBrick * 20)
    return totalAmt
    
# ~~~~ Program ~~~~ #
longestLengthP = 0
longestLengthR = 0


os.chdir(SAVEPATH) # Change Dir To Save Path
userIds = os.listdir() # Get User Ids

for uid in userIds:
    name = decodeSteamUserId(uid)
    usernames.update({name: uid})
    
selectedUser = q.select("Select User:", choices=usernames.keys(), qmark="~").ask()

selectedUserId = usernames[selectedUser]

os.chdir(selectedUserId)
saves = [d for d in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), d))]

for save in saves:
    saveName = decodeSaveName(save)
    saveFiles.update({saveName: save})

selectedSave = q.select("Select Save File:", choices=saveFiles.keys(), qmark="~").ask()

selectedSaveId = saveFiles[selectedSave]

os.chdir(selectedSaveId)

while True:
    rd = readRank(ranks)
    currentRank = rd[0]
    xp = rd[1]
    
    saveData = readSaveFile() # Read Save File
    
    productsW = [
        ("OG Kush", "Weed", ["calming"], "", findDrugAmt('ogkush')),
        ("Sour Diesel", "Weed", ["refreshing"], "", findDrugAmt('sourdiesel')),
        ("Green Crack", "Weed", ["energizing"], "", findDrugAmt('greencrack')),
        ("Granddaddy Purple", "Weed", ["sedating"], "", findDrugAmt('granddaddypurple')),
        ]
        
    productsM = [
        ("Meth", "Meth", [], "", findDrugAmt('meth')),
        ]
        
    productsC = [
        ("Cocaine", "Cocaine", [], "", findDrugAmt('cocaine')),
        ]

    for product in saveData["weedData"]:
        pName = product["Name"]
        pID = product["ID"]
        pDrugType = "Weed Mix"
        pProperties = product["Properties"]
        pRecipe = findRecipe(saveData, pID, pName)
        
        longestLengthP = max(longestLengthP, len(str(pProperties)))
        longestLengthR = max(longestLengthR, len(pRecipe))
        
        productsW.append((pName, pDrugType, pProperties, pRecipe, findDrugAmt(pID)))

    for product in saveData["methData"]:
        pName = product["Name"]
        pID = product["ID"]
        pDrugType = "Meth Mix"
        pProperties = product["Properties"]
        pRecipe = findRecipe(saveData, pID, pName)
        
        longestLengthP = max(longestLengthP, len(str(pProperties)))
        longestLengthR = max(longestLengthR, len(pRecipe))
        
        productsM.append((pName, pDrugType, pProperties, pRecipe, findDrugAmt(pID)))
        
    for product in saveData["cocaineData"]:
        pName = product["Name"]
        pID = product["ID"]
        pDrugType = "Cocaine Mix"
        pProperties = product["Properties"]
        pRecipe = findRecipe(saveData, pID, pName)
        
        longestLengthP = max(longestLengthP, len(str(pProperties)))
        longestLengthR = max(longestLengthR, len(pRecipe))
        
        productsC.append((pName, pDrugType, pProperties, pRecipe, findDrugAmt(pID)))

    TABLEFORMAT = f"║ {{:<32}} ║ {{:^12}} ║ {{:<{longestLengthP}}} ║ {{:<{longestLengthR}}} ║ {{:^4}} ║"  
    
    os.system("cls")

    print("╔"+ "═" * 34 + "╗")

    print("║ {:<32} ║".format(f"User: {selectedUser}"))
    print("║ {:<32} ║".format(f"Organisation: {selectedSave}"))
    print("║ {:<32} ║".format(f"Rank: {currentRank}"))
    print("║ {:<32} ║".format(f"XP: {xp}"))

    print("╠"+ "═" * 34 + "╬" + "═" * 14 + "╦" + "═" * (longestLengthP + 2) + "╦" + "═" * (longestLengthR + 2) + "╦" + "═" * 6 + "╗")

    print(TABLEFORMAT.format("Product Name", "Product Type", "Properties", "Recipe", "Amt"))

    print("╠"+ "═" * 34 + "╬" + "═" * 14 + "╬" + "═" * (longestLengthP + 2) + "╬" + "═" * (longestLengthR + 2) + "╬" + "═" * 6 + "╣")

    for entry in productsW:
        for i, p in enumerate(entry[2]):
            if p in effects.keys():
                entry[2][i] = effects.get(p)
        
        properties = ", ".join(entry[2])
        
        print(TABLEFORMAT.format(entry[0], entry[1], properties, entry[3], entry[4]))
        
    print("╠"+ "═" * 34 + "╬" + "═" * 14 + "╬" + "═" * (longestLengthP + 2) + "╬" + "═" * (longestLengthR + 2) + "╬" + "═" * 6 + "╣")

    for entry in productsM:
        for i, p in enumerate(entry[2]):
            if p in effects.keys():
                entry[2][i] = effects.get(p)
        properties = ", ".join(entry[2])
        
        print(TABLEFORMAT.format(entry[0], entry[1], properties, entry[3], entry[4]))

    print("╠"+ "═" * 34 + "╬" + "═" * 14 + "╬" + "═" * (longestLengthP + 2) + "╬" + "═" * (longestLengthR + 2) + "╬" + "═" * 6 + "╣")

    for entry in productsC:
        for i, p in enumerate(entry[2]):
            if p in effects.keys():
                entry[2][i] = effects.get(p)
        properties = ", ".join(entry[2])
        
        print(TABLEFORMAT.format(entry[0], entry[1], properties, entry[3], entry[4]))
    print("╚" + "═" * 34 + "╩" + "═" * 14 + "╩" + "═" * (longestLengthP + 2) + "╩" + "═" * (longestLengthR + 2) + "╩" + "═" * 6 + "╝")
    
    
    input("\n\nPress Return To Refresh...")