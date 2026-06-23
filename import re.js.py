import re

def convert_line(line):
    ol = line
    if '==' in line:
      return ol
    line = line.strip()
    if not line:
        return ""

    # 1. Match array assignments: manager.armor[9] = 0 -> setManagerData("armor", 9, 0)
    # Also handles variables inside brackets like manager.armor[this.counter] = 0
    array_match = re.match(r'^manager\.(\w+)\[([^\]]+)\]\s*=\s*(.+)$', line)
    if array_match:
        if f"{array_match[1]}[{array_match[2]}]" in input_text:
          prop, index, value = array_match.groups()
          # Clean up quotes if the index is a literal string, or leave as is if it's a number/variable
          return f'setManagerData("{prop}", {index}, {value})'

    # 2. Match standard assignments: manager.bombCapacity = 0 -> setManagerData("bombCapacity", 0)
    # (Note: Standard variables don't have an index, so we pass None or skip that argument depending on your API)
    direct_match = re.match(r'^manager\.(\w+)\s*=\s*(.+)$', line)
    if direct_match:
      if direct_match[1] in input_text:
        prop, value = direct_match.groups()
        return f'setManagerData("{prop}", {value})'

    # 3. Match increments: manager.aurastones++ or manager.correct++ -> setManagerData("correct", manager.correct + 1)
    inc_match = re.match(r'^manager\.(\w+)\+\+$', line)
    if inc_match:
      if inc_match[1] in input_text:
        prop = inc_match.group(1)
        return f'setManagerData("{prop}", manager.{prop} + 1)'

    # 4. Match decrements: manager.aurastones-- -> setManagerData("aurastones", manager.aurastones - 1)
    dec_match = re.match(r'^manager\.(\w+)--$', line)
    if dec_match:
      if dec_match[1] in input_text:
        prop = dec_match.group(1)
        return f'setManagerData("{prop}", manager.{prop} - 1)'

    # Return the line untouched if it doesn't match any pattern
    return ol

# --- Execution ---
input_text = re.split(r"[^\w]","""
manager.armor[0] = 1
manager.armor[0] = 2
manager.armor[1] = 1
manager.armor[1] = 2
manager.armor[10] = 1
manager.armor[10] = 2
manager.armor[11] = 1
manager.armor[11] = 2
manager.armor[12] = 1
manager.armor[12] = 2
manager.armor[13] = 1
manager.armor[13] = 2
manager.armor[14] = 1
manager.armor[14] = 2
manager.armor[2] = 1
manager.armor[2] = 2
manager.armor[3] = 1
manager.armor[3] = 2
manager.armor[4] = 0
manager.armor[4] = 1
manager.armor[4] = 2
manager.armor[5] = 1
manager.armor[5] = 2
manager.armor[6] = 0
manager.armor[6] = 1
manager.armor[6] = 2
manager.armor[7] = 1
manager.armor[7] = 2
manager.armor[8] = 1
manager.armor[8] = 2
manager.armor[9] = 0
manager.armor[9] = 1
manager.armor[9] = 2
manager.armor[this.armorCounter] = 1
manager.armor[this.counter] = 0
manager.aurastones = 0
manager.aurastones--
manager.aurastones++
manager.bombCapacity = 0
manager.bombCapacity = 99
manager.bombs = 0
manager.bombs = 15
manager.bombs = 99
manager.bombs--
manager.bombs++
manager.correct = 0
manager.correct++
manager.crafts[0] = 1
manager.crafts[1] = 1
manager.crafts[10] = 1
manager.crafts[10]++
manager.crafts[11] = 1
manager.crafts[11]++
manager.crafts[12] = 1
manager.crafts[12]++
manager.crafts[13] = 1
manager.crafts[13]++
manager.crafts[2] = 1
manager.crafts[3] = 1
manager.crafts[4] = 1
manager.crafts[5] = 1
manager.crafts[6] = 1
manager.crafts[7] = 1
manager.crafts[8] = 1
manager.crafts[9] = 1
manager.crafts[this.counter] = 0
manager.decimalSplitVar = 0
manager.diamonds = 0
manager.diamonds--
manager.diamonds++
manager.eHealth = 0
manager.eHealth--
manager.eMagic = 0
manager.eMagic--
manager.emeralds = 0
manager.emeralds--
manager.emeralds++
manager.eSpeed = 0
manager.eSpeed--
manager.eSpeed++
manager.eStr = 0
manager.eStr++
manager.fireWall = 0
manager.fireWall = 30
manager.fireWall--
manager.food[0]--
manager.food[0]++
manager.food[1]--
manager.food[1]++
manager.food[10] = 99
manager.food[10]--
manager.food[10]++
manager.food[11] = 99
manager.food[11]--
manager.food[11]++
manager.food[12] = 99
manager.food[12]--
manager.food[12]++
manager.food[13]--
manager.food[13]++
manager.food[14] = 99
manager.food[14]--
manager.food[14]++
manager.food[15]--
manager.food[15]++
manager.food[16]--
manager.food[16]++
manager.food[17] = 99
manager.food[17]--
manager.food[17]++
manager.food[18] = 99
manager.food[18]--
manager.food[18]++
manager.food[2]--
manager.food[2]++
manager.food[3]--
manager.food[3]++
manager.food[4] = 99
manager.food[4]--
manager.food[4]++
manager.food[5] = 1
manager.food[5] = 99
manager.food[5]--
manager.food[5]++
manager.food[6]--
manager.food[6]++
manager.food[7] = 99
manager.food[7]--
manager.food[7]++
manager.food[8] = 99
manager.food[8]--
manager.food[8]++
manager.food[9] = 99
manager.food[9]--
manager.food[9]++
manager.food[this.counter] = 0
manager.food[this.counter] = 5
manager.food[this.innerCounter] = 99
manager.geodes = 0
manager.geodes++
manager.gold = 0
manager.gold--
manager.gold++
manager.hugeBomb = 0
manager.hugeBomb = 1
manager.iceSageVar = 0
manager.keys = 0
manager.keys--
manager.keys++
manager.loot[Enum.Loot.aAxe]--
manager.loot[Enum.Loot.aAxe]++
manager.loot[Enum.Loot.aClub]++
manager.loot[Enum.Loot.aScepter]--
manager.loot[Enum.Loot.aScepter]++
manager.loot[Enum.Loot.bClaw]++
manager.loot[Enum.Loot.bFang]++
manager.loot[Enum.Loot.bTusk]++
manager.loot[Enum.Loot.cFang]++
manager.loot[Enum.Loot.cShell]++
manager.loot[Enum.Loot.cThread]++
manager.loot[Enum.Loot.dScale]++
manager.loot[Enum.Loot.fBone]++
manager.loot[Enum.Loot.gFeather]++
manager.loot[Enum.Loot.gSkin]++
manager.loot[Enum.Loot.kCrest]++
manager.loot[Enum.Loot.mHat]--
manager.loot[Enum.Loot.mHat]++
manager.loot[Enum.Loot.mHorn]--
manager.loot[Enum.Loot.mHorn]++
manager.loot[Enum.Loot.mStaff]--
manager.loot[Enum.Loot.mStaff]++
manager.loot[Enum.Loot.oArm]++
manager.loot[Enum.Loot.oCoin]++
manager.loot[Enum.Loot.sClaw]++
manager.loot[Enum.Loot.sFrag]++
manager.loot[Enum.Loot.sTooth]++
manager.loot[Enum.Loot.tBand]--
manager.loot[Enum.Loot.tBand]++
manager.loot[Enum.Loot.vAsh]++
manager.loot[Enum.Loot.venom]--
manager.loot[Enum.Loot.vHorn]++
manager.loot[Enum.Loot.wPelt]++
manager.magic[1] = 1
manager.magic[10] = 1
manager.magic[11] = 1
manager.magic[12] = 1
manager.magic[13] = 1
manager.magic[14] = 1
manager.magic[2] = 1
manager.magic[3] = 1
manager.magic[4] = 1
manager.magic[5] = 1
manager.magic[6] = 1
manager.magic[7] = 1
manager.magic[8] = 1
manager.magic[9] = 1
manager.magic[this.counter] = 0
manager.magic[this.counter] = 1
manager.magic[this.upgradeSpell]++
manager.medallions = 0
manager.medallions++
manager.ornaments = 0
manager.ornaments++
manager.pup = 0
manager.pup--
manager.pup++
manager.ring1 = 0
manager.ring1 = 1
manager.ring1++
manager.ring2 = 0
manager.ring2 = 1
manager.ring3 = 0
manager.ring3 = 1
manager.ring4 = 0
manager.ring4 = 1
manager.ring5 = 0
manager.ring5 = 1
manager.ring6 = 0
manager.ring6 = 1
manager.ring7 = 0
manager.ring7 = 1
manager.rubies = 0
manager.rubies--
manager.rubies++
manager.shadowCrest = 0
manager.shadowCrest++
manager.skillPoints = 0
manager.skillPoints--
manager.skillPoints++
manager.skills[0] = 1
manager.skills[1] = 1
manager.skills[10] = 1
manager.skills[11] = 1
manager.skills[12] = 1
manager.skills[12] = 2
manager.skills[12] = 3
manager.skills[12] = 4
manager.skills[12] = 5
manager.skills[13] = 1
manager.skills[14] = 1
manager.skills[14] = 2
manager.skills[14] = 3
manager.skills[14] = 4
manager.skills[14] = 5
manager.skills[14] = 6
manager.skills[15] = 1
manager.skills[15] = 2
manager.skills[15] = 3
manager.skills[15] = 4
manager.skills[15] = 5
manager.skills[2] = 1
manager.skills[3] = 1
manager.skills[4] = 1
manager.skills[5] = 1
manager.skills[6] = 1
manager.skills[7] = 1
manager.skills[8] = 1
manager.skills[9] = 1
manager.skills[this.counter] = 0
manager.slamstones = 0
manager.slamstones--
manager.slamstones++
manager.speed = 1
manager.staffVar = 0
manager.str = 1
manager.str++
manager.weapon[0] = 0
manager.weapon[0] = 1
manager.weapon[0] = 2
manager.weapon[1] = 1
manager.weapon[1] = 2
manager.weapon[10] = 0
manager.weapon[10] = 1
manager.weapon[10] = 2
manager.weapon[11] = 1
manager.weapon[11] = 2
manager.weapon[12] = 1
manager.weapon[12] = 2
manager.weapon[13] = 0
manager.weapon[13] = 1
manager.weapon[13] = 2
manager.weapon[14] = 1
manager.weapon[14] = 2
manager.weapon[15] = 0
manager.weapon[15] = 1
manager.weapon[15] = 2
manager.weapon[16] = 1
manager.weapon[16] = 2
manager.weapon[17] = 1
manager.weapon[17] = 2
manager.weapon[18] = 1
manager.weapon[18] = 2
manager.weapon[19] = 1
manager.weapon[19] = 2
manager.weapon[2] = 0
manager.weapon[2] = 1
manager.weapon[2] = 2
manager.weapon[3] = 0
manager.weapon[3] = 1
manager.weapon[3] = 2
manager.weapon[4] = 0
manager.weapon[4] = 1
manager.weapon[4] = 2
manager.weapon[5] = 1
manager.weapon[5] = 2
manager.weapon[6] = 0
manager.weapon[6] = 1
manager.weapon[6] = 2
manager.weapon[7] = 0
manager.weapon[7] = 1
manager.weapon[7] = 2
manager.weapon[8] = 0
manager.weapon[8] = 1
manager.weapon[8] = 2
manager.weapon[9] = 1
manager.weapon[9] = 2
manager.weapon[this.counter] = 0
manager.weapon[this.weapCounter] = 1
manager.wrong = 0
manager.wrong++

""")

print("--- Converted Output ---")
lines=''
with open("./MathQuest/MathQuest.base.js", "r") as f:
  text = f.read()
  for line in text.strip().split('\n'):
      lines+=(convert_line(line))
      lines+='\n'
with open("./MathQuest/MathQuest.base.js", "w") as f:
  f.write(lines)