
with open("./MathQuest/MathQuest.js", "r") as f:
  text=f.read()

Enum = {
  "Loot": {
    "aAxe": 19,
    "aClub": 18,
    "aScepter": 20,
    "bClaw": 2,
    "bFang": 4,
    "bTooth": 1,
    "bTusk": 0,
    "cFang": 11,
    "cShell": 6,
    "cThread": 24,
    "dScale": 15,
    "fBone": 9,
    "gFeather": 12,
    "gSkin": 16,
    "kCrest": 14,
    "mHat": 21,
    "mHorn": 17,
    "mStaff": 7,
    "oArm": 26,
    "oCoin": 13,
    "sClaw": 10,
    "sFrag": 22,
    "sTooth": 25,
    "tBand": 5,
    "vAsh": 23,
    "venom": 3,
    "vHorn": 27,
    "wPelt": 8,
  },
  "Quest": {
    "access": 12,
    "aSword": 17,
    "bBomb": 1,
    "canteen": 7,
    "curse": 9,
    "dig": 3,
    "dream": 10,
    "geo": 8,
    "gTree": 0,
    "hWater": 14,
    "isles": 16,
    "mChal": 4,
    "oMan": 15,
    "pam": 6,
    "rings": 13,
    "seeds": 5,
    "warp": 2,
  },
  "Food": {
    "apple": 0,
    "honey": 1,
    "grapes": 2,
    "orange": 3,
    "gingerBread": 4,
    "banana": 5,
    "carrot": 6,
    "beefJerky": 7,
    "cherries": 8,
    "chocolate": 9,
    "steak": 10,
    "holyWater": 11,
    "peppers": 12,
    "sunflowerSeeds": 13,
    "gummyBears": 14,
    "blueberries": 15,
    "newtonsApple": 16,
    "elixir": 17,
    "strawberry": 18,
  },
  "Skill": {
    "dig": 0,
    "kick": 1,
    "flee": 2,
    "swap": 3,
    "firewall": 4,
    "warp": 5,
    "halo": 6,
    "convert": 7,
    "hint": 8,
    "fear": 9,
    "shield": 10,
    "craft": 11,
    "reveal": 12,
    "snowball": 13,
    "medic": 14,
    "tough": 15,
  },
  "Magic": {
    "tele": 0,
    "slow": 1,
    "heal": 2,
    "blast": 3,
    "fire": 4,
    "regen": 5,
    "cloud": 6,
    "weak": 7,
    "ice": 8,
    "refresh": 9,
    "lightning": 10,
    "drain": 11,
    "blessing": 12,
    "doubleDown": 13,
    "crush": 14,
  },
  "Craft": {
    "chocolate": 0,
    "orange": 1,
    "steak": 2,
    "blueberries": 3,
    "craftBomb": 4,
    "craftKey": 5,
    "craftRingGold": 6,
    "holyWater": 7,
    "newtonApple": 8,
    "elixir": 9,
    "emerald": 10,
    "upgradeAAHP": 11,
    "upgradeAAMP": 12,
    "upgradeStaff": 13,
  },
  "Weapon": {
    "club": 0,
    "dagger": 1,
    "sword": 2,
    "royalSword": 3,
    "royalStaff": 4,
    "sKnife": 5,
    "warlockStaff": 6,
    "sunSword": 7,
    "orcBlade": 8,
    "shadowStaff": 9,
    "baneBlade": 10,
    "creeperCrusher": 11,
    "pitchfork": 12,
    "bombSword": 13,
    "refreshStaff": 14,
    "axe": 15,
    "soulSword": 16,
    "twinFury": 17,
    "upgradeStaff": 18,
    "aSword": 19,
  },
  "Armor": {
    "vest": 0,
    "robe": 1,
    "iron": 2,
    "regenArmor": 3,
    "royalArmor": 4,
    "mysticCloak": 5,
    "sunArmor": 6,
    "speedVest": 7,
    "grimGear": 8,
    "phantomCoat": 9,
    "diamondArmor": 10,
    "nobleArmor": 11,
    "shadowCoat": 12,
    "soulArmor": 13,
    "alphaArmor": 14,
  },
}
import re
for k in Enum:
  for kk in Enum[k]:
      v=Enum[k][kk]
      print(k)
      if k=="Weapon":
        old_str = f".weapTile[{v}]"
        new_str = f".weapTile[Enum.{k}.{kk}]"
        text = text.replace(old_str, new_str)
      old_str = f".{k.lower()}[{v}]"
      new_str = f".{k.lower()}[Enum.{k}.{kk}]"
      text = text.replace(old_str, new_str)
      old_str = f".{k.lower()}s[{v}]"
      new_str = f".{k.lower()}s[Enum.{k}.{kk}]"
      text = text.replace(old_str, new_str)
      old_str = f".{k.lower()}Tile[{v}]"
      new_str = f".{k.lower()}Tile[Enum.{k}.{kk}]"
      text = text.replace(old_str, new_str)
      old_str = f".{k.lower()}sTile[{v}]"
      new_str = f".{k.lower()}sTile[Enum.{k}.{kk}]"
      text = text.replace(old_str, new_str)
      old_str = f".{k.lower()}[.{kk}]"
      new_str = f".{k.lower()}[Enum.{k}.{kk}]"
      text = text.replace(old_str, new_str)
with open("./MathQuest/MathQuest.js", "w") as f:
  f.write(text)