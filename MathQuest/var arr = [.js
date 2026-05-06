var arr = [
  (a) => {
    a.mess.set_text(
      "Serlon: You can learn to craft new items\nfrom a girl named Kate in the town of Dyce."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Watch your step!\nInvisible treasure chest nearby."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Caution: Arithma Tics bite!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Creepers' Cavern: Lower Level"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Only by draining the water will\nthe way be revealed."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "East: Island of Abundance\nSouth: Island of Opulence\nSouthwest: Island of Aridack"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Gator Lagoon"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The last remaining Borloc Tree."), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("North: Viper's Nest - Beware!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "(Someone has etched something on the sign)\nIt reads: W10 S2"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Queen's Garden: Do not pick the flowers!"),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "If lost, remember:\nWEST, SOUTH, EAST, SOUTH\nand the way will be revealed..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "There's an engraving on the base of the\nstatue that reads:\nThe product of " +
        a.a2 +
        " and " +
        a.b2 +
        "."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Something very old is sketched on the stone:\nThe sum of " +
        a.a1 +
        " and " +
        a.b1 +
        "."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nThe difference between " + a.a3 + " and " + a.b3 + "."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nThe difference between " + a.a3 + " and " + a.b3 + "."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nOnly with two can one enter the Grotto of\nMages."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nNorth: Grimsbane\nSouth: Grimsyard Cemetery"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The sign reads:\nTake caution! Creepers' Nest ahead!"),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The sign reads:\nOpah are easily startled."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The sign reads:\nBeware of Cave Trolls!"),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "The walls have become fragile.\nIt would take very little for new\npaths to be revealed."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Only level 2 magic (or higher) can light the way."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Ignite both chalices with powerful\nmagic to open the way."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The sign reads:\nYou shall never leave here."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("You lay the fire crystal on the statue."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("You fill the canteen with water."), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("The sign reads:\nWest: Division Desert - Caution Hot!")
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nNorth: Castle Muldivadd\nWest: Multiple Mountains"
    )
  },
  (a) => {
    a.mess.set_text(
      "The sign reads:\nWest - Creepers' Cavern\nSouth - Prism Lake System"
    )
  },
  (a) => {
    a.mess.set_text("The sign reads:\nWelcome to Dyce")
  },
  (a) => {
    a.mess.set_text("The sign reads:\nForest of Fayth")
  },
  (a) => {
    a.mess.set_text("The sign reads:\nDo not enter!")
  },
  (a) => {
    a.mess.set_text(
      "To the south, you can find the\nIslands of Inequality.\nBut you should be warned:\nSharks are everywhere!!!"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("This water also restores magic."), (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "You're looking for a Shadoom? Are you insane?!\nThat's just not a very smart idea..."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "Here's what you need to do:\nEnter the trick room to the south and stand in\nfront of the hooded statue. Use the skill of\nREVEAL and then cast a\nlevel 3 LIGHTNING SPELL."
        ),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "Many adventurers become lost here in\nThe Necropolis of Illusion. Some rooms\nare not what they appear to be..."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Shayde Obi: The ways of the ninja are lost\nto time. However, I can teach them to you."
      ),
      2 == a.messPage &&
        a.mess.set_text(
          "Shayde Obi: Once you learn them, they will last\n30 minutes."
        ),
      3 == a.messPage &&
        a.mess.set_text(
          "Shayde Obi: You will earn 3x the amount of\nskill points during battle."
        ),
      4 == a.messPage &&
        a.mess.set_text(
          "Shayde Obi: Your walking speed will temporarily\nincrease by 5."
        ),
      5 == a.messPage &&
        a.mess.set_text(
          "Shayde Obi: And 10% of your attacks will deal\nan ending blow. Instantly defeating\nyour opponent... Well, except for the Battle\nArena and a few powerful enemies."
        ),
      6 == a.messPage &&
        (0 == a.ninjaSkills &&
          a.mess.set_text(
            "Shayde Obi: So, what do you say?\nWanna learn some ninja skills for 30 minutes?\n(500 gold)"
          ),
        1 == a.ninjaSkills &&
          a.mess.set_text(
            "Shayde Obi: Would you like to reset\nyour ninja timer to 30?\n(500 gold)"
          ),
        a.showYesNoOptions())
  },
  (a) => {
    a.mess.set_text("Shayde Obi: Go forth, mighty ninja!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "There are many treasures hidden throughout\nthis part of the Necropolois of Illusion.\nI have seen at least three."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "There's room west of here, far to the west.\nI keep hearing a child's voice in there...\nbut I do not see any children..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Shayde Taab Jr.: You did it! You defeated\nthe Shadoom! Please go tell my father\nI'm safe. I'm going to explore a little more,\nand then I'll return home."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Shayde Taab Jr.: I'm being chased!\nI believe by a Shadoom, they're very dangerous.\nI'm using this trick room to hide."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "Shayde Taab Jr.: Please help me!\nFind and defeat the Shadoom..."
        ),
        3 == a.quest[a.hWater] && (a.quest[a.hWater] = 4),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "The battle arena is only for brave players.\nWe've gathered the fiercest beasts and\nbest warriors."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Queen Esther: I keep hearing a voice, but\nI don't see anyone around...\nCreepy..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Shayde Taab: I'm so sad... My son left to\nexplore the Multiple Mountains 5 days ago\nand I haven't heard from him since. Please help\nme. If you find him, I'll teach you how to\ncraft holy water."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Shayde Taab: Learn how to craft, and\nthen come back to see me..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Shade Taab: Thank you for finding my son!\nTo craft holy water, you need to combine\n25 pinches of void ash with a Power-Up.\nOh, and you MUST be standing in water\nat the time."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Shayde Taab: My son is always\nwandering off..."),
      (a.messFin = true)
  },
  (a) => {
    1 == a.quest[a.hWater] || 2 == a.quest[a.hWater]
      ? (a.mess.set_text(
          "Shayde Ja: You're looking for Shayde Taab's son?\nI saw him a few days ago, heading northwest."
        ),
        (a.quest[a.hWater] = 2))
      : a.mess.set_text(
          "Shayde Ja: You can find some very rare\nitems in red treasure chests, but only\nif you defeat a rare attacker."
        ),
      (a.messFin = true)
  },
  (a) => {
    13 > a.quest[a.gTree]
      ? a.mess.set_text(
          "Do you hear that? It sounds like water,\nbut the sound seems like it's coming\nfrom under the ground..."
        )
      : a.mess.set_text(
          "I keep hearing something under the ground...\nI sure wish I had a bomb..."
        ),
      (a.messFin = true)
  },
  (a) => {
    0 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: I love flowers. Would you find\na blue flower for me?"
        ),
        a.showYesNoOptions())
      : 1 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: If you are able to find a blue flower\nplease bring it to me."
        ),
        (a.messFin = true))
      : 2 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found one!\nHere, you can have this.\n(She gives you 20 gold coins.)"
        ),
        a.fame++,
        (a.gold += 20),
        a.hitMax(),
        (a.quest[a.pam] = 3))
      : 4 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found another one!\nI made these just for you.\n(She gives you 10 gingerbread cookies.)"
        ),
        a.fame++,
        (a.food[4] += 10),
        a.hitMax(),
        (a.quest[a.pam] = 5))
      : 6 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found another one!\nYou'll love this.\n(She gives you 5 chocolate bars.)"
        ),
        a.fame++,
        (a.food[9] += 5),
        a.hitMax(),
        (a.quest[a.pam] = 7))
      : 8 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found another one!\nI cooked this for you.\n(She gives you 3 juicy steaks.)"
        ),
        a.fame++,
        (a.food[10] += 3),
        a.hitMax(),
        (a.quest[a.pam] = 9))
      : 10 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found another one!\nI saved these for you.\n(She gives you 5 peppers and 20 oranges.)"
        ),
        a.fame++,
        (a.food[12] += 5),
        (a.food[3] += 20),
        a.hitMax(),
        (a.quest[a.pam] = 11))
      : 12 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: You found a sixth one!\nThat makes a half dozen!\nYou deserve this.\n(She gives you a bottle of holy water.)"
        ),
        a.fame++,
        a.food[11]++,
        a.hitMax(),
        (a.quest[a.pam] = 13))
      : 13 == a.quest[a.pam]
      ? (a.mess.set_text(
          "Pam: I can't believe you found a dozen\nof these rare flowers. Let me tell you\na little secret...\n"
        ),
        (a.quest[a.pam] = 14))
      : (14 != a.quest[a.pam] && 15 != a.quest[a.pam]) ||
        (3 != a.messPage && 1 != a.messPage)
      ? 14 != a.quest[a.pam] || (4 != a.messPage && 2 != a.messPage)
        ? 16 == a.quest[a.pam] && 1 == a.christmas
          ? (a.mess.set_text(
              "Pam: If you see Santa, give him some of these\ngingerbread cookies."
            ),
            a.food[4]++,
            (a.messFin = true))
          : 16 == a.quest[a.pam]
          ? (a.mess.set_text(
              "Pam: I'll never forget how helpful you've been.\nCome back to see me anytime you run\nout of gingerbread cookies."
            ),
            0 == a.food[4] && (a.food[4] += 10),
            (a.messFin = true))
          : 1 == a.quest[a.pam] % 2 &&
            2 < a.quest[a.pam] &&
            13 > a.quest[a.pam] &&
            (a.mess.set_text(
              "Pam: Thank you so much!\nIf you find any more blue flowers,\nplease bring them to me."
            ),
            (a.messFin = true))
        : ((a.quest[a.pam] = 15),
          a.mess.set_text(
            "Pam: Here, you'll need this blue crystal to find it.\n(She hands you a blue crystal.)"
          ),
          (a.messFin = true))
      : (a.mess.set_text(
          "Pam: My son once made a special type of armor\nthat would prevent you from being\npoisoned. He hid it somewhere in\nthe Multiple Mountains."
        ),
        15 == a.quest[a.pam] && (a.messFin = true))
  },
  (a) => {
    0 == a.quest[a.dig] && 1 == a.messPage
      ? (a.mess.set_text(
          "I lost my special locket! Will you\nhelp me find it?"
        ),
        a.showYesNoOptions(),
        a.enterButton.set_visible(false))
      : 1 == a.quest[a.dig] && 1 == a.messPage
      ? (a.mess.set_text(
          "I laid it down somewhere in the grass\nabout a week ago. Maybe it got covered\nup by dirt."
        ),
        (a.messFin = true))
      : 2 == a.quest[a.dig] && 1 == a.messPage
      ? a.mess.set_text("You found it!")
      : 2 == a.quest[a.dig] && 2 == a.messPage
      ? (a.mess.set_text(
          C.plus(
            C.plus("Thank you, ", a.charName.get_text()),
            "!\nHere, take this.\n(She hands you 25 gold coins.)"
          )
        ),
        (a.quest[a.dig] = 3),
        (a.gold += 25),
        a.hitMax(),
        a.fame++,
        (a.messFin = true))
      : 3 == a.quest[a.dig] &&
        1 == a.messPage &&
        (a.mess.set_text("Thank you so much for finding my locket."),
        (a.messFin = true))
  },
  (a) => {
    if (3 > a.quest[a.bBomb])
      a.mess.set_text(
        "Wanna hear a secret?\nThere's a rarely used entrance to\nCreepers' Cavern east of the one most\npeople use."
      ),
        (a.messFin = true)
    else if (0 == a.quest[a.mChal] && 1 == a.messPage)
      a.mess.set_text("Do you enjoy going on quests?"), a.showYesNoOptions()
    else if (1 == a.quest[a.mChal])
      a.mess.set_text(
        "I need for you to journey to the western\npart of the Multiple Mountains.\nThere's a chalice there filled with oil.\nI need for you to light it with fire."
      ),
        (a.messFin = true)
    else if (2 == a.quest[a.mChal] || 2 < a.quest[a.mChal])
      a.mess.set_text(
        C.plus(
          C.plus("Great work, ", a.charName.get_text()),
          ".\nNow people that are exploring the mountains\nhave a place to go when they're cold."
        )
      ),
        2 == a.quest[a.mChal] && (a.fame++, (a.quest[a.mChal] = 3)),
        (a.messFin = true)
  },
  (a) => {
    1 == a.messPage
      ? (a.mess.set_text("I sell bombs for 25 gold each.\nAre you interested?"),
        a.showYesNoOptions())
      : 2 == a.messPage &&
        (a.mess.set_text("How many do you want to buy?\n(1 bomb = 25 gold)"),
        a.sell.set_y(470),
        a.sell.set_text("1"),
        a.sell.setTextFormat(a.sellFormat),
        a.sell.set_visible(true),
        a.exitButton.set_x(530),
        a.exitButton.set_y(520),
        a.exitButton.set_visible(true),
        a.buyButton.set_visible(true),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "The Creeper keeps using its shell\nas a shield. If only I had a SKILL that could\nstun it, maybe it would put its guard\ndown."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Elemental magic uses Earth's elements\nsuch as rock, ice, lightning, or fire"
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage
      ? (a.mess.set_text(
          "I'll trade rubies for 20 medallions each.\nAre you interested?"
        ),
        a.showYesNoOptions())
      : 2 == a.messPage &&
        (a.mess.set_text(
          "How many do you want to buy?\n(1 ruby = 20 medallions)"
        ),
        a.sell.set_y(470),
        a.sell.set_text("1"),
        a.sell.setTextFormat(a.sellFormat),
        a.sell.set_visible(true),
        a.exitButton.set_x(530),
        a.exitButton.set_y(520),
        a.exitButton.set_visible(true),
        a.tradeButton.set_visible(true),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage && 0 < a.dia
      ? (a.mess.set_text("I'll buy diamonds from you for 100 gold a piece?"),
        a.showYesNoOptions())
      : 1 == a.messPage && 0 == a.dia
      ? (a.mess.set_text(
          "If you find any diamonds, I'll buy them\nfor 100 gold a piece."
        ),
        (a.messFin = true))
      : 2 == a.messPage &&
        (a.mess.set_text(
          "How many do you want to sell?\n(1 diamond = 100 gold)"
        ),
        a.sell.set_y(470),
        a.sell.set_text(n.string(a.dia)),
        a.sell.setTextFormat(a.sellFormat),
        a.sell.set_visible(true),
        a.exitButton.set_x(530),
        a.exitButton.set_y(520),
        a.exitButton.set_visible(true),
        a.sellButton.set_visible(true),
        (a.messFin = true))
  },
  (a) => {
    0 == a.quest[a.canteen]
      ? (1 == a.messPage &&
          a.mess.set_text("Please... help...\nI'm so... thirsty..."),
        2 == a.messPage &&
          (a.mess.set_text(
            "Take... my... canteen...\nFill it... with wat... water..."
          ),
          a.quest[a.canteen]++))
      : 1 == a.quest[a.canteen]
      ? (a.mess.set_text(
          "Hurry... I... need... water...\n(press 'F' when standing in water\nto fill the canteen)"
        ),
        (a.messFin = true))
      : 2 == a.quest[a.canteen]
      ? (a.mess.set_text(
          "Thank you so much!\nHere, you can have this diamond."
        ),
        a.dia++,
        a.fame++,
        (a.messFin = true),
        (a.quest[a.canteen] = 3),
        (a.messPage = 1))
      : 2 < a.quest[a.canteen] &&
        (a.mess.set_text(
          C.plus(
            C.plus("You are a true hero, ", a.charName.get_text()),
            ".\nLet me tell you a secret. There's a hidden\nunderground chamber southeast of here."
          )
        ),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "In order to activate the magma furnace,\nyou must input the correct code. I'll give\nyou a little clue."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "The code is equal to the perimeter of a\nquadrilateral that has a length of " +
            a.pSide1 +
            " and a\nheight of " +
            a.pSide2 +
            "."
        ),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage
      ? (a.mess.set_text("Input the code to open the furnace."),
        a.sell.set_text("?"),
        a.sell.setTextFormat(a.sellFormat),
        a.sell.set_visible(true))
      : 2 == a.messPage &&
        (n.parseInt(a.sell.get_text()) == a.perimeter
          ? 7 == a.quest[a.bBomb]
            ? (a.mess.set_text(
                "A door to the furnace opens. You use\nyour bucket to scoop up some magma."
              ),
              (a.quest[a.bBomb] = 8))
            : a.mess.set_text(
                "A door to the furnace opens. Inside you\nnotice very hot magma."
              )
          : a.mess.set_text("That is not the correct code."),
        a.sell.set_visible(false),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "You feel a very powerful energy emitting\nfrom the pedestal. You hear a strange voice say,\n'Place a Troll Wristband upon me, if you dare!"
    ),
      0 < a.loot[a.tBand] && a.showYesNoOptions(),
      0 == a.loot[a.tBand] && (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You feel a very powerful energy emitting\nfrom the pedestal. You hear a strange voice say,\n'Place a Minotaur Horn upon me, if you dare!"
    ),
      0 < a.loot[a.mHorn] && a.showYesNoOptions(),
      0 == a.loot[a.mHorn] && (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You feel a very powerful energy emitting\nfrom the pedestal. You hear a strange voice say,\n'Place a Mage's Hat upon me, if you dare!"
    ),
      0 < a.loot[a.mHat] && a.showYesNoOptions(),
      0 == a.loot[a.mHat] && (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You feel a very powerful energy emitting\nfrom the pedestal. You hear a strange voice say,\n'Place 6 pinches of Void Ash upon me, if you\ndare!"
    ),
      6 <= a.loot[a.vAsh] && a.showYesNoOptions(),
      6 > a.loot[a.vAsh] && (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "When you are ready for battle, step onto\nthe magic symbol."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage
      ? a.mess.set_text(
          "Welcome to the battle arena. You can\nfight monsters and warriors here and earn\nprizes."
        )
      : 2 == a.messPage
      ? a.mess.set_text(
          "If you want to gain access to the arena, you\nmust first prove your valor."
        )
      : 3 == a.messPage && 0 == a.loot[a.aClub]
      ? (a.mess.set_text(
          "Retrieve an Alpha Club from Creepers' Cavern\nand we'll talk more..."
        ),
        0 == a.quest[a.access] && (a.quest[a.access] = 1),
        (a.messFin = true))
      : 3 == a.messPage &&
        0 < a.loot[a.aClub] &&
        (a.mess.set_text(
          "You have an Alpha Club! Impressive.\nI'll grant you access to the Tame section of the\narena on the left. Be sure to speak with Thales\nbefore you enter."
        ),
        (a.quest[a.access] = 2),
        a.fame++,
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "If you want access to the Savage Section of\nthe arena, you first need to win " +
        (5 - a.tameWins) +
        " more\nbattles in the Tame Section."
    ),
      4 == a.tameWins &&
        a.mess.set_text(
          "If you want access to the Savage Section of\nthe arena, you first need to win " +
            (5 - a.tameWins) +
            " more\nbattle in the Tame Section."
        ),
      (a.messFin = true)
  },
  (a) => {
    3 == a.quest[a.access]
      ? (a.mess.set_text("Well done, you're well on your way."),
        (a.quest[a.access] = 4),
        (a.messPage = 1))
      : 4 == a.quest[a.access]
      ? (a.mess.set_text(
          "To gain access to the Savage Section of our\narena, you must once again prove your courage.\nBring me an Alpha Axe taken from an Alpha\nMinotaur."
        ),
        0 == a.loot[a.aAxe]
          ? (a.messFin = true)
          : 0 < a.loot[a.aAxe] &&
            ((a.quest[a.access] = 5), a.fame++, (a.messPage = 1)))
      : 5 == a.quest[a.access] && 0 == a.savageWins
      ? (a.mess.set_text(
          "You rise to the challenge yet again.\nI shall now grant you access to the Savage\nSection of the arena. Try to win at least\n5 battles in the Savage Section."
        ),
        (a.messFin = true))
      : 5 == a.quest[a.access] &&
        5 > a.savageWins &&
        (a.mess.set_text(
          "If you want access to the Elite Section of\nthe arena, you first need to win " +
            (5 - a.savageWins) +
            " more\nbattles in the Savage Section."
        ),
        4 == a.tameWins &&
          a.mess.set_text(
            "If you want access to the Elite Section of\nthe arena, you first need to win " +
              (5 - a.savageWins) +
              " more\nbattle in the Savage Section."
          ),
        (a.messFin = true))
  },
  (a) => {
    5 == a.quest[a.access]
      ? (a.mess.set_text("You're becoming quite the warrior."),
        (a.quest[a.access] = 6),
        (a.messPage = 1))
      : 6 == a.quest[a.access]
      ? (a.mess.set_text(
          "To gain access to the Elite Section of our\narena, you must really show your worth.\nBring me an Alpha Scepter taken from an Alpha\nMage."
        ),
        0 == a.loot[a.aScepter]
          ? (a.messFin = true)
          : 0 < a.loot[a.aScepter] &&
            ((a.quest[a.access] = 7), a.fame++, (a.messPage = 1)))
      : 7 == a.quest[a.access] && 0 == a.eliteWins
      ? (a.mess.set_text(
          "You beat an Alpha Mage?!\nI shall now grant you access to the Elite\nSection of the arena. You should speak with\nThales before your first Elite battle."
        ),
        (a.messFin = true))
      : 8 == a.quest[a.access] &&
        5 > a.eliteWins &&
        (a.mess.set_text("Best of luck... You're going to need it."),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text("Wow! You are doing so well.\nCan you beat Kid Genius?"),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("You have become the arena's greatest warrior!"),
      8 == a.quest[a.access] && ((a.quest[a.access] = 9), (a.fame += 5)),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "We are gathering numerous items\nyou can buy with your medallions. In the\nmeantime, try to win as many as you can.\nCheck back soon."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "You can however learn some new\nskills. Talk to my partner over there."
        ),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "Oh, how badly do I want the Soul Sword.\nWith each successful hit, it uses 1 magic point\nto increase it's strength. If you miss, it's strength\nresets..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "This entire place has a spell over it causing\nmy weapons to be almost useless...\nIf only I had an upgraded Honed Staff..."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Jonus: There once was a suit of armor known\nas Alpha Armor. It could be upgraded many\ntimes and even had some special powers."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "Jonus: Last I heard, it was hidden in a green\nchest... probably in a dangerous place.\nIf you ever find the Alpha Armor, show me and\nI'll teach you how to upgrade it."
        ),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Jonus: You found the Alpha Armor!\nI will now teach you how to upgrade it."
      ),
      2 == a.messPage &&
        (a.mess.set_text("Jonus teaches you 2 new crafting recipes."),
        a.craftsTile[11].set_x(220),
        a.craftsTile[11].set_y(430),
        a.craftsTile[11].set_visible(true),
        a.craftsTile[12].set_x(380),
        a.craftsTile[12].set_y(430),
        a.craftsTile[12].set_visible(true),
        (a.crafts[11] = 1),
        (a.crafts[12] = 1),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "Jonus: The nice thing about Alpha Armor\nis that you can upgrade it forever."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage
      ? (a.mess.set_text("What do you want to type into the keypad?"),
        a.codeInput.set_text("?"),
        a.codeInput.setTextFormat(a.sellFormat),
        a.codeInput.set_visible(true))
      : 2 == a.messPage &&
        (n.parseInt(a.codeInput.get_text()) == (a.an1 | 0)
          ? (10 != a.quest[a.curse] && (a.fame++, (a.quest[a.curse] = 10)),
            a.gWallHorz[52].set_visible(false),
            a.gWallHorz[53].set_visible(false),
            a.mess.set_text("That's it!!!"))
          : a.mess.set_text("That is not the correct code."),
        a.codeInput.set_visible(false),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text("Arc's son: I'm free!!!!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Arc: We found him!"), a.fame++, (a.quest[a.curse] = 9)
  },
  (a) => {
    a.mess.set_text(
      "Arc: There's a lock on his cell, and\nthere appears to be a keypad where we can\nenter a code. It appears that there are\nthree digits in the code."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Arc: Thanks for saving my son.\nHere, take these gingerbread cookies as\na reward."
    ),
      (a.food[4] = 99),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "I know that device over there actives a\nbridge. I just don't know where..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("You have no business here stranger.\nLeave at once."),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Thanks for bringing water to my son."), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Help! My squad and I were sent by\nKing Mathius to destroy the Creepers' Nest\nbut there are just too many of them."
    ),
      (a.quest[a.bBomb] = 10),
      (a.messPage = 1)
  },
  (a) => {
    a.mess.set_text(
      "I need you to rush back to Muldivadd and\ntell my captain we need help.\nYou can find him in the throne room.\nHurry!"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "What?! The captain couldn't send any more\ntroops? There's simply no way you can help alone...\nThere are a dozen Creepers in here!\nDo what you can..."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You need to defeat " +
        (25 - (a.quest[a.bBomb] | 0)) +
        " more Creepers with the\nCreeper Crusher sword to clean out this nest."
    )
  },
  (a) => {
    a.mess.set_text(
      "You need to defeat 1 more Creeper with the\nCreeper Crusher sword to clean out this nest."
    )
  },
  (a) => {
    a.mess.set_text("You did it!")
  },
  (a) => {
    a.mess.set_text(
      "Get out, quick. It's much too\ndangerous in here for you!"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Ron: I've been trying to pump GeoMana but\nmy pump has run out of fuel.\nI really need some more quartz geodes.\nFive should do the trick."
    )
  },
  (a) => {
    a.mess.set_text(
      "Ron: Quartz geodes can only be found in the\nMultiple Mountains."
    ),
      (a.quest[a.geo] = 1),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Ron: If you are able to mine five quartz\ngeodes, bring them back to me so I can\nget my GeoMana pump to work."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Ron: You found some quartz geodes!\nCould I have five of them for my GeoMana\npump?"
    ),
      a.showYesNoOptions()
  },
  (a) => {
    a.mess.set_text(
      C.plus(C.plus("Ron: Thanks a lot, ", a.charName.get_text()), ".")
    ),
      (a.quest[a.geo] = 3),
      (a.messPage = 0)
  },
  (a) => {
    a.mess.set_text(
      "Ron: You want me to soak that Opah meat in\nGeoMana? Well, I would if my pump hadn't\njammed."
    ),
      (a.quest[a.oMan] = 17)
  },
  (a) => {
    a.mess.set_text(
      "Ron: Help me fix my jammed pump.\nGet a wrench from a Desert Dwarf."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Ron: Perfect! Let me see if I can fix the\nGeoMana pump."
      ),
      2 == a.messPage && a.mess.set_text("(Ron uses the wrench.)"),
      3 == a.messPage && a.mess.set_text("Ron: ..."),
      4 == a.messPage && a.mess.set_text("Ron: hmm."),
      5 == a.messPage && a.mess.set_text("(Ron rubs his chin.)"),
      6 == a.messPage && a.mess.set_text("Ron: ..."),
      7 == a.messPage &&
        a.mess.set_text("(Ron bangs on the pump. It begins to work!)"),
      8 == a.messPage &&
        a.mess.set_text("Ron: There, now let's soak that Opah meat."),
      8 == a.messPage &&
        a.mess.set_text("(Ron soaks the Opah meat in the GeoMana.)"),
      9 == a.messPage &&
        (a.mess.set_text(
          "Ron: You should probably take the meat to the\nVariable Volcano and have the GeoMana\ninfused by the heat."
        ),
        (a.quest[a.oMan] = 19),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Ron: Hey, if you run an important errand\nfor me, I'll teach you a cool SKILL."
      ),
      2 == a.messPage &&
        (a.mess.set_text(
          "Ron: Take this vial of GeoMana to girl\nnamed Sable in Dyce."
        ),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage &&
      a.mess.set_text(
        "Ron: Well done. As promised, I will teach\nyou the SKILL of CONVERT."
      ),
      2 == a.messPage &&
        a.mess.set_text(
          "Ron: When you use CONVERT, press the\nUP arrow to convert magic to gold,\nor press the DOWN arrow to convert\ngold to magic."
        ),
      3 == a.messPage &&
        (a.mess.set_text("You learned the SKILL of CONVERT!"),
        a.skillTile[7].set_x(300),
        a.skillTile[7].set_y(420),
        a.skillTile[7].set_visible(true),
        (a.messFin = true),
        (a.quest[a.geo] = 5),
        a.fame++,
        (a.skills[7] = 1))
  },
  (a) => {
    a.mess.set_text(
      "Ron: You need some GeoMana for a ring?\nThat'll cost ya 1,000 gold."
    ),
      a.showYesNoOptions()
  },
  (a) => {
    a.mess.set_text("Ron: You don't have enough gold."), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(C.plus(C.plus("Good luck, ", a.charName.get_text()), ".")),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "I'm so glad someone lit this chalice!\nI've been stranded out here for days now."
    )
  },
  (a) => {
    a.mess.set_text(
      "A Mountain Mage stole my rucksack.\nIf you get it back for me, I'll pay you!"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You got it!\nHere, you've earned this.\n(He hands you 200 gold coins.)"
    ),
      a.fame++,
      (a.gold += 200),
      a.hitMax(),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(C.plus(C.plus("Thanks, ", a.charName.get_text()), ".")),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Jorian: My dream is to become a solider for the\nKingdom of Muldivadd. Have you been to the\ncastle?"
    ),
      a.showYesNoOptions()
  },
  (a) => {
    a.mess.set_text(
      "Jorian: You've been to Castle Muldivadd?!\nWow! The next time you go, please let\none of the soldiers know I'd love to be trained."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Soldier: He's doing well. I think\nhe's about ready to use a beginner's sword.\nCould we have yours?"
    ),
      a.showYesNoOptions()
  },
  (a) => {
    a.mess.set_text(
      "Soldier: He's doing well. I think\nhe's about ready to use a sword.\nCould we have your bomb sword?"
    ),
      a.showYesNoOptions()
  },
  (a) => {
    a.mess.set_text(
      "Soldier: He's doing well. We could\nreally use that sword you're holding.\nCould you equip a different weapon?"
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Soldier: He's doing well. I think\nhe's ready to use a beginner's sword.\nIf you find one, please bring it here."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      C.plus(
        C.plus("Jorian: Thanks, ", a.charName.get_text()),
        ",\nfor telling him. He's going to train me\nto use a sword."
      )
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Soldier: Your sword will help a lot.\nJorian will also need to learn how to\nslow down his enemy's. Go show him how to\nuse magic to slow down an attacker."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Jorian: This sword is great!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Soldier:  Very good!"),
      (a.messFin = true),
      (a.quest[a.dream] = 5),
      (a.messPage = 1),
      a.fame++
  },
  (a) => {
    a.mess.set_text("Jorian: You're good with magic!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Soldier: You're a great teacher.\nJorian's ready for battle. Meet him in the Temple\nof Tessellation."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("Jorian: You're good with magic!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      C.plus(
        C.plus("Hey, ", a.charName.get_text()),
        ".\nIt's me, Jorian. I'm a soldier now!\nI have you to thank for it too!"
      )
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Some beasts only have a weakness to magic.\nYour weapons will not be very effective\nagainst them."
    ),
      (a.messFin = true)
  },
  (a) => {
    1 == a.messPage &&
      (a.mess.set_text(
        "I can upgrade your firewall skill.\nTrade me " +
          5 * a.fwUpgrade +
          " dragon scales and " +
          3 * a.fwUpgrade +
          " medallions."
      ),
      a.showYesNoOptions()),
      2 == a.messPage &&
        (a.mess.set_text("You don't have enough items to upgrade."),
        (a.messFin = true)),
      3 == a.messPage &&
        (a.mess.set_text("Your FIREWALL is now at level " + a.fwUpgrade + "."),
        (a.messFin = true))
  },
  (a) => {
    1 == a.messPage
      ? (a.mess.set_text(
          "Sir Albert Newton: Would you like one\nof my special apples? I'll trade you them\nat a rate of 1 Newton Apple per medallion."
        ),
        a.showYesNoOptions())
      : 2 == a.messPage &&
        (a.mess.set_text(
          "How many do you want to buy?\n(1 Newton Apple = 1 Medallion)"
        ),
        a.sell.set_y(470),
        a.sell.set_text("1"),
        a.sell.setTextFormat(a.sellFormat),
        a.sell.set_visible(true),
        a.exitButton.set_x(530),
        a.exitButton.set_y(520),
        a.exitButton.set_visible(true),
        a.tradeButton.set_visible(true))
    rando.comparearea(10, 10) &&
      (8 == a.quest[a.dream]
        ? (a.mess.set_text("Whew! It's hot out here..."),
          (a.quest[a.dream] = 9),
          (a.messPage = 1))
        : 9 == a.quest[a.dream]
        ? (a.mess.set_text(
            "A desert dwarf took my training manual.\nSee if you can get it back."
          ),
          (a.messFin = true))
        : 10 == a.quest[a.dream]
        ? (a.mess.set_text(
            C.plus(
              C.plus(
                "My training manual! How'd you get it?!\nThanks, ",
                a.charName.get_text()
              ),
              "."
            )
          ),
          a.fame++,
          (a.quest[a.dream] = 11),
          (a.messPage = 1))
        : 11 == a.quest[a.dream] &&
          (a.mess.set_text(
            "I need to report back to the castle now.\nI'm hoping to get promoted!"
          ),
          (a.messFin = true)))
  },
  (a) => {
    5 == a.quest[a.dream]
      ? (a.mess.set_text("Jorian: You made it!"),
        a.fame++,
        (a.quest[a.dream] = 6),
        (a.messPage = 1))
      : 6 == a.quest[a.dream]
      ? (a.mess.set_text("Jorian: Show me how to beat mages."),
        (a.messFin = true))
      : 7 == a.quest[a.dream]
      ? (a.mess.set_text("Jorian: You're a skilled warrior!"),
        a.fame++,
        (a.quest[a.dream] = 8),
        (a.messPage = 1))
      : 8 == a.quest[a.dream] &&
        (a.mess.set_text("Jorian: I think I'll head to Division Desert next."),
        (a.messFin = true))
  },
  (a) => {
    a.mess.set_text(
      "If you want to save your progress, click \non STATS, and then click the SAVE button."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Your SPEED can help you in 3 ways:\n1) You'll dodge attacks more often.\n2) You'll walk quicker.\n3) You'll not be attacked as often."
    )
  },
  (a) => {
    a.mess.set_text(
      "Your STRENGTH is also important.\nThe stronger you are, the more damage you can\ndo during a battle."
    )
  },
  (a) => {
    a.mess.set_text(
      "Equip weapons and armor to increase your\nstrength and speed."
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "You made it!\nAll we need to do now is defeat the Denominator\nand we can save the king.\nYou attack first, and I'll help out."
    )
  },
  (a) => {
    a.mess.set_text(
      C.plus(
        C.plus(
          "You won! You defeated The Denominator.\nYou are a true hero, ",
          a.charName.get_text()
        ),
        "."
      )
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      C.plus(
        C.plus("Thank you, ", a.charName.get_text()),
        "!\nI am in your debt. Let us meet back at the\ncastle."
      )
    ),
      (a.messFin = true)
  },
  (a) => {
    a.mess.set_text("You cannot have the Orb of Life!!!"), (a.messFin = true)
  },
  (a) => {
    a.mess.set_text(
      "Be careful, those magic floor tiles will\nabsorb your magic."
    ),
      (a.messFin = true)
  },
]
// a.mess.set_text[\w\r\s\W]+?(?:a\.messFin = true|a\.showYesNoOptions|rando\.msg|this\.addChild)\)?

function logFunctionCalls(func) {
  return function (...args) {
    console.log(
      `Called ${func.name} from ${new Error().stack.split("\n")[1].trim()}`
    )
    return func.apply(this, args)
  }
}
// rando.msg\((\d+)\)
// rando.msg(a, $1)

// Example usage:
function add(a, b) {
  return a + b
}

const loggedAdd = logFunctionCalls(add)

loggedAdd(2, 3) // Output: Called add from <filename>:<line number>
