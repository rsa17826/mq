const fs = require('fs');
const path = require('path');

// Your dictionary mapping full location strings to IDs
const AP_LOCATION_IDS = {
  "20_20 - skill:dig": 1,
  "20_20 - skill:kick": 2,
  "20_20 - skill:flee": 3,
  "20_20 - skill:swap": 4,
  "20_20 - misc:magic only resist bypass": 5,
  "20_20 - skill:firewall": 6,
  "20_20 - skill:firewall.1": 7,
  "20_20 - skill:halo": 8,
  "20_20 - item:aurastones": 9,
  "20_20 - item:gold": 10,
  "20_20 - item:shadowCrest": 11,
  "20_20 - item:blue crystal": 12,
  "20_20 - item:key": 13,
  "20_20 - item:emeralds": 14,
  "20_20 - misc:fire crystal": 15,
  "20_20 - item:ring of evasion": 16,
  "20_20 - item:slamstones": 17,
  "15_21 - food:banana": 18,
  "21_20 - food:orange": 19,
  "13_16 - weapon:sKnife": 20,
  "15_16 - magic:ice": 21,
  "11_13 - food:blueberries": 22,
  "11_12 - food:sunflowerSeeds": 23,
  "12_12 - misc:headstoneSwitch2": 24,
  "12_9 - food:cherry": 25,
  "12_9 - weapon:sKnife": 26,
  "12_9 - weapon:warlockStaff": 27,
  "12_9 - weapon:sunSword": 28,
  "12_9 - food:orange": 29,
  "11_9 - magic:weak": 30,
  "11_9 - item:gold": 31,
  "8_14 - skill:tough.+1": 32,
  "9_16 - item:gold": 33,
  "4_17 - weapon:axe.+1": 34,
  "8_17 - misc:green secret code": 35,
  "11_17 - item:bombs": 36,
  "11_17 - item:gold": 37,
  "7_18 - skill:reveal.+1": 38,
  "9_22 - food:chocolate": 39,
  "9_22 - food:steak": 40,
  "9_22 - food:peppers": 41,
  "10_25 - misc:headstoneSwitch3": 42,
  "12_25 - food:gummyBears": 43,
  "12_25 - item:diamonds": 44,
  "13_26 - food:gingerBread": 45,
  "18_24 - misc:headstoneSwitch4": 46,
  "21_23 - item:diamonds": 47,
  "20_22 - item:rubies": 48,
  "19_22 - skill:reveal": 49,
  "19_21 - item:gold": 50,
  "21_20 - item:gold": 51,
  "21_18 - item:diamonds": 52,
  "21_18 - food:peppers": 53,
  "21_17 - item:rubies": 54,
  "20_15 - skill:firewall.2": 55,
  "20_15 - skill:firewall.3": 56,
  "20_15 - skill:firewall.4": 57,
  "20_15 - skill:firewall.5": 58,
  "20_15 - skill:firewall.6": 59,
  "20_15 - skill:firewall.7": 60,
  "20_15 - skill:firewall.8": 61,
  "20_15 - skill:firewall.9": 62,
  "20_15 - skill:firewall.10": 63,
  "19_15 - item:rubies": 64,
  "19_15 - skill:hint": 65,
  "19_15 - skill:fear": 66,
  "16_16 - misc:headstoneSwitch1": 67,
  "18_13 - misc:bombCapacity": 68,
  "24_11 - weapon:baneBlade": 69,
  "17_10 - food:gummyBears": 70,
  "4_13 - food:orange": 71,
  "4_13 - food:gingerBread": 72,
  "4_13 - food:strawberry": 73,
  "21_20 - magic:crush": 74,
  "19_20 - item:gold": 75,
  "19_20 - food:gingerBread": 76,
  "21_21 - skill:craft": 77,
  "15_18 - food:beefJerky": 78,
  "13_21 - item:bombs": 79,
  "13_21 - permit:bomb": 80,
  "19_20 - food:chocolate": 81,
  "10_19 - misc:orb of peace": 82,
  "12_9 - misc:fire crystal": 83,
  "15_18 - permit:shadowsoul entrance": 84,
  "5_24 - food:holyWater": 85,
  "14_18 - misc:pup": 86,
  "14_18 - item:gold": 87,
  "12_11 - item:diamonds": 88,
  "14_22 - item:ring of gold": 89,
  "16_21 - item:ring of health": 90,
  "13_16 - item:ring of evasion": 91,
  "11_9 - skill:warp": 92,
  "13_21 - permit:volcano": 93,
  "13_21 - permit:bomb.2": 94,
  "9_22 - food:orange": 95,
  "11_11 - item:ring of poison": 96,
  "19_20 - food:peppers": 97,
  "19_20 - food:orange": 98,
  "15_16 - item:ring of magic": 99,
  "6_12 - skill:convert": 100,
  "19_16 - item:medallions": 101,
  "18_20 - item:gold": 102,
  "18_19 - item:gold": 103,
  "17_20 - item:gold": 104,
  "17_20 - food:beefJerky": 105,
  "15_19 - item:gold": 106,
  "15_19 - item:bombs": 107,
  "15_19 - food:banana": 108,
  "14_19 - armor:regenArmor": 109,
  "11_19 - food:sunflowerSeeds": 110,
  "11_19 - food:strawberry": 111,
  "8_18 - item:bombs": 112,
  "8_18 - food:steak": 113,
  "11_18 - magic:refresh": 114,
  "15_18 - food:chocolate": 115,
  "15_18 - item:bombs": 116,
  "19_18 - item:rubies": 117,
  "18_17 - item:gold": 118,
  "13_16 - magic:weak": 119,
  "17_16 - item:diamonds": 120,
  "18_15 - food:newtonsApple": 121,
  "17_15 - item:gold": 122,
  "17_15 - food:gingerBread": 123,
  "16_15 - armor:diamondArmor": 124,
  "14_15 - food:orange": 125,
  "14_15 - item:bombs": 126,
  "9_15 - armor:phantomCoat": 127,
  "15_14 - food:carrot": 128,
  "23_10 - armor:alphaArmor": 129,
  "23_10 - item:diamonds": 130,
  "23_10 - food:newtonsApple": 131,
  "21_11 - food:gummyBears": 132,
  "24_14 - armor:grimGear": 133,
  "10_13 - misc:ninja": 134,
  "10_13 - item:gold": 135,
  "10_13 - item:diamonds": 136,
  "10_13 - item:aurastones": 137,
  "10_13 - item:slamstones": 138,
  "10_13 - food:elixir": 139,
  "10_13 - food:holyWater": 140,
  "9_13 - item:bombs": 141,
  "19_20 - food:holyWater": 142,
  "6_13 - food:grape": 143,
  "6_13 - food:strawberry": 144,
  "6_12 - item:geode": 145,
  "12_12 - magic:blessing": 146,
  "8_10 - item:gold": 147,
  "8_10 - food:beefJerky": 148,
  "9_10 - item:gold": 149,
  "10_9 - food:steak": 150,
  "6_10 - food:chocolate": 151,
  "18_21 - item:gingerBread": 152,
  "15_21 - item:gold": 153,
  "15_21 - item:bombs": 154,
  "14_21 - item:gold": 155,
  "14_21 - item:bombs": 156,
  "14_21 - food:apple": 157,
  "12_21 - item:diamonds": 158,
  "12_21 - food:banana": 159,
  "11_21 - item:bombs": 160,
  "9_22 - magic:doubleDown": 161,
  "16_22 - item:gold": 162,
  "17_22 - item:diamonds": 163,
  "21_23 - item:gold": 164,
  "19_23 - magic:fire": 165,
  "18_23 - weapon:warlockStaff": 166,
  "9_23 - magic:drain": 167,
  "4_24 - food:cherry": 168,
  "15_24 - item:gold": 169,
  "16_24 - item:gold": 170,
  "16_24 - food:gummyBears": 171,
  "16_25 - item:diamonds": 172,
  "16_25 - food:steak": 173,
  "11_25 - food:beefJerky": 174,
  "3_26 - food:elixir": 175,
  "4_26 - weapon:shadowStaff": 176,
  "9_26 - food:blueberries": 177,
  "19_20 - misc:blue crystal": 178,
  "19_15 - weapon:bombSword": 179,
  "19_15 - weapon:refreshStaff": 180,
  "19_15 - weapon:axe": 181,
  "19_15 - weapon:soulSword": 182,
  "19_15 - armor:shadowCoat": 183,
  "19_15 - armor:soulArmor": 184,
  "19_15 - skill:shield": 185,
  "20_20 - food:apple": 186,
  "20_20 - food:honey": 187,
  "20_20 - food:grapes": 188,
  "12_9 - food:carrot": 189,
  "12_9 - food:beefJerky": 190,
  "12_9 - food:cherries": 191,
  "21_20 - magic:slow": 192,
  "21_20 - magic:heal": 193,
  "21_20 - magic:blast": 194,
  "13_17 - magic:regen": 195,
  "13_17 - magic:cloud": 196,
  "13_17 - magic:weak": 197,
  "11_9 - magic:refresh": 198,
  "11_9 - magic:lightning": 199,
  "20_20 - weapon:club": 200,
  "20_20 - weapon:sword": 201,
  "13_17 - weapon:royalSword": 202,
  "13_17 - weapon:royalStaff": 203,
  "20_20 - armor:vest": 204,
  "20_20 - armor:robe": 205,
  "20_20 - armor:iron": 206,
  "13_17 - armor:royalArmor": 207,
  "13_17 - armor:mysticCloak": 208,
  "12_9 - armor:sunArmor": 209,
  "12_9 - armor:speedVest": 210,
  "19_20 - skill:dig": 211,
  "19_20 - skill:kick": 212,
  "20_20 - weapon:dagger": 213,
  "500_501 - weapon:aSword": 214,
  "200_200 - weapon:twinFury": 215,
  "18_25 - skill:medic.1": 216,
  "18_25 - skill:medic.2": 217,
  "18_25 - skill:medic.3": 218,
  "18_25 - skill:medic.4": 219,
  "18_25 - skill:medic.5": 220,
  "18_25 - skill:medic.6": 221,
  "6_13 - food:grapes": 222,
  "4_24 - food:cherries": 223,
  "18_21 - food:gingerBread": 224,
  "9_25 - item:gold": 225,
  "9_25 - food:elixir": 226,
  "19_20 - food:steak": 227,
  "4_26 - skill:tough": 228,
  "14_18 - weapon:creeperCrusher": 229,
  "14_18 - item:pup": 230,
  "13_17 - armor:nobleArmor": 231,
  "20_20 - misc:str up npc": 232
};

const filePath = path.join(__dirname, 'MathQuest', 'MathQuest.base.js');

try {
  // 1. Read the target file content
  let fileContent = fs.readFileSync(filePath, 'utf8');
  let totalReplacements = 0;

  // 2. Loop through each key in your object
  for (const fullKey of Object.keys(AP_LOCATION_IDS)) {
    // Extract the shorthand part (e.g., "skill:dig" from "20_20 - skill:dig")
    // This splits by the " - " divider
    const parts = fullKey.split(' - ');
    if (parts.length < 2) continue;

    const shortKey = parts[1];

    // Create a dynamic regex to find exactly `newItem("shortKey")`
    // Escapes special characters if any exist in your keys
    const searchStr = `newItem("${shortKey}")`;

    // Count how many times this exact newItem string appears in the file
    const occurrences = fileContent.split(searchStr).length - 1;

    // 3. If it occurs exactly once, replace ALL instances of the shortKey globaly
    if (occurrences === 0) {
    }
    else if (occurrences === 1) {
      // Use a global regular expression to replace every plain "skill:dig" with "20_20 - skill:dig"
      fileContent = fileContent.replaceAll(`newItem("${shortKey}")`, `newItem("${fullKey}")`);
      fileContent = fileContent.replaceAll('"'+shortKey+'": ()', '"'+fullKey+'": ()');

      console.log(`✅ Replaced all instances of "${shortKey}" with "${fullKey}" (newItem matched exactly once).`);
      totalReplacements++;
    } else {
      console.log(`⚠️ Skipped "${shortKey}": Found ${occurrences} matches for ${searchStr} (Expected exactly 1).`);
    }
  }

  // 4. Save the updated content back to the file if changes were made
  if (totalReplacements > 0) {
    fs.writeFileSync(filePath, fileContent, 'utf8');
    console.log(`\n🎉 Done! Successfully updated ${totalReplacements} keys.`);
  } else {
    console.log('\n❌ No changes made to the file.');
  }

} catch (error) {
  console.error('An error occurred:', error.message);
}