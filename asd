              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.skills[Enum.Skill.hint] == 0 &&
            manager.medallions >= 3 &&
            manager.skillTile[Enum.Skill.hint].get_visible() == 1
          ) {
            newItem("19_15 - skill:hint")
            // manager.skills[Enum.Skill.hint] = 1
            manager.medallions -= 3
            this.medallionAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.skills[Enum.Skill.shield] == 0 &&
            manager.medallions >= 200 &&
            manager.skillTile[Enum.Skill.shield].get_visible() == 1
          ) {
            newItem("19_15 - skill:shield")
            // manager.skills[Enum.Skill.shield] = 1
            manager.medallions -= 200
            this.medallionAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 5 &&
            manager.food[Enum.Food.apple] < 99 &&
            this.itemTile[0].get_visible() == 1
          ) {
            newItem("20_20 - food:apple")
            manager.gold -= 5
            this.buyAni()
            this.shopMess.set_text(
              "Eat this when your health is getting low.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 1 &&
            manager.food[Enum.Food.honey] < 99 &&
            this.itemTile[1].get_visible() == 1
          ) {
            newItem("20_20 - food:honey")
            --manager.gold
            this.buyAni()
            this.shopMess.set_text(
              "A drop of honey will help restore your magic skills.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 15 &&
            manager.food[Enum.Food.grapes] < 99 &&
            this.itemTile[2].get_visible() == 1
          ) {
            newItem("20_20 - food:grapes")
            manager.gold -= 15
            this.buyAni()
            this.shopMess.set_text(
              "Grapes are very good for your health!",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 125 &&
            manager.food[Enum.Food.carrot] < 99 &&
            this.itemTile[6].get_visible() == 1
          ) {
            newItem("12_9 - food:carrot")
            manager.gold -= 125
            this.buyAni()
            this.shopMess.set_text(
              "A vegetable with balanced nutrition!",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 200 &&
            manager.food[Enum.Food.beefJerky] < 99 &&
            this.itemTile[7].get_visible() == 1
          ) {
            newItem("12_9 - food:beefJerky")
            manager.gold -= 200
            this.buyAni()
            this.shopMess.set_text(
              "A great source of protein to keep you healthy.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 250 &&
            manager.food[Enum.Food.cherries] < 99 &&
            this.itemTile[8].get_visible() == 1
          ) {
            newItem("12_9 - food:cherries")
            manager.gold -= 250
            this.buyAni()
            this.shopMess.set_text(
              "Cherries can give you a quick boast of magic.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 300 &&
            manager.food[Enum.Food.chocolate] < 99 &&
            this.itemTile[9].get_visible() == 1
          ) {
            newItem("?_? - food:chocolate")
            manager.gold -= 300
            this.buyAni()
            this.shopMess.set_text(
              "You're gonna love this chocolate bar.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 450 &&
            manager.food[Enum.Food.steak] < 99 &&
            this.itemTile[10].get_visible() == 1
          ) {
            newItem("?_? - food:steak")
            manager.gold -= 450
            this.shopMess.set_text(
              "There is a lot of protein in this juicy steak!",
            )
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 500 &&
            manager.food[Enum.Food.peppers] < 99 &&
            this.itemTile[12].get_visible() == 1
          ) {
            newItem("?_? - food:peppers")
            // manager.food[Enum.Food.peppers] =
            //   manager.food[Enum.Food.peppers] + 1
            manager.gold -= 500
            this.buyAni()
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 49 &&
            manager.magic[Enum.Magic.slow] < 1 &&
            manager.magicTile[Enum.Magic.slow].get_visible() == 1
          ) {
            newItem("21_20 - magic:slow")
            manager.gold -= 50
            this.buyAni()
            this.shopMess.set_text(
              "You will now be able to slow down your enemy's attack.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 99 &&
            manager.magic[Enum.Magic.heal] < 1 &&
            manager.magicTile[Enum.Magic.heal].get_visible() == 1
          ) {
            newItem("21_20 - magic:heal")
            manager.gold -= 100
            this.buyAni()
            this.shopMess.set_text("Use this to heal your wounds.")
          } else if (
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 199 &&
            manager.magic[Enum.Magic.blast] < 1 &&
            manager.magicTile[Enum.Magic.blast].get_visible() == 1
          ) {
            newItem("21_20 - magic:blast")
            manager.gold -= 200
            this.buyAni()
            this.shopMess.set_text(
              "This will double your attack whenever you cast it.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 299 &&
            manager.magic[Enum.Magic.regen] < 1 &&
            manager.magicTile[Enum.Magic.regen].get_visible() == 1
          ) {
            newItem("13_17 - magic:regen")
            // manager.magic[Enum.Magic.regen] = 1
            manager.gold -= 300
            this.buyAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 2e3 &&
            manager.magic[Enum.Magic.cloud] < 1 &&
            manager.magicTile[Enum.Magic.cloud].get_visible() == 1
          ) {
            newItem("13_17 - magic:cloud")
            // manager.magic[Enum.Magic.cloud] = 1
            manager.gold -= 2e3
            this.buyAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 900 &&
            manager.magic[Enum.Magic.weak] < 1 &&
            manager.magicTile[Enum.Magic.weak].get_visible() == 1
          ) {
            newItem("13_17 - magic:weak")
            manager.gold -= 900
            this.buyAni()
            this.shopMess.set_text(
              "Cast this spell and foes will deal less damage.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 4500 &&
            manager.magic[Enum.Magic.refresh] < 1 &&
            manager.magicTile[Enum.Magic.refresh].get_visible() == 1
          ) {
            newItem("11_9 - magic:refresh")
            // manager.magic[Enum.Magic.refresh] = 1
            manager.gold -= 4500
            this.buyAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 1e4 &&
            manager.magic[Enum.Magic.lightning] < 1 &&
            manager.magicTile[Enum.Magic.lightning].get_visible() == 1
          ) {
            newItem("11_9 - magic:lightning")
            manager.gold -= 1e4
            this.buyAni()
            this.shopMess.set_text(
              "A mighty spell that deals great damage when cast.",
--
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 9 &&
            manager.weapon[Enum.Weapon.club] < 1 &&
            this.weapTile[Enum.Weapon.club].get_visible() == 1 &&
            manager.weapon[Enum.Weapon.upgradeStaff] == 0
          ) {
            newItem("20_20 - weapon:club")
            manager.gold -= 10
            this.buyAni()
            this.shopMess.set_text(
              "Not a strong weapon, but it will help.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 49 &&
            manager.weapon[Enum.Weapon.dagger] < 1 &&
            this.weapTile[Enum.Weapon.dagger].get_visible() == 1
          ) {
            newItem("20_20 - weapon:dagger")
            manager.gold -= 50
            this.buyAni()
            this.shopMess.set_text("A quick weapon, use it well.")
          } else if (
--
              true,
            ) &&
            manager.gold > 199 &&
            manager.weapon[Enum.Weapon.sword] < 1 &&
            this.weapTile[Enum.Weapon.sword].get_visible() == 1 &&
            manager.weapon[Enum.Weapon.bombSword] < 1
          ) {
            console.log("buy sword")
            newItem("20_20 - weapon:sword")
            manager.gold -= 200
            this.buyAni()
            this.shopMess.set_text(
              "A simple sword, but mighty still.",
--
              true,
            ) &&
            manager.gold >= 800 &&
            manager.weapon[Enum.Weapon.royalSword] < 1 &&
            this.weapTile[Enum.Weapon.royalSword].get_visible() ==
              1 &&
            manager.weapon[Enum.Weapon.creeperCrusher] == 0
          ) {
            newItem("13_17 - weapon:royalSword")
            // manager.weapon[Enum.Weapon.royalSword] = 1
            manager.gold -= 800
            this.buyAni()
            this.shopMess.set_text(
--
              true,
            ) &&
            manager.gold >= 500 &&
            manager.weapon[Enum.Weapon.royalStaff] < 1 &&
            this.weapTile[Enum.Weapon.royalStaff].get_visible() ==
              1 &&
            manager.weapon[Enum.Weapon.refreshStaff] == 0
          ) {
            newItem("13_17 - weapon:royalStaff")
            // manager.weapon[Enum.Weapon.royalStaff] = 1
            manager.gold -= 500
            this.buyAni()
            this.shopMess.set_text(
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 49 &&
            manager.armor[Enum.Armor.vest] < 1 &&
            manager.armorTile[Enum.Armor.vest].get_visible() == 1
          ) {
            newItem("20_20 - armor:vest")
            manager.gold -= 50
            this.buyAni()
            this.shopMess.set_text(
              "This vest will make your steps quicker.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 299 &&
            manager.armor[Enum.Armor.robe] < 1 &&
            manager.armorTile[Enum.Armor.robe].get_visible() == 1
          ) {
            newItem("20_20 - armor:robe")
            manager.gold -= 300
            this.buyAni()
            this.shopMess.set_text(
              "When you wear this robe, you'll have more magic.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold > 799 &&
            manager.armor[Enum.Armor.iron] < 1 &&
            manager.armorTile[Enum.Armor.iron].get_visible() == 1
          ) {
            newItem("20_20 - armor:iron")
            manager.gold -= 800
            this.buyAni()
            this.shopMess.set_text("This is a great piece of armor!")
          } else if (
--
              true,
            ) &&
            manager.gold >= 1500 &&
            manager.armor[Enum.Armor.royalArmor] < 1 &&
            manager.armorTile[Enum.Armor.royalArmor].get_visible() ==
              1 &&
            manager.armor[Enum.Armor.nobleArmor] == 0
          ) {
            newItem("13_17 - armor:royalArmor")
            // manager.armor[Enum.Armor.royalArmor] = 1
            manager.gold -= 1500
            this.buyAni()
            this.shopMess.set_text(
--
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 700 &&
            manager.armor[Enum.Armor.mysticCloak] < 1 &&
            manager.armorTile[Enum.Armor.mysticCloak].get_visible() ==
              1
          ) {
            newItem("13_17 - armor:mysticCloak")
            // manager.armor[Enum.Armor.mysticCloak] = 1
            manager.gold -= 700
            this.buyAni()
            this.shopMess.set_text(
--
              true,
            ) &&
            manager.gold >= 250 &&
            manager.armor[Enum.Armor.sunArmor] < 1 &&
            manager.armorTile[Enum.Armor.sunArmor].get_visible() ==
              1 &&
            manager.armor[Enum.Armor.soulArmor] == 0
          ) {
            newItem("12_9 - armor:sunArmor")
            manager.gold -= 250
            this.buyAni()
            this.shopMess.set_text(
              "Wear this to protect yourself from the desert heat.",
--
              this.get_mouseX(),
              this.get_mouseY(),
              true,
            ) &&
            manager.gold >= 3500 &&
            manager.armor[Enum.Armor.speedVest] < 1 &&
            manager.armorTile[Enum.Armor.speedVest].get_visible() == 1
          ) {
            newItem("12_9 - armor:speedVest")
            manager.gold -= 3500
            this.buyAni()
            this.shopMess.set_text(
              "A strange piece of armor that will make you quick!",
--
              manager.mobSecs = this.prize3 < 25 ? 4 : 5
            } else if (manager.mName == "EMPEROR COBRA") {
              newObserveObject.fightMes[
                newObserveObject.fightMesCurrent
              ].set_text(
                "You find the Ring of Poison on the EMPEROR COBRA!!!",
              )
              this.batEndMesMover()
              newItem("item:ring of poison")
              // manager.ring4 = 1
              manager.quest[Enum.Quest.rings] = 6
            } else if (manager.mName == "ICE SAGE") {
              newObserveObject.fightMes[
                newObserveObject.fightMesCurrent
              ].set_text(
                "You find the Ring of Magic on the ICE SAGE!!!",
              )
              this.batEndMesMover()
              manager.mobSecs = this.prize3 < 25 ? 4 : 5
              newItem("item:ring of magic")
              // manager.ring5 = 1
              newQuest("15_16", "rings", 9, false)
              // manager.quest[Enum.Quest.rings] = 9
              manager.fame += 2
            } else if (manager.mName == "DEATH REAPER") {
              newObserveObject.fightMes[
                newObserveObject.fightMesCurrent
              ].set_text("You now possess the Ring of Death!")
              this.batEndMesMover()
              manager.mobSecs = this.prize3 < 25 ? 4 : 5
              newItem("item:ring of death")
              // manager.ring7 = 1
              newQuest("16_10", "rings", 16, false)
              // manager.quest[Enum.Quest.rings] = 16
              manager.fame++
--
                this.weapTile[Enum.Weapon.pitchfork].set_x(300)
                this.weapTile[Enum.Weapon.pitchfork].set_y(420)
                this.weapTile[Enum.Weapon.pitchfork].set_visible(true)
                this.enterFunc()
              } else if (
                manager.correct - manager.wrong > 9 &&
                manager.skills[Enum.Skill.dig] == 0
              ) {
                newItem("19_20 - skill:dig")
                // manager.skills[Enum.Skill.dig] = 1
                manager.mess.set_text("You've learned the skill DIG!")
                manager.mess.setTextFormat(manager.messFormat)
                manager.mess.set_visible(true)
--
                  )
                }
                manager.skillTile[Enum.Skill.dig].set_visible(true)
                this.enterFunc()
              } else if (
                manager.correct - manager.wrong > 49 &&
                manager.skills[Enum.Skill.kick] == 0
              ) {
                newItem("19_20 - skill:kick")
                // manager.skills[Enum.Skill.kick] = 1
                manager.mess.set_text(
                  "You've learned the skill KICK!",
                )
--
              manager.quest[Enum.Quest.aSword] == 6
            ) {
              if (manager.weapon[Enum.Weapon.baneBlade] == 2) {
                manager.eHealth -= 80
                manager.eStr -= 50
                manager.speed += 2
              }
              manager.weapon[Enum.Weapon.baneBlade] = 0
              newItem("500_501 - weapon:aSword")
              // manager.weapon[Enum.Weapon.aSword] = 1
              this.weapTile[Enum.Weapon.aSword].set_x(300)
              this.weapTile[Enum.Weapon.aSword].set_y(440)
              this.weapTile[Enum.Weapon.aSword].set_visible(true)
--
              manager.loot[Enum.Loot.vHorn] -= 20
              manager.loot[Enum.Loot.cThread] -= 30
              manager.loot[Enum.Loot.gFeather] -= 5
              if (manager.weapon[Enum.Weapon.orcBlade] == 2) {
                manager.eStr -= 50
                manager.eSpeed -= 10
              }
              manager.weapon[Enum.Weapon.orcBlade] = 0
              newItem("200_200 - weapon:twinFury")
              // manager.weapon[Enum.Weapon.twinFury] = 1
              manager.messPage = 2
              this.weapTile[Enum.Weapon.twinFury].set_x(300)
              this.weapTile[Enum.Weapon.twinFury].set_y(420)
--
              manager.skills[Enum.Skill.medic] == 5 &&
              manager.loot[Enum.Loot.gFeather] >= 3 &&
              manager.loot[Enum.Loot.aScepter] >= 5
            ) {
              manager.loot[Enum.Loot.gFeather] -= 3
              manager.loot[Enum.Loot.aScepter] -= 5
              manager.messPage = 2
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 6
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.skills[Enum.Skill.medic] == 4 &&
              manager.loot[Enum.Loot.kCrest] >= 10 &&
              manager.loot[Enum.Loot.aAxe] >= 5
            ) {
              manager.loot[Enum.Loot.kCrest] -= 10
              manager.loot[Enum.Loot.aAxe] -= 5
              manager.messPage = 2
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 5
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.skills[Enum.Skill.medic] == 3 &&
              manager.loot[Enum.Loot.dScale] >= 10 &&
              manager.loot[Enum.Loot.gSkin] >= 10
            ) {
              manager.loot[Enum.Loot.dScale] -= 10
              manager.loot[Enum.Loot.gSkin] -= 10
              manager.messPage = 2
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 4
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.skills[Enum.Skill.medic] == 2 &&
              manager.loot[Enum.Loot.oCoin] >= 20 &&
              manager.loot[Enum.Loot.mStaff] >= 10
            ) {
              manager.loot[Enum.Loot.oCoin] -= 20
              manager.loot[Enum.Loot.mStaff] -= 10
              manager.messPage = 2
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 3
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.north == 18 &&
              manager.east == 25 &&
              manager.skills[Enum.Skill.medic] == 1 &&
              manager.loot[Enum.Loot.cFang] >= 5
            ) {
              manager.loot[Enum.Loot.cFang] -= 5
              manager.messPage = 2
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 2
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.east == 25 &&
              manager.skills[Enum.Skill.medic] == 0 &&
              manager.loot[Enum.Loot.tBand] >= 2 &&
              manager.messPage == 3
            ) {
              manager.loot[Enum.Loot.tBand] -= 2
              manager.messPage = 4
              this.dialogue()
              newItem("18_25 - skill:medic")
              // manager.skills[Enum.Skill.medic] = 1
              manager.skillTile[Enum.Skill.medic].set_x(300)
              manager.skillTile[Enum.Skill.medic].set_y(420)
              manager.skillTile[Enum.Skill.medic].set_visible(true)
--
              manager.bombCapacity += 50
              this.dialogue()
            } else if (
              manager.north == 19 &&
              manager.east == 22 &&
              manager.skills[Enum.Skill.reveal] == 0
            ) {
              manager.messPage = 1
              newItem("19_22 - skill:reveal")
              // manager.skills[Enum.Skill.reveal] = 1
              manager.loot[Enum.Loot.aAxe] -= 5
              manager.fame++
              this.dialogue()
--
              manager.mBox.set_visible(false)
              manager.mess.set_visible(false)
              this.addListeners()
            } else if (
              manager.charBottom[0].hitTestObject(manager.strGuy) &&
              manager.strGuy.get_visible() == 1
            ) {
              if (checker.strUpNpc == 1) {
                newItem("str up npc", 1)
                manager.loot[Enum.Loot.bClaw] -= 13
                this.enterBounceback()
              } else if (checker.strUpNpc == 2) {
                newItem("str up npc", 1)
                manager.loot[Enum.Loot.tBand] -= 15
                this.enterBounceback()
              } else if (checker.strUpNpc == 3) {
                newItem("str up npc", 1)
                manager.loot[Enum.Loot.mStaff] -= 12
                this.enterBounceback()
              } else if (checker.strUpNpc == 4) {
                newItem("str up npc", 1)
                manager.loot[Enum.Loot.fBone] -= 10
                this.enterBounceback()
              } else if (checker.strUpNpc == 5) {
                newItem("str up npc", 3)
                manager.loot[Enum.Loot.cFang] -= 15
                this.enterBounceback()
              } else if (checker.strUpNpc == 8) {
                newItem("str up npc", 5)
                manager.loot[Enum.Loot.oCoin] -= 50
                this.enterBounceback()
              } else if (checker.strUpNpc == 13) {
                newItem("str up npc", 5)
                manager.loot[Enum.Loot.kCrest] -= 10
                this.enterBounceback()
              } else if (checker.strUpNpc == 18) {
                newItem("str up npc", 5)
                manager.loot[Enum.Loot.dScale] -= 10
                this.enterBounceback()
              } else if (checker.strUpNpc == 23) {
                newItem("str up npc", 3)
                manager.loot[Enum.Loot.vHorn] -= 20
                this.enterBounceback()
              } else if (checker.strUpNpc == 26) {
                newItem("str up npc", 4)
                manager.slamstones -= 10
                manager.fame++
                this.enterBounceback()
              } else if (checker.strUpNpc == 30) {
                newItem("str up npc", 5)
                manager.shadowCrest -= 5
                this.enterBounceback()
              }
              manager.mBox.set_visible(false)
--
                "mouseDown",
                createObjectMixin(this, this.diaBuyHandler),
              )
            } else if (manager.north == 11 && manager.east == 12) {
              if (
                manager.gold > 99 &&
                manager.food[Enum.Food.sunflowerSeeds] < 99
              ) {
                newItem("11_12 - food:sunflowerSeeds")
                manager.gold -= 100
                manager.hitMax()
                manager.messPage = 3
              } else {
--
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 21 && manager.east == 23) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[44].set_visible(false)
              manager.tBoxUsed[44] = 1
              newItem("21_23 - diamonds")
              newItem("21_23 - gold")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 9 && manager.east == 13) {
              manager.messPage = 2
--
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 6 && manager.east == 13) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[0].set_visible(false)
              manager.tBoxUsed[51] = 1
              newItem("6_13 - food:grapes")
              newItem("6_13 - food:strawberry")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 11 && manager.east == 19) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[0].set_visible(false)
              manager.tBoxUsed[52] = 1
              newItem("11_19 - food:sunflowerSeeds")
              newItem("11_19 - food:strawberry")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 23 && manager.east == 10) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[0].set_visible(false)
              manager.tBoxUsed[50] = 1
              newItem("23_10 - diamonds")
              newItem("23_10 - food:newtonsApple")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 17 && manager.east == 20) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[45].set_visible(false)
              manager.tBoxUsed[45] = 1
              newItem("17_20 - gold")
              newItem("17_20 - food:beefJerky")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 15 && manager.east == 24) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[46].set_visible(false)
              manager.tBoxUsed[46] = 1
              newItem("15_24 - gold")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 10 && manager.east == 9) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[32].set_visible(false)
              manager.tBoxUsed[32] = 1
              newItem("10_9 - food:steak")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 9 && manager.east == 26) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[36].set_visible(false)
              manager.tBoxUsed[36] = 1
              newItem("9_26 - food:blueberries")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 21 && manager.east == 11) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[33].set_visible(false)
              manager.tBoxUsed[33] = 1
              newItem("21_11 - food:gummyBears")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 24 && manager.east == 11) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              // this.weapTile[Enum.Weapon.baneBlade].set_x(300)
              // this.weapTile[Enum.Weapon.baneBlade].set_y(420)
              // this.weapTile[Enum.Weapon.baneBlade].set_visible(true)
              manager.tBox[17].set_visible(false)
              manager.tBoxUsed[17] = 1
              newItem("24_11 - weapon:baneBlade")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 11 && manager.east == 15) {
              manager.fame++
--
              manager.crafts[Enum.Craft.craftRingGold] = 1
              this.dialogue()
              this.enterFunc()
              manager.loot[Enum.Loot.tBand] -= 5
              manager.loot[Enum.Loot.gSkin] -= 2
            } else if (manager.north == 21 && manager.east == 21) {
              manager.messPage = 1
              manager.fame++
              newItem("21_21 - skill:craft")
              // TODO
              // manager.skills[Enum.Skill.craft] = 1
              manager.crafts[Enum.Craft.chocolate] = 1
              manager.crafts[Enum.Craft.orange] = 1
--
              this.enterFunc()
              manager.magicTile[Enum.Magic.doubleDown].set_x(300)
              manager.magicTile[Enum.Magic.doubleDown].set_y(420)
              manager.magicTile[Enum.Magic.doubleDown].set_visible(
                true,
              )
              manager.tBox[29].set_visible(false)
              manager.tBoxUsed[29] = 1
              newItem("9_22 - magic:doubleDown")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (
              manager.north == 21 &&
              manager.east == 20 &&
              manager.char[0].get_x() < 75
            ) {
              newItem("21_20 - magic:crush")
              this.dialogue()
              this.enterFunc()
              manager.magicTile[Enum.Magic.crush].set_x(300)
              manager.magicTile[Enum.Magic.crush].set_y(420)
              manager.magicTile[Enum.Magic.crush].set_visible(true)
              manager.tBoxSound.play()
            } else if (manager.north == 18 && manager.east == 20) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("18_20 - gold")
              manager.tBox[19].set_visible(false)
              manager.tBoxUsed[19] = 1
              manager.tBoxSound.play()
              manager.keys = manager.keys - 1
            } else if (
              manager.north == 6 &&
              manager.east == 12 &&
              manager.charBottom[0].get_y() > 400
            ) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("6_12 - geode")
              manager.tBox[27].set_visible(false)
              manager.tBoxUsed[27] = 1
              manager.tBoxSound.play()
              manager.keys = manager.keys - 1
            } else if (manager.north == 17 && manager.east == 16) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("17_16 - diamonds")
              manager.tBox[26].set_visible(false)
              manager.tBoxUsed[26] = 1
              manager.tBoxSound.play()
              manager.keys = manager.keys - 1
            } else if (manager.north == 18 && manager.east == 17) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("18_17 - gold")
              manager.tBox[30].set_visible(false)
              manager.tBoxUsed[30] = 1
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (
              manager.north == 15 &&
              manager.east == 19 &&
              manager.char[0].get_x() < 300
            ) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("15_19 - gold")
              newItem("15_19 - item:bombs")
              if (manager.bombs > manager.bombCapacity) {
                manager.bombs = manager.bombCapacity
              }
              newItem("15_19 - food:banana")
              manager.tBox[20].set_visible(false)
              manager.tBoxUsed[20] = 1
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 11 && manager.east == 21) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              newItem("11_21 - item:bombs")
              if (manager.bombs > manager.bombCapacity) {
                manager.bombs = manager.bombCapacity
              }
              manager.tBox[34].set_visible(false)
              manager.tBoxUsed[34] = 1
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 14 && manager.east == 15) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              if (manager.quest[Enum.Quest.bBomb] > 3) {
                newItem("14_15 - item:bombs")
                if (manager.bombs > manager.bombCapacity) {
                  manager.bombs = manager.bombCapacity
                }
              }
              newItem("14_15 - food:orange")
              manager.tBox[21].set_visible(false)
              manager.tBoxUsed[21] = 1
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              // manager.armorTile[Enum.Armor.grimGear].set_x(300)
              // manager.armorTile[Enum.Armor.grimGear].set_y(420)
              // manager.armorTile[Enum.Armor.grimGear].set_visible(true)
              manager.tBox[18].set_visible(false)
              manager.tBoxUsed[18] = 1
              newItem("24_14 - armor:grimGear")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 9 && manager.east == 15) {
              manager.messPage = 2
--
              this.enterFunc()
              // manager.armorTile[Enum.Armor.phantomCoat].set_x(300)
              // manager.armorTile[Enum.Armor.phantomCoat].set_y(420)
              // manager.armorTile[Enum.Armor.phantomCoat].set_visible(
              //   true,
              // )
              manager.tBox[22].set_visible(false)
              manager.tBoxUsed[22] = 1
              newItem("9_15 - armor:phantomCoat")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 15 && manager.east == 21) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBox[23].set_visible(false)
              manager.tBoxUsed[23] = 1
              newItem("15_21 - gold")
              newItem("15_21 - item:bombs")
              if (manager.bombs > manager.bombCapacity) {
                manager.bombs = manager.bombCapacity
              }
              manager.hitMax()
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              this.itemTile[8].set_x(300)
              this.itemTile[8].set_y(420)
              this.itemTile[8].set_visible(true)
              manager.tBox[16].set_visible(false)
              manager.tBoxUsed[16] = 1
              newItem("4_24 - food:cherries")
              // if (manager.food[Enum.Food.cherries] > 99) {
              //   manager.food[Enum.Food.cherries] = 99
              // }
              manager.keys = manager.keys - 1
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              this.itemTile[9].set_x(300)
              this.itemTile[9].set_y(420)
              this.itemTile[9].set_visible(true)
              manager.tBox[11].set_visible(false)
              manager.tBoxUsed[11] = 1
              newItem("6_10 - food:chocolate")
              // if (manager.food[Enum.Food.chocolate] > 99) {
              //   manager.food[Enum.Food.chocolate] = 99
              // }
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 9 && manager.east == 10) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBoxUsed[12] = 1
              manager.tBox[12].set_visible(false)
              newItem("9_10 - gold")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 11 && manager.east == 17) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBoxUsed[9] = 1
              manager.tBox[9].set_visible(false)
              newItem("11_17 - item:bombs")
              if (manager.bombs > manager.bombCapacity) {
                manager.bombs = manager.bombCapacity
              }
              newItem("11_17 - gold")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (
              manager.char[0].hitTestObject(manager.bombSis) &&
--
              this.yesFunc()
              manager.fame++
            } else if (manager.north == 14 && manager.east == 21) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.tBoxUsed[7] = 1
              manager.tBox[7].set_visible(false)
              newItem("14_21 - item:bombs")
              if (manager.bombs > manager.bombCapacity) {
                manager.bombs = manager.bombCapacity
              }
              newItem("14_21 - food:apple")
              newItem("14_21 - gold")
              manager.hitMax()
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 4 && manager.east == 26) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              this.weapTile[Enum.Weapon.shadowStaff].set_x(300)
              this.weapTile[Enum.Weapon.shadowStaff].set_y(420)
              this.weapTile[Enum.Weapon.shadowStaff].set_visible(true)
              manager.tBox[15].set_visible(false)
              manager.tBoxUsed[15] = 1
              newItem("4_26 - weapon:shadowStaff")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 18 && manager.east == 23) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              if (manager.weapon[Enum.Weapon.warlockStaff] == 0) {
                this.weapTile[Enum.Weapon.warlockStaff].set_x(300)
                this.weapTile[Enum.Weapon.warlockStaff].set_y(420)
                this.weapTile[Enum.Weapon.warlockStaff].set_visible(
                  true,
                )
                newItem("18_23 - weapon:warlockStaff")
              }
              // else {
              //   newItem("18_23 - gold", 2e3, add)
              // }
              manager.tBox[8].set_visible(false)
              manager.tBoxUsed[8] = 1
              manager.keys = manager.keys - 1
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              this.itemTile[6].set_x(300)
              this.itemTile[6].set_y(420)
              this.itemTile[6].set_visible(true)
              manager.tBox[5].set_visible(false)
              manager.tBoxUsed[5] = 1
              newItem("15_14 - food:carrot")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 9 && manager.east == 23) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.magicTile[Enum.Magic.drain].set_x(300)
              manager.magicTile[Enum.Magic.drain].set_y(420)
              manager.magicTile[Enum.Magic.drain].set_visible(true)
              manager.tBox[13].set_visible(false)
              manager.tBoxUsed[13] = 1
              newItem("9_23 - magic:drain")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 15 && manager.east == 16) {
              manager.messPage = 2
              V.dialogueMess()
              this.enterFunc()
              manager.magicTile[Enum.Magic.ice].set_x(300)
              manager.magicTile[Enum.Magic.ice].set_y(420)
              manager.magicTile[Enum.Magic.ice].set_visible(true)
              manager.loot[Enum.Loot.mStaff] -= 20
              newItem("15_16 - magic:ice")
            } else if (
              manager.north == 11 &&
              manager.east == 18 &&
              manager.magic[Enum.Magic.refresh] == 0
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.magicTile[Enum.Magic.refresh].set_x(300)
              manager.magicTile[Enum.Magic.refresh].set_y(420)
              manager.magicTile[Enum.Magic.refresh].set_visible(true)
              manager.tBox[10].set_visible(false)
              manager.tBoxUsed[10] = 1
              newItem("11_18 - magic:refresh")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (
              manager.north == 11 &&
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              // this.weapTile[Enum.Weapon.sKnife].set_x(300)
              // this.weapTile[Enum.Weapon.sKnife].set_y(420)
              // this.weapTile[Enum.Weapon.sKnife].set_visible(true)
              manager.tBox[6].set_visible(false)
              manager.tBoxUsed[6] = 1
              newItem("13_16 - weapon:sKnife")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (
              manager.north == 13 &&
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              // manager.magicTile[Enum.Magic.weak].set_x(300)
              // manager.magicTile[Enum.Magic.weak].set_y(420)
              // manager.magicTile[Enum.Magic.weak].set_visible(true)
              manager.tBox[4].set_visible(false)
              manager.tBoxUsed[4] = 1
              newItem("13_16 - magic:weak")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 13 && manager.east == 25) {
              console.log("nm")
--
              this.enterFunc()
              // manager.armorTile[Enum.Armor.regenArmor].set_x(300)
              // manager.armorTile[Enum.Armor.regenArmor].set_y(420)
              // manager.armorTile[Enum.Armor.regenArmor].set_visible(
              //   true,
              // )
              manager.tBox[3].set_visible(false)
              manager.tBoxUsed[3] = 1
              newItem("14_19 - armor:regenArmor")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 16 && manager.east == 22) {
              manager.messPage = 2
              newItem("16_22 - gold")
              manager.keys = manager.keys - 1
              V.tBoxMes()
              manager.tBoxUsed[2] = 1
              this.enterFunc()
--
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              manager.magicTile[Enum.Magic.fire].set_x(300)
              manager.magicTile[Enum.Magic.fire].set_y(420)
              manager.magicTile[Enum.Magic.fire].set_visible(true)
              manager.tBox[1].set_visible(false)
              manager.tBoxUsed[1] = 1
              newItem("19_23 - magic:fire")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
            } else if (manager.north == 18 && manager.east == 21) {
              manager.messPage = 2
              V.tBoxMes()
              this.enterFunc()
              this.itemTile[4].set_x(300)
              this.itemTile[4].set_y(420)
              this.itemTile[4].set_visible(true)
              manager.tBox[0].set_visible(false)
              manager.tBoxUsed[0] = 1
              newItem("18_21 - food:gingerBread")
              manager.keys = manager.keys - 1
              manager.tBoxSound.play()
              // if (manager.food[Enum.Food.gingerBread] > 99) {
              //   manager.food[Enum.Food.gingerBread] = 99
--
          manager.inWater == 1 &&
          manager.north == 14 &&
          manager.east == 22
        ) {
          manager.mess.set_text(
            "You found the Ring of Gold!\nFrom now on, you will earn a small amount of\ngold every time you win a battle.",
          )
          manager.fame++
          newItem("item:ring of gold")
        } else if (
          manager.quest[Enum.Quest.rings] > 0 &&
          manager.ring2 == 0 &&
          manager.north == 16 &&
          manager.east == 21
        ) {
          manager.mess.set_text(
            "You found the Ring of Health!\nFrom now on, every step you take will\nwill recover some health.",
          )
          manager.fame++
          newItem("misc:ring of health")
        } else if (manager.quest[Enum.Quest.dig] == 1) {
          manager.mess.set_text("You found a small locket!")
          manager.quest[Enum.Quest.dig] = 2
        } else if (
--
            (manager.north == 12 &&
              manager.east == 12 &&
              manager.headstoneSwitch3 == 0) ||
            (manager.north == 10 &&
              manager.east == 25 &&
              manager.headstoneSwitch4 == 0)
          ) {
            if (manager.north == 18 && manager.east == 24) {
              newItem("18_24 - headstoneSwitch1")
            }
            if (manager.north == 16 && manager.east == 16) {
              newItem("16_16 - headstoneSwitch2")
            }
            if (manager.north == 12 && manager.east == 12) {
              newItem("12_12 - headstoneSwitch3")
            }
            if (manager.north == 10 && manager.east == 25) {
              newItem("10_25 - headstoneSwitch4")
            }
            manager.mess.set_text(
              "You have found one of the Noble Headstones!",
            )
--
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] * 100) +
              " gold and a strawberry.",
          )
          manager.messFin = true
          manager.tBoxUsed[55] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("18_19 - gold")
          manager.removeMBox = true
          manager.tBoxGreen.set_visible(false)
          manager.tBoxSound.play()
        } else if (manager.north == 12 && manager.east == 21) {
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] + 1) +
              " diamonds and 20 bananas.",
          )
          manager.messFin = true
          manager.tBoxUsed[56] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("12_21 - food:banana")
          // // if (manager.food[Enum.Food.banana] > 99) {
          // //   manager.food[Enum.Food.banana] = 99
          // // }
          newItem("12_21 - diamonds")
          manager.removeMBox = true
          manager.tBoxGreen.set_visible(false)
          manager.tBoxSound.play()
        } else if (manager.north == 8 && manager.east == 18) {
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] * 5) +
              " steaks and 25 bombs.",
          )
          manager.messFin = true
          manager.tBoxUsed[57] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("8_18 - item:bombs")
          if (manager.bombs > manager.bombCapacity) {
            manager.bombs = manager.bombCapacity
          }
          newItem("8_18 - food:steak")
          // // if (manager.food[Enum.Food.steak] > 99) {
          // //   manager.food[Enum.Food.steak] = 99
          // // }
          manager.removeMBox = true
--
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] * 100) +
              " gold and 50 cookies!",
          )
          manager.messFin = true
          manager.tBoxUsed[58] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("17_15 - gold")
          newItem("17_15 - food:gingerBread")
          // // if (manager.food[Enum.Food.gingerBread] > 99) {
          // //   manager.food[Enum.Food.gingerBread] = 99
          // // }
          manager.removeMBox = true
--
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] * 100) +
              " gold and 30 strips of jerky!",
          )
          manager.messFin = true
          manager.tBoxUsed[59] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("8_10 - gold")
          newItem("8_10 - food:beefJerky")
          // if (manager.food[Enum.Food.beefJerky] > 99) {
          //   manager.food[Enum.Food.beefJerky] = 99
          // }
          manager.removeMBox = true
--
        } else if (manager.north == 21 && manager.east == 18) {
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] + 1) +
              " diamonds and 20 peppers!",
          )
          manager.messFin = true
          manager.tBoxUsed[60] = 1
          newItem("21_18 - diamonds")
          manager.emeralds = manager.emeralds - 1
          newItem("21_18 - food:peppers")
          // // if (manager.food[Enum.Food.peppers] > 99) {
          // //   manager.food[Enum.Food.peppers] = 99
          // // }
          manager.removeMBox = true
--
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find " +
              f.string(manager.crafts[Enum.Craft.emerald] * 100) +
              " gold and some elixir!",
          )
          manager.messFin = true
          manager.tBoxUsed[61] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("9_25 - gold")
          newItem("9_25 - food:elixir")
          // if (manager.food[Enum.Food.elixir] > 99) {
          //   manager.food[Enum.Food.elixir] = 99
          // }
          manager.removeMBox = true
--
          manager.tBoxSound.play()
        } else if (manager.north == 23 && manager.east == 10) {
          manager.mess.set_text(
            "One of your emeralds fades. The chest opens!\nYou find the legendary Alpha Armor!!!",
          )
          manager.messFin = true
          manager.tBoxUsed[62] = 1
          manager.emeralds = manager.emeralds - 1
          newItem("23_10 - armor:alphaArmor")
          // manager.armorTile[Enum.Armor.alphaArmor].set_x(300)
          // manager.armorTile[Enum.Armor.alphaArmor].set_y(450)
          // manager.armorTile[Enum.Armor.alphaArmor].set_visible(true)
          manager.removeMBox = true
--
          manager.east == 26 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find a bottle of elixir!.",
          )
          manager.messFin = true
          manager.tBoxUsed[53] = 1
          newItem("3_26 - food:elixir")
          manager.removeMBox = true
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
        } else if (
--
          manager.east == 24 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find a dozen gummy bears and 1,000 gold.",
          )
          manager.messFin = true
          manager.tBoxUsed[49] = 1
          newItem("16_24 - food:gummyBears")
          newItem("16_24 - gold")
          manager.removeMBox = true
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
        } else if (
--
          manager.east == 25 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find a dozen steaks and 5 diamonds!",
          )
          manager.messFin = true
          manager.tBoxUsed[48] = 1
          newItem("16_25 - food:steak")
          newItem("16_25 - diamonds")
          manager.removeMBox = true
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
        } else if (
--
          manager.east == 25 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 10 handfuls of gummy bears\nand 50 diamonds!",
          )
          manager.messFin = true
          manager.removeMBox = true
          newItem("12_25 - food:gummyBears")
          manager.tBoxUsed[35] = 1
          newItem("12_25 - diamonds")
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
        } else if (
          manager.north == 18 &&
          manager.east == 15 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 15 Newton apples!\nYou also feel fully refreshed.",
          )
          manager.messFin = true
          manager.removeMBox = true
          newItem("18_15 - food:newtonsApple")
          manager.tBoxUsed[47] = 1
          manager.hp = manager.mxhp
          manager.mp = manager.mxmp
          manager.tBoxBlue.set_visible(false)
--
          manager.east == 25 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 20 strips of beef jerky inside!",
          )
          manager.messFin = true
          manager.removeMBox = true
          newItem("11_25 - food:beefJerky")
          manager.tBoxUsed[28] = 1
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
        } else if (
--
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find some Diamond Armor inside!",
          )
          manager.messFin = true
          manager.removeMBox = true
          // manager.armorTile[Enum.Armor.diamondArmor].set_x(300)
          // manager.armorTile[Enum.Armor.diamondArmor].set_y(470)
          // manager.armorTile[Enum.Armor.diamondArmor].set_visible(true)
          newItem("16_15 - armor:diamondArmor")
          manager.tBoxBlue.set_visible(false)
          manager.tBoxSound.play()
          manager.quest[Enum.Quest.pam] = 16
        } else if (
          manager.north == 17 &&
          manager.east == 22 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 20 diamonds inside.",
          )
          newItem("17_22 - diamonds")
          manager.tBoxUsed[24] = 1
          manager.tBoxBlue.set_visible(false)
          manager.messFin = true
          manager.removeMBox = true
--
          manager.east == 18 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 50 bombs and some chocolate.",
          )
          manager.tBoxUsed[25] = 1
          manager.tBoxBlue.set_visible(false)
          newItem("15_18 - item:bombs")
          // TODO
          // if (manager.bombs > 99) {
          //   manager.bombs = 99
          // }
          newItem("15_18 - food:chocolate")
          manager.messFin = true
          manager.removeMBox = true
          manager.tBoxSound.play()
        } else if (
--
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find the Magic Scroll of Blessing.",
          )
          // manager.magicTile[Enum.Magic.blessing].set_x(300)
          // manager.magicTile[Enum.Magic.blessing].set_y(470)
          // manager.magicTile[Enum.Magic.blessing].set_visible(true)
          newItem("12_12 - magic:blessing")
          manager.tBoxBlue.set_visible(false)
          manager.messFin = true
          manager.removeMBox = true
          manager.tBoxSound.play()
        } else if (
          manager.north == 19 &&
          manager.east == 18 &&
          manager.quest[Enum.Quest.pam] > 14
        ) {
          manager.mess.set_text(
            "The blue crystal shines. The chest opens!\nYou find 3 rubies inside!",
          )
          newItem("19_18 - rubies")
          manager.tBoxUsed[31] = 1
          manager.tBoxBlue.set_visible(false)
          manager.messFin = true
          manager.removeMBox = true
--
              "Pam: If you are able to find a blue flower\nplease bring it to me.",
            )
            manager.messFin = true
          } else if (manager.quest[Enum.Quest.pam] == 2) {
            manager.mess.set_text(
              "Pam: You found one!\nHere, you can have this.\n(She gives you 20 gold coins.)",
            )
            manager.fame++
            newItem("19_20 - gold")
            // manager.gold += 20
            manager.hitMax()
            newQuest("19_20", "pam", 3, false)
            // manager.quest[Enum.Quest.pam] = 3
          } else if (manager.quest[Enum.Quest.pam] == 4) {
            manager.mess.set_text(
              "Pam: You found another one!\nI made these just for you.\n(She gives you 10 gingerbread cookies.)",
            )
            manager.fame++
            newItem("19_20 - food:gingerBread")
            // manager.food[Enum.Food.gingerBread] =
            //   manager.food[Enum.Food.gingerBread] + 10
            manager.hitMax()
            newQuest("19_20", "pam", 5, false)
            // manager.quest[Enum.Quest.pam] = 5
          } else if (manager.quest[Enum.Quest.pam] == 6) {
            manager.mess.set_text(
              "Pam: You found another one!\nYou'll love this.\n(She gives you 5 chocolate bars.)",
            )
            manager.fame++
            newItem("19_20 - food:chocolate")
            // manager.food[Enum.Food.chocolate] =
            //   manager.food[Enum.Food.chocolate] + 5
            manager.hitMax()
            newQuest("19_20", "pam", 7, false)
            // manager.quest[Enum.Quest.pam] = 7
          } else if (manager.quest[Enum.Quest.pam] == 8) {
            manager.mess.set_text(
              "Pam: You found another one!\nI cooked this for you.\n(She gives you 3 juicy steaks.)",
            )
            manager.fame++
            newItem("19_20 - food:steak")
            // manager.food[Enum.Food.steak] =
            //   manager.food[Enum.Food.steak] + 3
            manager.hitMax()
            newQuest("19_20", "pam", 9, false)
            // manager.quest[Enum.Quest.pam] = 9
          } else if (manager.quest[Enum.Quest.pam] == 10) {
            manager.mess.set_text(
              "Pam: You found another one!\nI saved these for you.\n(She gives you 5 peppers and 20 oranges.)",
            )
            manager.fame++
            newItem("19_20 - food:peppers")
            // manager.food[Enum.Food.peppers] =
            //   manager.food[Enum.Food.peppers] + 5
            newItem("19_20 - food:orange")
            // manager.food[Enum.Food.orange] =
            //   manager.food[Enum.Food.orange] + 20
            manager.hitMax()
            newQuest("19_20", "pam", 11, false)
            // manager.quest[Enum.Quest.pam] = 11
          } else if (manager.quest[Enum.Quest.pam] == 12) {
            manager.mess.set_text(
              "Pam: You found a sixth one!\nThat makes a half dozen!\nYou deserve this.\n(She gives you a bottle of holy water.)",
            )
            manager.fame++
            newItem("19_20 - food:holyWater")
            // manager.food[Enum.Food.holyWater] =
            //   manager.food[Enum.Food.holyWater] + 1
            manager.hitMax()
            newQuest("19_20", "pam", 13, false)
--
                _aNewIdentifierName.plus(
                  "Thank you, ",
                  manager.charName.get_text(),
                ),
                "!\nHere, take this.\n(She hands you 25 gold coins.)",
              ),
            )
            manager.quest[Enum.Quest.dig] = 3
            newItem("19_21 - gold")
            manager.hitMax()
            manager.fame++
            manager.messFin = true
          } else if (
--
            manager.mess.set_text(
              "Hurry... I... need... water...\n(press 'F' when standing in water\nto fill the canteen)",
            )
            manager.messFin = true
          } else if (manager.quest[Enum.Quest.canteen] == 2) {
            manager.mess.set_text(
              "Thank you so much!\nHere, you can have this diamond.",
            )
            newItem("12_11 - diamonds")
            manager.fame++
            manager.messFin = true
            // newItem(12,11,'Enum.Quest.canteen',3)
            manager.quest[Enum.Quest.canteen] = 3
--
            manager.mess.set_text(
              "Arc: There's a lock on his cell, and\nthere appears to be a keypad where we can\nenter a code. It appears that there are\nthree digits in the code.",
            )
            manager.messFin = true
          } else if (manager.quest[Enum.Quest.curse] == 10) {
            manager.mess.set_text(
              "Arc: Thanks for saving my son.\nHere, take these gingerbread cookies as\na reward.",
            )
            newItem("13_26 - food:gingerBread")
            // manager.food[Enum.Food.gingerBread] = 99
            manager.messFin = true
          }
        }
--
              )
              manager.skillTile[Enum.Skill.convert].set_x(300)
              manager.skillTile[Enum.Skill.convert].set_y(420)
              manager.skillTile[Enum.Skill.convert].set_visible(true)
              manager.messFin = true
              newQuest("6_12", "geo", 5, false)
              // manager.quest[Enum.Quest.geo] = 5
              manager.fame++
              newItem("6_12 - skill:convert")
              // manager.skills[Enum.Skill.convert] = 1
            }
          } else if (
            manager.quest[Enum.Quest.rings] == 12 &&
--
              if (manager.messPage == 2) {
                // newItem(11,9,'Enum.Quest.warp',null)
                manager.quest[Enum.Quest.warp] = 2
                manager.fame++
                manager.mess.set_text("Here, you have earned this:")
                manager.skillTile[Enum.Skill.warp].set_x(300)
                manager.skillTile[Enum.Skill.warp].set_y(420)
                manager.skillTile[Enum.Skill.warp].set_visible(true)
                newItem("11_9 - skill:warp")
                manager.messFin = true
              }
            } else {
              if (manager.quest[Enum.Quest.warp] == 0) {
--
            manager.quest[Enum.Quest.seeds] == 3 &&
            manager.messPage == 2
          ) {
            manager.mess.set_text(
              "Here, you can have this.\n(He hands you some peppers and oranges.)",
            )
            newQuest("9_22", "seeds", 4, false)
            // manager.quest[Enum.Quest.seeds] = 4
            newItem("9_22 - food:orange")
            // manager.food[Enum.Food.orange] =
            //   manager.food[Enum.Food.orange] + 10
            newItem("9_22 - food:peppers")
            // manager.food[Enum.Food.peppers] =
            //   manager.food[Enum.Food.peppers] + 3
            manager.fame++
            manager.messFin = true
--
          ) {
            if (manager.quest[Enum.Quest.gTree] == 14) {
              manager.fame++
              // newItem(12,9,'Enum.Quest.gTree',null)
              manager.quest[Enum.Quest.gTree]++
              manager.loot[Enum.Loot.sClaw] -= 7
              manager.loot[Enum.Loot.cFang] -= 5
            }
            newItem("item:fire crystal")
            manager.mess.set_text(
              "If you're seeking the Orb of Strength, you'll\nneed to enter the Tomb of the Quarter Hawk.\nTo enter the tomb, place this fire crystal\non the statue south of here.",
            )
            manager.messFin = true
--
            manager.mess.set_text(
              "Desmond: Help me defeat 3 black mambas,\nand I'll teach you a new skill!",
            )
            manager.messFin = true
          } else if (manager.quest[Enum.Quest.isles] == 22) {
            manager.mess.set_text(
              "Desmond: You did it! As I promised:\nDesmond teaches you the Skill of TOUGH.",
            )
            newItem("4_26 - skill:tough")
            // manager.skills[Enum.Skill.tough] = 1
            manager.skillTile[Enum.Skill.tough].set_x(300)
            manager.skillTile[Enum.Skill.tough].set_y(450)
            manager.skillTile[Enum.Skill.tough].set_visible(true)
--
              )
              manager.messFin = true
              manager.loot[Enum.Loot.dScale] -= 3
              manager.loot[Enum.Loot.sFrag] -= 5
              manager.loot[Enum.Loot.fBone] -= 10
              newQuest("20_18", "rings", 14, false)
              // manager.quest[Enum.Quest.rings] = 14
              manager.fame += 2
              newItem("item:ring of skill")
              // manager.ring6 = 1
            }
          } else if (manager.quest[Enum.Quest.rings] >= 14) {
            manager.mess.set_text(
--
        if (
          manager.north == 13 &&
          manager.east == 16 &&
          manager.charBottom[0].hitTestObject(manager.ringEvaIcon)
        ) {
          manager.mess.set_text(
            "You found the Ring of Evasion.\nThis ring will help you dodge a small amount\nof your enemy's attacks.",
          )
          newItem("item:ring of evasion")
          // manager.ring3 = 1
          manager.fame++
          manager.ringEvaIcon.set_visible(false)
          manager.messFin = true
--
            }
          } else {
            if (
              (manager.quest[Enum.Quest.gTree] == 10 &&
                manager.messPage == 5) ||
              manager.quest[Enum.Quest.gTree] == 11
            ) {
              if (manager.quest[Enum.Quest.gTree] == 10) {
                newItem("15_18 - food:beefJerky")
                // newItem(15,18,'Enum.Quest.gTree',null)
                manager.quest[Enum.Quest.gTree] = 11
              }
              manager.mess.set_text(
--
          }
          if (
            (manager.quest[Enum.Quest.bBomb] == 3 &&
              manager.messPage == 2) ||
            manager.quest[Enum.Quest.bBomb] == 4
          ) {
            if (manager.quest[Enum.Quest.bBomb] == 3) {
              manager.fame++
              newItem("craft:bomb")
              newQuest("13_21", "bBomb", 4, false)
              manager.quest[Enum.Quest.bBomb] = 4
              manager.bombCapacity = 99
              manager.hitMax()
--
              "You're gonna have to help us out.\nI'll upgrade your Royal Sword, and you should\nhave no problem at all. Please report back if you\nsucceed.",
            )
            manager.messFin = true
            if (manager.weapon[Enum.Weapon.royalSword] == 2) {
              manager.eStr -= 15
              manager.eSpeed -= 2
            }
            manager.weapon[Enum.Weapon.royalSword] = 0
            newItem("14_18 - weapon:creeperCrusher")
            // manager.weapon[Enum.Weapon.creeperCrusher] = 1
            newQuest("14_18", "bBomb", 12, false)
            // manager.quest[Enum.Quest.bBomb] = 12
          } else if (manager.quest[Enum.Quest.bBomb] == 12) {
--
              "As an added reward, I will now grant\nyou access to our secret tunnel.\nVisit the my wife's garden for a shortcut to Dyce.",
            )
            manager.messFin = true
          } else if (manager.quest[Enum.Quest.gTree] == 24) {
            manager.mess.set_text(
              "You have returned as a hero.\nAs a reward, I give you 1,000 gold\nand 10 Power-Ups!!!.",
            )
            manager.messFin = true
            newItem("14_18 - pup")
            newItem("14_18 - gold")
            manager.hitMax()
            // newItem(14,18,'Enum.Quest.gTree',null)
            manager.quest[Enum.Quest.gTree] = 25
          } else if (
--
              manager.mess.set_text(
                "As a reward for your service, I'd like\nto upgrade your Royal Armor.",
              )
              if (manager.armor[Enum.Armor.royalArmor] == 2) {
                manager.eHealth -= 110
                manager.eSpeed += 1
              }
              manager.armor[Enum.Armor.royalArmor] = 0
              newItem("13_17 - armor:nobleArmor")
              // manager.armor[Enum.Armor.nobleArmor] = 1
            }
            manager.messFin = true
            newQuest("13_17", "dream", 15, false)
--
                    "Bobbi: You saved me!!!\nThank you so much, ",
                    manager.charName.get_text(),
                  ),
                  "!\n",
                ),
              )
              if (manager.quest[Enum.Quest.oMan] == 21) {
                newQuest("17_19", "oMan", 22, false)
                newItem("misc:bobbisPendant")
                // manager.quest[Enum.Quest.oMan] = 22
                manager.mess.set_text(
                  _aNewIdentifierName.plus(
                    _aNewIdentifierName.plus(
--
            )
          } else if (
            manager.quest[Enum.Quest.gTree] == 5 &&
            manager.messPage == 2
          ) {
            manager.mess.set_text(
              "Here, take this reward of 50 gold.",
            )
            newItem("21_20 - gold")
            manager.goldDisplay.set_text("Gold: " + manager.gold)
            manager.goldDisplay.setTextFormat(manager.goldFormat)
            manager.fame += 5
          } else if (
