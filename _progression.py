from typing import NotRequired, TypedDict


class RoomCoordinates(TypedDict):
  north: int
  east: int


class ProgressionNode(TypedDict):
  room: RoomCoordinates
  receive: NotRequired[list[str]]
  requires: NotRequired[list[list[str]]]
  info: NotRequired[str]


PROG: list[ProgressionNode] = [
  {
    "room": {"north": 20, "east": 20},
    "requires": [[]],
    "receive": [
      "skill:dig",
      "skill:kick",
      "skill:flee",
      "skill:swap",
      "skill:firewall",
      "skill:firewall.1",
      "skill:halo",
      "item:aurastone",
      "item:key",
      "item:gold",
      "item:dragon scale",
      "item:cotton thread",
      "item:shadow crest",
      "item:orc coin",
      "item:blue crystal",
    ],
    "info": """can be got anywhere
manager.correct - manager.wrong > 9 = dig
manager.correct - manager.wrong > 49 = kick
manager.correct - manager.wrong > 149 = flee
manager.correct - manager.wrong > 300 = swap
manager.correct - manager.wrong > 500 = firewall
  can be leveled up without getting it first and doesn't give it to do so so the levels are separate
manager.correct - manager.wrong > 800 = halo
""",
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [[]],
    "receive": [
      "item:bear tooth",
      "item:boar tusk",
      "item:cobra fang",
      "item:emerald",
      "item:fire crystal",
      "item:funny bone",
      "item:gator skin",
      "item:golden feather",
      "item:kings crest",
      "item:mage staff",
      "item:mages hat",
      "item:minotaur horn",
      "item:ring of evasion",
      "item:scorpion claw",
      "item:shark tooth",
      "item:slamstone",
      "item:steel fragment",
      "item:tentacle",
      "item:troll wristband",
      "item:venom",
      "item:viking horn",
      "item:void ash",
      "item:wolf pelt",
    ],
    "info": """add to correct locations later
""",
  },
  {"room": {"north": 20, "east": 20}, "receive": ["spawnpoint"]},
  {
    "room": {"north": 15, "east": 21},
    "requires": [["entrance.west0"]],
    "receive": ["food:banana#1"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:venom#1", "???"]],
    "receive": ["food:orange#1"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["weapon:club"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["weapon:dagger"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["weapon:sword"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["armour:vest"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["armour:magic robe"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["armour:iron armour"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:apple#inf"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:honey#inf"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:grapes#inf"],
  },
  {"room": {"north": 18, "east": 20}, "info": "warp skill warp point"},
  {
    "room": {"north": 19, "east": 21},
    "requires": [["skill:dig"]],
    "receive": ["item:gold#25"],
  },
  {
    "room": {"north": 14, "east": 19},
    "requires": [["item:troll wristband#1", "entrance.north0"]],
    "receive": ["item:broken alpha club#1"],
  },
  {"room": {"north": 12, "east": 19}, "info": "warp skill warp point"},
  {
    "room": {"north": 13, "east": 16},
    "requires": [["item:key#1", "entrance.west0"]],
    "receive": ["weapon:survival knife"],
  },
  {"room": {"north": 14, "east": 16}, "info": "warp skill warp point"},
  {
    "room": {"north": 15, "east": 16},
    "requires": [["permit:bomb", "???"]],
    "receive": ["magic:ice"],
  },
  {
    "room": {"north": 13, "east": 13},
    "requires": [["armour:alpha armour", "???"]],
    "receive": ["armour:alpha armour.+inf"],
  },
  {
    "room": {"north": 11, "east": 13},
    "requires": [["item:mage staff#1"]],
    "receive": ["food:blueberries#1"],
  },
  {
    "room": {"north": 11, "east": 12},
    "requires": [["item:gold#100"]],
    "receive": ["food:sunflower seed#1"],
  },
  {
    "room": {"north": 12, "east": 12},
    "requires": [["quest:rings.1", "entrance.west0"]],
    "receive": ["misc:headstone 2"],
  },
  {"room": {"north": 10, "east": 12}, "info": "warp skill warp point"},
  {"room": {"north": 12, "east": 9}, "receive": ["spawnpoint"]},
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["food:carrot"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["food:beef jerky"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["food:cherry"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["weapon:survival knife"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["weapon:warlock staff"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["weapon:sun sword"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["armour:sun armour"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["armour:speed vest"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:venom"]],
    "receive": ["food:orange"],
  },
  {"room": {"north": 11, "east": 9}, "receive": ["quest:headstone"]},
  {
    "room": {"north": 11, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["magic:weak"],
  },
  {
    "room": {"north": 11, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["magic:refresh"],
  },
  {
    "room": {"north": 11, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["magic:lightning"],
  },
  {
    "room": {"north": 11, "east": 9},
    "requires": [["item:wolf pelt"]],
    "receive": ["item:gold#22"],
  },
  {
    "room": {"north": 5, "east": 9},
    "requires": [
      ["item:minotaur horn", "entrance.north0"],
      ["item:minotaur horn", "entrance.east0"],
    ],
    "receive": ["item:broken alpha axe#1"],
  },
  {
    "room": {"north": 8, "east": 14},
    "requires": [["item:shark tooth#30", "item:gold#800", "skill:tough"]],
    "receive": ["skill:tough.+1"],
  },
  {"room": {"north": 10, "east": 16}, "info": "warp skill warp point"},
  {
    "room": {"north": 9, "east": 16},
    "requires": [["item:gator skin#1"]],
    "receive": ["item:gold#23"],
  },
  {
    "room": {"north": 4, "east": 17},
    "requires": [["weapon:random axe", "???"]],
    "receive": ["weapon:random axe.+1"],
  },
  {"room": {"north": 8, "east": 17}, "receive": ["misc:green secret code"]},
  {
    "room": {"north": 11, "east": 17},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["item:bomb#8", "item:gold#200"],
  },
  {
    "room": {"north": 7, "east": 18},
    "requires": [["item:slamstone#1", "skill:reveal"]],
    "receive": ["skill:reveal.+1"],
  },
  {
    "room": {"north": 7, "east": 25},
    "requires": [["magic:fire.2"]],
    "receive": ["state:lit torch 2"],
  },
  {
    "room": {"north": 8, "east": 21},
    "requires": [["magic:fire.2"]],
    "receive": ["state:lit torch 1"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["entrance.south0", "item:gold"]],
    "receive": ["food:chocolate"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["entrance.south0", "item:gold"]],
    "receive": ["food:steak"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["entrance.south0", "item:gold"]],
    "receive": ["food:peppers"],
  },
  {
    "room": {"north": 10, "east": 22},
    "requires": [
      [
        "entrance.south0",
        "item:alpha scepter#1",
        "item:dragon scale#5",
        "skill:craft",
      ],
      [
        "entrance.south1",
        "item:alpha scepter#1",
        "item:dragon scale#5",
        "skill:craft",
        "permit:bomb.2",
      ],
    ],
    "receive": ["craft:elixir"],
  },
  {
    "room": {"north": 10, "east": 25},
    "requires": [["quest:rings.1"]],
    "receive": ["misc:headstone 3"],
  },
  {"room": {"north": 11, "east": 24}, "info": "warp skill warp point"},
  {
    "room": {"north": 11, "east": 22},
    "requires": [["item:shark tooth#10", "skill:craft"]],
    "receive": ["craft:emerald"],
  },
  {
    "room": {"north": 12, "east": 25},
    "requires": [["item:shark tooth#10", "skill:craft"]],
    "receive": ["food:gummy bear#10", "item:diamonds#50"],
  },
  {
    "room": {"north": 13, "east": 25},
    "requires": [["item:mages hat#1", "misc:magic only resist bypass"]],
    "receive": ["item:alpha scepter#1"],
  },
  {"room": {"north": 14, "east": 25}, "receive": ["misc:three part code part 1"]},
  {"room": {"north": 14, "east": 24}, "receive": ["misc:three part code part 2"]},
  {"room": {"north": 13, "east": 24}, "receive": ["misc:three part code part 3"]},
  {
    "room": {"north": 13, "east": 26},
    "requires": [
      [
        "misc:three part code part 1",
        "misc:three part code part 2",
        "misc:three part code part 3",
      ]
    ],
    "receive": ["???"],
  },
  {"room": {"north": 11, "east": 26}, "receive": ["misc:stomp code"]},
  {
    "room": {"north": 18, "east": 25},
    "requires": [["skill:medic.1", "item:cobra fang#5"]],
    "receive": ["skill:medic.2"],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["skill:medic.2", "item:orc coin#20", "item:mage staff#10"]],
    "receive": ["skill:medic.3"],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["skill:medic.3", "item:dragon scale#10", "item:gator skin#10"]],
    "receive": ["skill:medic.4"],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["skill:medic.4", "item:kings crest#10", "item:alpha axe#5"]],
    "receive": ["skill:medic.5"],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [
      ["skill:medic.5", "item:golden feather#3", "item:alpha scepter#5"]
    ],
    "receive": ["skill:medic.6"],
  },
  {
    "room": {"north": 18, "east": 24},
    "requires": [["quest:rings.1"]],
    "receive": ["misc:headstone 4"],
  },
  {
    "room": {"north": 21, "east": 23},
    "requires": [["skill:dig"]],
    "receive": ["item:diamonds#1"],
  },
  {
    "room": {"north": 21, "east": 22},
    "requires": [
      ["item:ring of gold", "item:troll wristband#5", "item:gator skin#2"]
    ],
    "receive": ["craft:ring of gold"],
  },
  {
    "room": {"north": 20, "east": 22},
    "requires": [["item:gold#500"]],
    "receive": ["item:ruby#1"],
  },
  {
    "room": {"north": 20, "east": 23},
    "requires": [["skill:reveal", "entrance.east0"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 19, "east": 22},
    "requires": [["item:broken alpha axe#5"]],
    "receive": ["skill:reveal"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["quest:dig.3", "item:bear tooth#1"]],
    "receive": ["item:gold#18"],
  },
  {"room": {"north": 19, "east": 20}, "receive": ["quest:pam.1"]},
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["magic:slow"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["magic:heal"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["magic:blast"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["food:honey#10"]],
    "receive": ["magic:crush"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:boar tusk#1"]],
    "receive": ["item:gold#20"],
  },
  {
    "room": {"north": 20, "east": 18},
    "requires": [["quest:rings.11"]],
    "receive": ["quest:rings.12"],
  },
  {
    "room": {"north": 21, "east": 18},
    "requires": [["item:emerald#1"]],
    "receive": ["item:diamonds#2", "food:peppers#20"],
  },
  {
    "room": {"north": 21, "east": 17},
    "requires": [["item:aurastone#1", "item:gold#500"]],
    "receive": ["item:ruby#1"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.1", "item:dragon scale#5", "item:medallion#3"]],
    "receive": ["skill:firewall.2"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.2", "item:dragon scale#10", "item:medallion#6"]
    ],
    "receive": ["skill:firewall.3"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.3", "item:dragon scale#15", "item:medallion#9"]
    ],
    "receive": ["skill:firewall.4"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.4", "item:dragon scale#20", "item:medallion#12"]
    ],
    "receive": ["skill:firewall.5"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.5", "item:dragon scale#25", "item:medallion#15"]
    ],
    "receive": ["skill:firewall.6"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.6", "item:dragon scale#30", "item:medallion#18"]
    ],
    "receive": ["skill:firewall.7"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.7", "item:dragon scale#35", "item:medallion#21"]
    ],
    "receive": ["skill:firewall.8"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.8", "item:dragon scale#40", "item:medallion#24"]
    ],
    "receive": ["skill:firewall.9"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [
      ["skill:firewall.9", "item:dragon scale#45", "item:medallion#27"]
    ],
    "receive": ["skill:firewall.10"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#20"]],
    "receive": ["item:ruby#1"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#3"]],
    "receive": ["19_15 - skill:hint"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#30"]],
    "receive": ["skill:fear"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#200"]],
    "receive": ["skill:shield"],
  },
  {
    "room": {"north": 16, "east": 16},
    "requires": [["quest:rings.1"]],
    "receive": ["misc:headstone 1"],
  },
  {
    "room": {"north": 18, "east": 13},
    "requires": [
      ["item:cotton thread#10", "item:shadow crest#5", "skill:reveal"]
    ],
    "receive": ["misc:max bombs.149"],
  },
  {"room": {"north": 19, "east": 12}, "info": "warp skill warp point"},
  {
    "room": {"north": 23, "east": 10},
    "requires": [["item:key#1"]],
    "receive": ["food:newton apple#3", "item:diamonds#3"],
  },
  {
    "room": {"north": 24, "east": 11},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["weapon:bane blade"],
  },
  {
    "room": {"north": 17, "east": 10},
    "requires": [["item:void ash#6"]],
    "receive": ["food:gummy bear#5"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["weapon:bane blade", "skill:reveal"]],
    "receive": ["quest:alpha blade.1"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:orange"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:gingerbread cookie"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:strawberry"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [
      ["item:shark tooth#5", "item:viking horn#5", "item:tentacle#5"]
    ],
    "receive": ["craft:newton apple"],
  },
  {
    "room": {"north": 11, "east": 15},
    "requires": [["skill:craft", "item:troll wristband#5", "item:wolf pelt#2"]],
    "receive": ["craft:key"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [[]],
    "receive": ["quest:gTree.1"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["entrance.south0"]],
    "receive": ["quest:bBomb.1"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [[]],
    "receive": ["quest:dig.1"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["skill:dig", "quest:dig.1"]],
    "receive": ["quest:dig.2"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["quest:dig.2"]],
    "receive": ["quest:dig.3", "item:gold#25"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["food:honey#10"]],
    "receive": ["magic:crush"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["quest:gTree.1"]],
    "receive": ["quest:gTree.2"],
  },
  {
    "room": {"north": 18, "east": 22},
    "requires": [["quest:gTree.2"]],
    "receive": ["quest:gTree.3"],
    # TODO
    "info": "also unblocks the path here add info to other place too",
  },
  {
    "room": {"north": 19, "east": 23},
    "requires": [["item:bear tooth#15", "quest:gTree.3"]],
    "receive": ["quest:gTree.4"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [["quest:gTree.4"]],
    "receive": ["quest:gTree.5"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["quest:gTree.5"]],
    "receive": ["quest:gTree.6", "item:gold#50"],
  },
  {
    "room": {"north": 15, "east": 23},
    "requires": [["quest:pam.1", "skill:dig"]],
    "receive": ["quest:pam.2"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.2"]],
    "receive": ["quest:pam.3", "item:gold#20"],
  },
  {
    "room": {"north": 12, "east": 20},
    "requires": [["quest:pam.3"]],
    "receive": ["quest:pam.4"],
    # TODO make sure to show all req pam also req skill dig
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.4"]],
    "receive": ["quest:pam.5", "food:gingerbread cookie#10"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:gTree.7"]],
    "receive": ["quest:gTree.8"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:gTree.8"]],
    "receive": ["quest:gTree.9"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [[]],
    "receive": ["quest:oMan.1", "misc:old pendant"],
  },
  {
    "room": {"north": 21, "east": 21},
    "requires": [["food:honey#5", "item:venom#1"]],
    "receive": ["skill:craft"],
  },
  {
    "room": {"north": 16, "east": 14},
    "requires": [["quest:gTree.9"]],
    "receive": ["quest:gTree.10"],
  },
  {
    "room": {"north": 15, "east": 18},
    "requires": [["quest:gTree.10"]],
    "receive": ["quest:gTree.11", "food:beef jerky#3"],
  },
  {
    "room": {"north": 13, "east": 21},
    "requires": [["quest:bBomb.1", "entrance.south0"]],
    "receive": ["quest:bBomb.2"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["quest:bBomb.2"]],
    "receive": ["quest:bBomb.3"],
    "info": "sable broke here once but now working, unsure why",
  },
  {
    "room": {"north": 13, "east": 21},
    "requires": [["quest:bBomb.3", "entrance.south0"]],
    "receive": ["quest:bBomb.4", "item:bomb#15", "permit:bomb"],
    "info": """bomb active here so find ui update code here
[ACCESS SET] Key: quest"1" was set to: 4 from 3 bBomb Error
at Object.set (http://127.0.0.1:1533/MathQuest/MathQuest.js:19993:15)
at V.dialogueMess (http://127.0.0.1:1533/MathQuest/MathQuest.js:59689:47)
at _createObject.dialogue (http://127.0.0.1:1533/MathQuest/MathQuest.js:31370:13)
at _createObject.messEnter (http://127.0.0.1:1533/MathQuest/MathQuest.js:31788:18)
at Qr.cllosureHandler [as callback] (http://127.0.0.1:1533/MathQuest/MathQuest.js:257:43)
at Jh.__dispatchEvent (http://127.0.0.1:1533/MathQuest/MathQuest.js:1617:37)
at Jh.__dispatch (http://127.0.0.1:1533/MathQuest/MathQuest.js:2275:55)
at Jh.__dispatchStack (http://127.0.0.1:1533/MathQuest/MathQuest.js:99926:26)
at Jh.__onKey (http://127.0.0.1:1533/MathQuest/MathQuest.js:100517:18)
at Jh.onKeyDown (http://127.0.0.1:1533/MathQuest/MathQuest.js:99147:18)
""",
  },
  {
    "room": {"north": 10, "east": 17},
    "requires": [["quest:pam.5"]],
    "receive": ["quest:pam.6"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.6"]],
    "receive": ["quest:pam.7", "food:chocolate#5"],
  },
  {
    "room": {"north": 10, "east": 19},
    "requires": [["quest:gTree.11"]],
    "receive": ["quest:gTree.12", "misc:orb of peace"],
  },
  {
    "room": {"north": 15, "east": 18},
    "requires": [["quest:gTree.12"]],
    "receive": ["quest:gTree.13"],
  },
  {
    "room": {"north": 12, "east": 14},
    "requires": [["quest:bBomb.4"]],
    "receive": ["quest:bBomb.5"],
    "info": "fix warp zone around here they appear to be incorrect",
  },
  {
    "room": {"north": 9, "east": 11},
    "requires": [["quest:pam.7", "entrance.south1"]],
    "receive": ["quest:pam.8"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["quest:gTree.13"]],
    "receive": ["quest:gTree.14"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["quest:gTree.14", "item:scorpion claw#7", "item:cobra fang#5"]],
    "receive": ["quest:gTree.15", "misc:fire crystal"],
  },
  {
    "room": {"north": 11, "east": 9},
    "requires": [["entrance.north0"], ["entrance.east1"]],
    "receive": ["quest:warp.1"],
  },
  {
    "room": {"north": 12, "east": 11},
    "requires": [["entrance.west0"], ["entrance.south0"]],
    "receive": ["quest:canteen.1"],
  },
  {
    "room": {"north": 8, "east": 9},
    "requires": [["misc:fire crystal"]],
    "receive": [],
    "info": """289 374
MathQuest.js:42502 remove listeners
MathQuest.js:31398 enterHandlertrue
MathQuest.js:111001 [ER DEBUG] Transition initiated. From room: 8,9 at position X/Y: 350,300
MathQuest.js:111037 [ER DEBUG] Checking redirection for vanilla move path key: 8_9_7_9
MathQuest.js:111157 [ER DEBUG] No randomizer override entry for key [8_9_7_9]. Retaining game defaults.
MathQuest.js:31309 0 0 0 0
MathQuest.js:42550 add listeners""",
  },
  {
    "room": {"north": 7, "east": 11},
    "requires": [["quest:gTree.15"]],
    "receive": ["quest:gTree.16", "flag:7_11 boss dead"],
  },
  {
    "room": {"north": 7, "east": 10},
    "requires": [["quest:gTree.16", "permit:bomb", "!flag:7_11 boss dead"]],
    # TODO
    "receive": ["quest:gTree.17"],
    "info": "forgot to add permit:bomb to above, do so later",
  },
  {
    "room": {"north": 15, "east": 18},
    "requires": [["quest:gTree.17"]],
    # TODO
    "receive": ["quest:gTree.18", "permit:shadowsoul entrance"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["entrance.south0"]],
    "receive": ["quest:seeds.1"],
  },
  {
    "room": {"north": 6, "east": 23},
    "requires": [[]],
    "receive": [],
    "info": "how show the warp requiring this",
  },
  {
    "room": {"north": 5, "east": 24},
    "requires": [["quest:gTree.18"]],
    "receive": ["quest:gTree.19", "food:holy water#1"],
  },
  {
    "room": {"north": 5, "east": 24},
    "requires": [["quest:gTree.19"]],
    "receive": ["quest:gTree.20"],
  },
  {
    "room": {"north": 15, "east": 18},
    "requires": [["quest:gTree.20"]],
    "receive": ["quest:gTree.21"],
  },
  {
    "room": {"north": 16, "east": 14},
    "requires": [["quest:gTree.21"]],
    "receive": ["quest:gTree.22"],
    "info": "passage up now available",
  },
  {
    "room": {"north": 24, "east": 9},
    "requires": [["quest:gTree.22"]],
    "receive": ["quest:gTree.23", "flag:final boss dead"],
  },
  {
    "room": {"north": 24, "east": 9},
    "requires": [["quest:gTree.23"]],
    "receive": ["quest:gTree.24"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:gTree.24"]],
    "receive": ["quest:gTree.25", "misc:power up#10", "item:gold#1000"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:gTree.25"]],
    "receive": ["quest:aSword.1"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:aSword.1", "weapon:bane blade"]],
    "receive": ["quest:aSword.2"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.2", "skill:reveal"]],
    "receive": ["quest:aSword.3"],
  },
  {
    "room": {"north": 15, "east": 24},
    "requires": [["quest:oMan.1", "misc:old pendant"]],
    "receive": ["quest:oMan.2"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [["quest:oMan.2"]],
    "receive": ["quest:oMan.3"],
  },
  {
    "room": {"north": 11, "east": 21},
    "requires": [["quest:oMan.3"]],
    "receive": ["quest:oMan.4"],
  },
  {
    "room": {"north": 10, "east": 15},
    "requires": [["quest:oMan.4"]],
    "receive": ["quest:oMan.5"],
  },
  {
    "room": {"north": 12, "east": 11},
    "requires": [["quest:canteen.2"]],
    "receive": ["quest:canteen.3", "item:diamonds#1"],
  },
  {"room": {"north": 14, "east": 22}, "requires": [[]], "receive": ["quest:rings.1"]},
  {
    "room": {"north": 14, "east": 22},
    "requires": [["quest:rings.1", "skill:dig"]],
    "receive": ["item:ring of gold"],
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [["quest:rings.1", "item:ring of gold"]],
    "receive": ["quest:rings.2"],
  },
  {
    "room": {"north": 16, "east": 21},
    "requires": [["skill:dig", "quest:rings.1"]],
    "receive": ["item:ring of health"],
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [["item:ring of gold", "item:ring of health", "quest:rings.1"]],
    "receive": ["quest:rings.3"],
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [
      [
        "item:ring of gold",
        "item:ring of health",
        "item:ring of evasion",
        "quest:rings.1",
      ]
    ],
    "receive": ["quest:rings.4"],
  },
  {
    "room": {"north": 13, "east": 16},
    "requires": [["quest:rings.1", "entrance.south0", "permit:bomb"]],
    "receive": ["item:ring of evasion"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [
      [
        "quest:warp.1",
        "misc:headstone 1",
        "misc:headstone 2",
        "misc:headstone 3",
        "misc:headstone 4",
      ]
    ],
    "receive": ["quest:warp.2", "skill:warp"],
  },
  {
    "room": {"north": 13, "east": 21},
    "requires": [["quest:bBomb.5"]],
    "receive": ["quest:bBomb.6", "permit:volcano"],
  },
  {
    "room": {"north": 17, "east": 17},
    "requires": [["quest:bBomb.6"]],
    "receive": ["quest:bBomb.7"],
  },
  {
    "room": {"north": 20, "east": 18},
    "requires": [["quest:bBomb.7"]],
    "receive": ["quest:bBomb.8"],
  },
  {
    "room": {"north": 13, "east": 21},
    "requires": [["quest:bBomb.8"]],
    "receive": ["quest:bBomb.9", "permit:bomb.2"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.8"]],
    "receive": ["quest:pam.9"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [["quest:seeds.1"]],
    "receive": ["quest:seeds.2"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [["quest:seeds.2", "item:orc coin#20"]],
    "receive": ["quest:seeds.3"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["quest:seeds.3", "entrance.south0"]],
    "receive": ["quest:seeds.4", "food:orange#10", "food:pepper#3"],
  },
  {
    "room": {"north": 11, "east": 11},
    "requires": [
      ["quest:rings.4", "entrance.north0"],
      ["quest:rings.4", "entrance.west0"],
    ],
    "receive": ["quest:rings.5"],
  },
  {
    "room": {"north": 11, "east": 11},
    "requires": [
      ["quest:rings.5"],
    ],
    "receive": ["quest:rings.6", "item:ring of poison"],
    "info": "can be anywhere in desert but this loc required for .5 so best to put it here",
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [
      [
        "item:ring of gold",
        "item:ring of health",
        "item:ring of evasion",
        "item:ring of poison",
        "quest:rings.1",
      ]
    ],
    "receive": ["quest:rings.7"],
  },
  {
    "room": {"north": 16, "east": 15},
    "requires": [["quest:pam.9", "skill:dig"]],
    "receive": ["quest:pam.10"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.10"]],
    "receive": ["quest:pam.11", "food:peper#5", "food:orange#20"],
  },
  {
    "room": {"north": 15, "east": 16},
    "requires": [["quest:rings.7", "permit:bomb"]],
    "receive": ["quest:rings.8"],
  },
  {
    "room": {"north": 15, "east": 16},
    "requires": [["quest:rings.8"]],
    "receive": ["item:ring of magic", "quest:rings.9"],
    "info": "doesn't require lv3 fire but using lv3 fire doesn't require as much luck but if not it will spawn eventually",
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [["quest:rings.9"]],
    "receive": ["quest:rings.10"],
  },
  {
    "room": {"north": 19, "east": 18},
    "requires": [["quest:rings.10"]],
    "receive": ["quest:rings.11"],
  },
  {
    "room": {"north": 20, "east": 18},
    "requires": [
      [
        "quest:rings.13",
        "item:steel fragment#5",
        "item:dragon scale#3",
        "item:funny bone#10",
        "?misc:geomana",
      ]
    ],
    "receive": ["quest:rings.14"],
  },
  {"room": {"north": 6, "east": 12}, "requires": [[]], "receive": ["quest:geo.1"]},
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:geo.1", "item:quartz geode#5"]],
    "receive": ["quest:geo.2"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:geo.2"]],
    "receive": ["quest:geo.3"],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["quest:geo.3"]],
    "receive": ["quest:geo.4"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:geo.4"]],
    "receive": ["quest:geo.5", "skill:convert"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:rings.12", "quest:geo.5", "item:gold#1000"]],
    "receive": ["quest:rings.13", "?misc:geomana"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [[]],
    "receive": ["item:medallion"],
    "info": "add reqs later",
  },
  {
    "room": {"north": 13, "east": 14},
    "requires": [
      ["magic:fire.3?", "quest:?", "entrance.east0"],
      ["magic:fire.3?", "quest:?", "entrance.north0", "permit:bomb"],
    ],
    "receive": ["???"],
  },
  # TODO start of all chests remove dupes when done
  {
    "room": {"north": 18, "east": 20},
    "requires": [["item:key"]],
    "receive": ["item:gold#30"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#100"],
    "info": "does not give a strawberry and gp is 100*level of craft emerald",
  },
  {
    "room": {"north": 17, "east": 20},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#200", "food:beef jerky#5"],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["skill:reveal", "permit:bomb"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["item:gold#300", "item:bomb#10", "food:banana#5"],
  },
  {
    "room": {"north": 14, "east": 19},
    "requires": [["item:key#1", "entrance.south0"]],
    "receive": ["armour:regen armour"],
  },
  {
    "room": {"north": 11, "east": 19},
    "requires": [["item:key#1", "entrance.south2"]],
    "receive": ["food:sunflower seed#1", "food:strawberry#1"],
  },
  {
    "room": {"north": 8, "east": 18},
    "requires": [["item:emerald#1", "entrance.north1"]],
    "receive": ["item:bomb#25", "food:steak#5"],
  },
  {
    "room": {"north": 11, "east": 18},
    "requires": [["item:key#1"]],
    "receive": ["magic:refresh#1"],
  },
  {
    "room": {"north": 15, "east": 18},
    "requires": [["misc:blue crystal#1", "permit:bomb.2", "quest:gTree.?"]],
    "receive": ["food:chocolate#20", "item:bomb#50"],
  },
  {
    "room": {"north": 19, "east": 18},
    "requires": [["item:blue crystal#1"]],
    "receive": ["item:rubies#3"],
  },
  {
    "room": {"north": 21, "east": 18},
    "requires": [["item:emerald#1"]],
    "receive": ["item:diamonds#2", "food:pepper#30"],
    "info": "30 not 20",
  },
  {
    "room": {"north": 19, "east": 17},
    "requires": [
      ["skill:reveal", "entrance.south0"],
      ["skill:reveal", "entrance.east0"],
    ],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 18, "east": 17},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#1000"],
  },
  {
    "room": {"north": 13, "east": 16},
    "requires": [["item:key#1", "entrance.south0"]],
    "receive": ["magic:weak"],
  },
  {
    "room": {"north": 17, "east": 16},
    "requires": [["item:key#1"]],
    "receive": ["item:diamonds#5"],
  },
  {
    "room": {"north": 18, "east": 15},
    "requires": [["misc:blue crystal"]],
    "receive": ["food:newton apple#15"],
    "info": "fill refresh too",
  },
  {
    "room": {"north": 17, "east": 15},
    "requires": [["item:emerald#1"]],
    "receive": ["item:gold#100", "food:gingerbread cookie#50"],
  },
  {
    "room": {"north": 16, "east": 15},
    "requires": [["misc:blue crystal#1"]],
    "receive": ["armour:diamonds armour", "quest:pam.16"],
  },
  {
    "room": {"north": 14, "east": 15},
    "requires": [["item:key#1"]],
    "receive": ["food:orange#12"],
  },
  {
    "room": {"north": 9, "east": 15},
    "requires": [["item:key#1"]],
    "receive": ["armour:phantom coat"],
  },
  {
    "room": {"north": 5, "east": 15},
    "requires": [["skill:reveal"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 14, "east": 14},
    "requires": [["skill:reveal"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 15, "east": 14},
    "requires": [["item:key#1", "entrance.east0"], ["item:key#1", "permit:bomb"]],
    "receive": ["food:carrot#5"],
  },
  {
    "room": {"north": 23, "east": 10},
    "requires": [["item:emerald#1"]],
    "receive": ["armour:alpha armour"],
  },
  {
    "room": {"north": 23, "east": 10},
    "requires": [["item:key#1"]],
    "receive": ["item:diamonds#5", "food:newton apple#2"],
    "info": "2 not 3",
  },
  {
    "room": {"north": 21, "east": 11},
    "requires": [["item:key#1", "entrance.north0"]],
    "receive": ["food:gummy bear#5"],
  },
  {
    "room": {"north": 23, "east": 13},
    "requires": [["skill:reveal"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 24, "east": 14},
    "requires": [["item:key#1"]],
    "receive": ["armour:grim gear"],
  },
  {
    "room": {"north": 10, "east": 13},
    "requires": [["permit:bomb", "item:gold#500", "skill:reveal"]],
    "receive": ["misc:ninja"],
  },
  {
    "room": {"north": 10, "east": 13},
    "requires": [["item:emerald#1"]],
    "receive": [
      "item:gold#1",
      "item:diamonds#1",
      "item:aurastone#1",
      "item:slamstone#1",
      "food:elixir#1",
      "food:holy water#1",
    ],
  },
  {
    "room": {"north": 9, "east": 13},
    "requires": [["item:key#1"]],
    "receive": ["item:bomb#10"],
    "info": "chest respawns on room reentry",
  },
  {
    "room": {"north": 6, "east": 13},
    "requires": [["item:key#1"]],
    "receive": ["food:grape#5", "food:strawberry#1"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["item:key#1"]],
    "receive": ["item:quartz geode#2"],
  },
  {
    "room": {"north": 12, "east": 12},
    "requires": [
      ["misc:blue crystal#1", "entrance.east1"],
      ["misc:blue crystal#1", "entrance.south0"],
    ],
    "receive": ["magic:blessing"],
  },
  {
    "room": {"north": 8, "east": 10},
    "requires": [
      ["skill:reveal", "entrance.east0"],
      ["skill:reveal", "entrance.west0"],
      ["skill:reveal", "entrance.north0"],
    ],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 8, "east": 10},
    "requires": [
      ["item:emerald#1", "entrance.north1"],
      ["item:emerald#1", "entrance.east1"],
      ["item:emerald#1", "entrance.east2"],
    ],
    "receive": ["item:gold#100", "food:beef jerky#30"],
    "info": "gold not fixed",
  },
  {
    "room": {"north": 9, "east": 10},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["item:gold#750"],
  },
  {
    "room": {"north": 10, "east": 9},
    "requires": [["item:key#1", "permit:bomb.2"]],
    "receive": ["food:steak#30"],
  },
  {
    "room": {"north": 6, "east": 10},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["food:chocolate#3"],
  },
  {
    "room": {"north": 18, "east": 21},
    "requires": [["item:key#1"]],
    "receive": ["item:gimgerbread cookie#5"],
  },
  {
    "room": {"north": 15, "east": 21},
    "requires": [["item:key#1", "entrance.south0"]],
    "receive": ["item:gold#0", "item:bomb#5"],
    "info": "gold not fixed",
  },
  {
    "room": {"north": 14, "east": 21},
    "requires": [
      ["item:key#1", "entrance.north0"],
      ["item:key#1", "permit:bomb"],
    ],
    "receive": ["item:gold#100", "item:bomb#12", "food:apple#30"],
  },
  {
    "room": {"north": 12, "east": 21},
    "requires": [["item:emerald#1", "permit:bomb"]],
    "receive": ["item:diamonds#2", "food:banana#20"],
  },
  {
    "room": {"north": 11, "east": 21},
    "requires": [["item:key#1"]],
    "receive": ["item:bomb#15"],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["item:key#1", "entrance.north1"]],
    "receive": ["magic:double down"],
  },
  {
    "room": {"north": 16, "east": 22},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#400"],
  },
  {
    "room": {"north": 17, "east": 22},
    "requires": [["misc:blue crystal"]],
    "receive": ["item:diamonds#20"],
  },
  {
    "room": {"north": 21, "east": 23},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#300", "item:diamonds#2"],
  },
  {
    "room": {"north": 19, "east": 23},
    "requires": [["item:key#1"]],
    "receive": ["magic:fire"],
  },
  {
    "room": {"north": 18, "east": 23},
    "requires": [["permit:bomb", "item:key#1"]],
    "receive": ["weapon:warlock staff"],
  },
  {
    "room": {"north": 9, "east": 23},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["magic:drain"],
  },
  {
    "room": {"north": 4, "east": 24},
    "requires": [["item:key#1", "entrance.east0"]],
    "receive": ["food:cherry#10"],
  },
  {
    "room": {"north": 6, "east": 24},
    "requires": [["skill:reveal"]],
    "receive": ["misc:red chest"],
  },
  {
    "room": {"north": 15, "east": 24},
    "requires": [["item:key#1", "entrance.north0"]],
    "receive": ["item:gold#2"],
    "info": "gold not fixed",
  },
  {
    "room": {"north": 16, "east": 24},
    "requires": [["misc:blue crystal", "entrance.north1"]],
    "receive": ["item:gold#1000", "food:gummy bear#12"],
  },
  {
    "room": {"north": 16, "east": 25},
    "requires": [
      ["misc:blue crystal", "entrance.south0"],
      ["misc:blue crystal", "entrance.west0"],
    ],
    "receive": ["item:diamonds#5", "food:steak#12"],
  },
  {
    "room": {"north": 12, "east": 25},
    "requires": [["misc:blue crystal"]],
    "receive": ["item:diamonds#50", "food:gummy bear#50"],
  },
  {
    "room": {"north": 11, "east": 25},
    "requires": [["misc:blue crystal"]],
    "receive": ["food:beef jerky#20"],
  },
  {
    "room": {"north": 3, "east": 26},
    "requires": [["misc:blue crystal"]],
    "receive": ["food:elixir#1"],
  },
  {
    "room": {"north": 4, "east": 26},
    "requires": [
      ["permit:bomb", "entrance.south3", "item:key#1"],
      ["permit:bomb", "entrance.south2", "item:key#1"],
      ["permit:bomb", "entrance.south1", "item:key#1"],
    ],
    "receive": ["weapon:shadow staff"],
  },
  {
    "room": {"north": 9, "east": 26},
    "requires": [["item:key#1"]],
    "receive": ["food:blueberries#10"],
  },
  # TODO
  {
    "room": {"north": 16, "east": 18},
    "requires": [["quest:bBomb.13"]],
    "receive": ["quest:bBomb.25"],
  },
  {
    "room": {"north": 11, "east": 16},
    "requires": [["quest:dream.6"]],
    "receive": ["quest:dream.7"],
  },
  {
    "room": {"north": 16, "east": 10},
    "requires": [["quest:rings.15"]],
    "receive": ["quest:rings.16"],
  },
  {
    "room": {"north": 17, "east": 10},
    "requires": [["quest:hWater.4"]],
    "receive": ["quest:hWater.5"],
  },
  {
    "room": {"north": 11, "east": 16},
    "requires": [["quest:oMan.5"]],
    "receive": ["quest:oMan.6"],
  },
  {
    "room": {"north": 10, "east": 15},
    "requires": [["quest:canteen.1"]],
    "receive": ["quest:canteen.2"],
  },
  {
    "room": {"north": 10, "east": 15},
    "requires": [["quest:canteen.3"]],
    "receive": ["quest:canteen.4"],
  },
  {
    "room": {"north": 21, "east": 17},
    "requires": [["quest:oMan.19"]],
    "receive": ["quest:oMan.20"],
  },
  {
    "room": {"north": 11, "east": 23},
    "requires": [["quest:dream.2"]],
    "receive": ["quest:dream.3"],
  },
  {
    "room": {"north": 14, "east": 17},
    "requires": [[]],
    "receive": ["quest:mChal.1"],
  },
  {
    "room": {"north": 13, "east": 14},
    "requires": [["quest:mChal.1"]],
    "receive": ["quest:mChal.2"],
  },
  {
    "room": {"north": 11, "east": 23},
    "requires": [["quest:dream.3"]],
    "receive": ["quest:dream.4"],
  },
  {
    "room": {"north": 6, "east": 24},
    "requires": [["quest:pam.11"]],
    "receive": ["quest:pam.12"],
  },
  {
    "room": {"north": 4, "east": 19},
    "requires": [["quest:isles.3"]],
    "receive": ["quest:isles.4"],
  },
  {
    "room": {"north": 17, "east": 11},
    "requires": [["quest:hWater.5"]],
    "receive": ["quest:hWater.6"],
  },
  {
    "room": {"north": 17, "east": 11},
    "requires": [["quest:hWater.3"]],
    "receive": ["quest:hWater.4"],
  },
  {
    "room": {"north": 15, "east": 17},
    "requires": [["quest:hWater.0"]],
    "receive": ["quest:hWater.1"],
  },
  {
    "room": {"north": 15, "east": 17},
    "requires": [["quest:hWater.6"]],
    "receive": ["quest:hWater.7"],
  },
  {
    "room": {"north": 16, "east": 15},
    "requires": [["quest:hWater.1"]],
    "receive": ["quest:hWater.2"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.12"]],
    "receive": ["quest:pam.13"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.13"]],
    "receive": ["quest:pam.14"],
  },
  {
    "room": {"north": 19, "east": 20},
    "requires": [["quest:pam.14"]],
    "receive": ["quest:pam.15"],
  },
  {
    "room": {"north": 14, "east": 17},
    "requires": [["quest:mChal.2"]],
    "receive": ["quest:mChal.3"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.1"]],
    "receive": ["quest:access.2"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.3"]],
    "receive": ["quest:access.4"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.4"]],
    "receive": ["quest:access.5"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.5"]],
    "receive": ["quest:access.6"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.6"]],
    "receive": ["quest:access.7"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.8"]],
    "receive": ["quest:access.9"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.2"]],
    "receive": ["quest:access.3"],
  },
  {
    "room": {"north": 19, "east": 16},
    "requires": [["quest:access.7"]],
    "receive": ["quest:access.8"],
  },
  {
    "room": {"north": 17, "east": 18},
    "requires": [["quest:bBomb.9"]],
    "receive": ["quest:bBomb.10"],
  },
  {
    "room": {"north": 17, "east": 18},
    "requires": [["quest:bBomb.12"]],
    "receive": ["quest:bBomb.13"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:oMan.16"]],
    "receive": ["quest:oMan.17"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["quest:oMan.18"]],
    "receive": ["quest:oMan.19"],
  },
  {
    "room": {"north": 13, "east": 14},
    "requires": [["quest:mChal.3"]],
    "receive": ["quest:mChal.4"],
  },
  {
    "room": {"north": 11, "east": 23},
    "requires": [["quest:dream.4"]],
    "receive": ["quest:dream.5"],
  },
  {
    "room": {"north": 10, "east": 10},
    "requires": [["quest:dream.8"]],
    "receive": ["quest:dream.9"],
  },
  {
    "room": {"north": 11, "east": 16},
    "requires": [["quest:dream.5"]],
    "receive": ["quest:dream.6"],
  },
  {
    "room": {"north": 100, "east": 100},
    "requires": [["quest:isles.0"]],
    "receive": ["quest:isles.1"],
  },
  {
    "room": {"north": 100, "east": 100},
    "requires": [["quest:isles.16"]],
    "receive": ["quest:isles.17"],
  },
  {
    "room": {"north": 4, "east": 26},
    "requires": [["quest:isles.18"]],
    "receive": ["quest:isles.19"],
  },
  {
    "room": {"north": 201, "east": 200},
    "requires": [["quest:isles.2"]],
    "receive": ["quest:isles.3"],
  },
  {
    "room": {"north": 201, "east": 200},
    "requires": [["quest:isles.4"]],
    "receive": ["quest:isles.5"],
  },
  {
    "room": {"north": 201, "east": 200},
    "requires": [["quest:isles.7"]],
    "receive": ["quest:isles.8"],
  },
  {
    "room": {"north": 201, "east": 200},
    "requires": [["quest:isles.14"]],
    "receive": ["quest:isles.15"],
  },
  {
    "room": {"north": 300, "east": 300},
    "requires": [["quest:isles.1"]],
    "receive": ["quest:isles.2"],
  },
  {
    "room": {"north": 300, "east": 300},
    "requires": [["quest:isles.5"]],
    "receive": ["quest:isles.6"],
  },
  {
    "room": {"north": 300, "east": 300},
    "requires": [["quest:isles.15"]],
    "receive": ["quest:isles.16"],
  },
  {
    "room": {"north": 300, "east": 300},
    "requires": [["quest:isles.17"]],
    "receive": ["quest:isles.18"],
  },
  {
    "room": {"north": 300, "east": 300},
    "requires": [["quest:isles.23"]],
    "receive": ["quest:isles.24"],
  },
  {
    "room": {"north": 8, "east": 12},
    "requires": [["quest:isles.8"]],
    "receive": ["quest:isles.9"],
  },
  {
    "room": {"north": 8, "east": 12},
    "requires": [["quest:isles.10"]],
    "receive": ["quest:isles.11"],
  },
  {
    "room": {"north": 8, "east": 12},
    "requires": [["quest:isles.11"]],
    "receive": ["quest:isles.12"],
  },
  {
    "room": {"north": 9, "east": 18},
    "requires": [["quest:isles.9"]],
    "receive": ["quest:isles.10"],
  },
  {
    "room": {"north": 14, "east": 22},
    "requires": [["quest:rings.14"]],
    "receive": ["quest:rings.15"],
  },
  {
    "room": {"north": 18, "east": 12},
    "requires": [["quest:rings.16"]],
    "receive": ["quest:rings.17"],
  },
  {
    "room": {"north": 19, "east": 14},
    "requires": [["quest:hWater.2"]],
    "receive": ["quest:hWater.3"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:bBomb.10"]],
    "receive": ["quest:bBomb.11"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:bBomb.11"]],
    "receive": ["quest:bBomb.12"],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["quest:bBomb.25"]],
    "receive": ["quest:bBomb.26"],
  },
  {
    "room": {"north": 13, "east": 17},
    "requires": [["quest:dream.1"]],
    "receive": ["quest:dream.2"],
  },
  {
    "room": {"north": 13, "east": 17},
    "requires": [["quest:dream.11"]],
    "receive": ["quest:dream.12"],
  },
  {
    "room": {"north": 13, "east": 17},
    "requires": [["quest:dream.13"]],
    "receive": ["quest:dream.14"],
  },
  {
    "room": {"north": 13, "east": 17},
    "requires": [["quest:dream.14"]],
    "receive": ["quest:dream.15"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.0"]],
    "receive": ["quest:aSword.1"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.12"]],
    "receive": ["quest:aSword.13"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.6"]],
    "receive": ["quest:aSword.7"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.4"]],
    "receive": ["quest:aSword.5"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.2"]],
    "receive": ["quest:aSword.3"],
  },
  {
    "room": {"north": 20, "east": 16},
    "requires": [["quest:aSword.3"]],
    "receive": ["quest:aSword.4"],
  },
  {
    "room": {"north": 20, "east": 17},
    "requires": [["quest:aSword.5"]],
    "receive": ["quest:aSword.6"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.7"]],
    "receive": ["quest:aSword.11"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.57"]],
    "receive": ["quest:aSword.58"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.51"]],
    "receive": ["quest:aSword.52"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.45"]],
    "receive": ["quest:aSword.46"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.39"]],
    "receive": ["quest:aSword.40"],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["quest:aSword.23"]],
    "receive": ["quest:aSword.24"],
  },
  {
    "room": {"north": 15, "east": 25},
    "requires": [["quest:oMan.13"]],
    "receive": ["quest:oMan.14"],
  },
  {
    "room": {"north": 10, "east": 23},
    "requires": [["quest:oMan.10"]],
    "receive": ["quest:oMan.11"],
  },
  {
    "room": {"north": 10, "east": 15},
    "requires": [["quest:oMan.8"]],
    "receive": ["quest:oMan.9"],
  },
  {
    "room": {"north": 10, "east": 15},
    "requires": [["quest:oMan.6"]],
    "receive": ["quest:oMan.7"],
  },
  {
    "room": {"north": 11, "east": 21},
    "requires": [["quest:oMan.15"]],
    "receive": ["quest:oMan.16"],
  },
  {
    "room": {"north": 11, "east": 21},
    "requires": [["quest:oMan.11"]],
    "receive": ["quest:oMan.12"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [["quest:oMan.14"]],
    "receive": ["quest:oMan.15"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [["quest:oMan.21"]],
    "receive": ["quest:oMan.22"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [["quest:oMan.20"]],
    "receive": ["quest:oMan.21"],
  },
  {
    "room": {"north": 17, "east": 19},
    "requires": [["quest:oMan.12"]],
    "receive": ["quest:oMan.13"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#3"]],
    "receive": ["skill:hint"],
  },{
					"room": {"north": 19, "east": 15},
					"requires": [["item:medallion#200"]],
					"receive": ["skill:shield"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#5"]],
					"receive": ["food:apple"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#1"]],
					"receive": ["food:honey"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#15"]],
					"receive": ["food:grapes"],
				},{
					"room": {"north": 12, "east": 9},
					"requires": [["item:gold#125"]],
					"receive": ["food:carrot"],
				},{
					"room": {"north": 12, "east": 9},
					"requires": [["item:gold#200"]],
					"receive": ["food:beefJerky"],
				},{
					"room": {"north": 12, "east": 9},
					"requires": [["item:gold#250"]],
					"receive": ["food:cherries"],
				},{
					"room": {"north": 21, "east": 20},
					"requires": [["item:gold#50"]],
					"receive": ["magic:slow"],
				},{
					"room": {"north": 21, "east": 20},
					"requires": [["item:gold#100"]],
					"receive": ["magic:heal"],
				},{
					"room": {"north": 21, "east": 20},
					"requires": [["item:gold#200"]],
					"receive": ["magic:blast"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#300"]],
					"receive": ["magic:regen"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#2000"]],
					"receive": ["magic:cloud"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#900"]],
					"receive": ["magic:weak"],
				},{
					"room": {"north": 11, "east": 9},
					"requires": [["item:gold#4500"]],
					"receive": ["magic:refresh"],
				},{
					"room": {"north": 11, "east": 9},
					"requires": [["item:gold#4000"]],
					"receive": ["magic:lightning"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#10"]],
					"receive": ["weapon:club"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#50"]],
					"receive": ["weapon:dagger"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#200"]],
					"receive": ["weapon:sword"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#800"]],
					"receive": ["weapon:royalSword"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#5000"]],
					"receive": ["weapon:royalStaff"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#500"]],
					"receive": ["armor:vest"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#300"]],
					"receive": ["armor:robe"],
				},{
					"room": {"north": 20, "east": 20},
					"requires": [["item:gold#8000"]],
					"receive": ["armor:iron"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#15000"]],
					"receive": ["armor:royalArmor"],
				},{
					"room": {"north": 13, "east": 17},
					"requires": [["item:gold#7000"]],
					"receive": ["armor:mysticCloak"],
				},{
					"room": {"north": 12, "east": 9},
					"requires": [["item:gold#2500"]],
					"receive": ["armor:sunArmor"],
				},{
					"room": {"north": 12, "east": 9},
					"requires": [["item:gold#3500"]],
					"receive": ["armor:speedVest"],
				},{
					"room": {"north": 19, "east": 20},
					"requires": [[]],
					"receive": ["skill:dig"],
				},{
					"room": {"north": 19, "east": 20},
					"requires": [[]],
					"receive": ["skill:kick"],
				},{
					"room": {"north": 500, "east": 501},
					"requires": [["weapon:bane blade#"]],
					"receive": ["weapon:alpha sword0"],
				},{
					"room": {"north": 200, "east": 200},
					"requires": [["weapon:orc blade"]],
					"receive": ["weapon:twin fury"],
				},
        # Auto-generated from MathQuest_base.js newItem() calls
# 159 items extracted

  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:kCrest#50"], ["item:sFrag#7"], ["armor:phantomCoat"], ["armor:sunArmor"]],
    "receive": ['skill:hint'],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:sFrag#7"], ["armor:sunArmor"]],
    "receive": ['skill:shield'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['food:apple'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['food:honey'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['food:grapes'],
  },
  {
    "room": {"north": 12, "east": 9},
    "receive": ['food:carrot'],
  },
  {
    "room": {"north": 12, "east": 9},
    "receive": ['food:beefJerky'],
  },
  {
    "room": {"north": 12, "east": 9},
    "receive": ['food:cherries'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['food:chocolate'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['food:steak'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['food:peppers'],
  },
  {
    "room": {"north": 21, "east": 20},
    "receive": ['magic:slow'],
  },
  {
    "room": {"north": 21, "east": 20},
    "receive": ['magic:heal'],
  },
  {
    "room": {"north": 21, "east": 20},
    "receive": ['magic:blast'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['magic:regen'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['magic:cloud'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['magic:weak'],
  },
  {
    "room": {"north": 11, "east": 9},
    "receive": ['magic:refresh'],
  },
  {
    "room": {"north": 11, "east": 9},
    "receive": ['magic:lightning'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['weapon:club'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['weapon:dagger'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['weapon:sword'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['weapon:royalSword'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['weapon:royalStaff'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['armor:vest'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['armor:robe'],
  },
  {
    "room": {"north": 20, "east": 20},
    "receive": ['armor:iron'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['armor:royalArmor'],
  },
  {
    "room": {"north": 13, "east": 17},
    "receive": ['armor:mysticCloak'],
  },
  {
    "room": {"north": 12, "east": 9},
    "receive": ['armor:sunArmor'],
  },
  {
    "room": {"north": 12, "east": 9},
    "receive": ['armor:speedVest'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['skill:dig'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['skill:kick'],
  },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["weapon:baneBlade"]],
    "receive": ['weapon:aSword'],
  },
  {
    "room": {"north": 200, "east": 200},
    "requires": [["item:sTooth#10"], ["item:dScale#3"], ["item:sTooth#5"], ["item:vHorn#5"], ["item:oArm#5"], ["item:vHorn#20"], ["item:cThread#30"], ["item:gFeather#5"], ["weapon:orcBlade"]],
    "receive": ['weapon:twinFury'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:sTooth#30"], ["item:oArm#40"], ["item:cShell#25"], ["item:oCoin#110"], ["item:mHorn#5"], ["item:aScepter#3"], ["item:gFeather#3"], ["item:aScepter#5"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:oArm#40"], ["item:cShell#25"], ["item:oCoin#110"], ["item:mHorn#5"], ["item:aScepter#3"], ["item:gFeather#3"], ["item:aScepter#5"], ["item:kCrest#10"], ["item:aAxe#5"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:mHorn#5"], ["item:aScepter#3"], ["item:gFeather#3"], ["item:aScepter#5"], ["item:kCrest#10"], ["item:aAxe#5"], ["item:dScale#10"], ["item:gSkin#10"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:gFeather#3"], ["item:aScepter#5"], ["item:kCrest#10"], ["item:aAxe#5"], ["item:dScale#10"], ["item:gSkin#10"], ["item:oCoin#20"], ["item:mStaff#10"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:gFeather#3"], ["item:aScepter#5"], ["item:kCrest#10"], ["item:aAxe#5"], ["item:dScale#10"], ["item:gSkin#10"], ["item:oCoin#20"], ["item:mStaff#10"], ["item:cFang#5"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 18, "east": 25},
    "requires": [["item:kCrest#10"], ["item:aAxe#5"], ["item:dScale#10"], ["item:gSkin#10"], ["item:oCoin#20"], ["item:mStaff#10"], ["item:cFang#5"], ["item:tBand#2"]],
    "receive": ['skill:medic'],
  },
  {
    "room": {"north": 19, "east": 22},
    "requires": [["item:tBand#2"], ["item:vAsh#30"], ["item:cThread#10"]],
    "receive": ['skill:reveal'],
  },
  {
    "room": {"north": 11, "east": 12},
    "requires": [["item:oCoin#20"]],
    "receive": ['food:sunflowerSeeds'],
  },
  {
    "room": {"north": 21, "east": 23},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 21, "east": 23},
    "receive": ['gold'],
  },
  {
    "room": {"north": 6, "east": 13},
    "receive": ['food:grapes'],
  },
  {
    "room": {"north": 6, "east": 13},
    "receive": ['food:strawberry'],
  },
  {
    "room": {"north": 11, "east": 19},
    "receive": ['food:sunflowerSeeds'],
  },
  {
    "room": {"north": 11, "east": 19},
    "receive": ['food:strawberry'],
  },
  {
    "room": {"north": 23, "east": 10},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 23, "east": 10},
    "receive": ['food:newtonsApple'],
  },
  {
    "room": {"north": 17, "east": 20},
    "receive": ['gold'],
  },
  {
    "room": {"north": 17, "east": 20},
    "receive": ['food:beefJerky'],
  },
  {
    "room": {"north": 15, "east": 24},
    "receive": ['gold'],
  },
  {
    "room": {"north": 10, "east": 9},
    "receive": ['food:steak'],
  },
  {
    "room": {"north": 9, "east": 26},
    "receive": ['food:blueberries'],
  },
  {
    "room": {"north": 21, "east": 11},
    "receive": ['food:gummyBears'],
  },
  {
    "room": {"north": 24, "east": 11},
    "receive": ['weapon:baneBlade'],
  },
  {
    "room": {"north": 21, "east": 21},
    "requires": [["item:wPelt#2"], ["item:tBand#5"], ["item:tBand#5"], ["item:gSkin#2"]],
    "receive": ['skill:craft'],
  },
  {
    "room": {"north": 9, "east": 22},
    "requires": [["item:wPelt#2"], ["item:tBand#5"], ["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['magic:doubleDown'],
  },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["item:wPelt#2"], ["item:tBand#5"], ["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['magic:crush'],
  },
  {
    "room": {"north": 18, "east": 20},
    "requires": [["item:wPelt#2"], ["item:tBand#5"], ["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['gold'],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["item:wPelt#2"], ["item:tBand#5"], ["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['geode'],
  },
  {
    "room": {"north": 17, "east": 16},
    "requires": [["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 18, "east": 17},
    "requires": [["item:tBand#5"], ["item:gSkin#2"], ["food:honey#5"]],
    "receive": ['gold'],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["food:honey#5"]],
    "receive": ['gold'],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["food:honey#5"]],
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["food:honey#5"]],
    "receive": ['food:banana'],
  },
  {
    "room": {"north": 11, "east": 21},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 14, "east": 15},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 14, "east": 15},
    "receive": ['food:orange'],
  },
  {
    "room": {"north": 24, "east": 14},
    "receive": ['armor:grimGear'],
  },
  {
    "room": {"north": 9, "east": 15},
    "receive": ['armor:phantomCoat'],
  },
  {
    "room": {"north": 15, "east": 21},
    "receive": ['gold'],
  },
  {
    "room": {"north": 15, "east": 21},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 4, "east": 24},
    "receive": ['food:cherries'],
  },
  {
    "room": {"north": 6, "east": 10},
    "receive": ['food:chocolate'],
  },
  {
    "room": {"north": 9, "east": 10},
    "receive": ['gold'],
  },
  {
    "room": {"north": 11, "east": 17},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 11, "east": 17},
    "receive": ['gold'],
  },
  {
    "room": {"north": 14, "east": 21},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 14, "east": 21},
    "receive": ['food:apple'],
  },
  {
    "room": {"north": 14, "east": 21},
    "receive": ['gold'],
  },
  {
    "room": {"north": 4, "east": 26},
    "receive": ['weapon:shadowStaff'],
  },
  {
    "room": {"north": 18, "east": 23},
    "receive": ['weapon:warlockStaff'],
  },
  {
    "room": {"north": 15, "east": 14},
    "receive": ['food:carrot'],
  },
  {
    "room": {"north": 9, "east": 23},
    "receive": ['magic:drain'],
  },
  {
    "room": {"north": 15, "east": 16},
    "requires": [["item:mStaff#20"]],
    "receive": ['magic:ice'],
  },
  {
    "room": {"north": 11, "east": 18},
    "requires": [["item:mStaff#20"]],
    "receive": ['magic:refresh'],
  },
  {
    "room": {"north": 13, "east": 16},
    "requires": [["item:mStaff#20"]],
    "receive": ['weapon:sKnife'],
  },
  {
    "room": {"north": 13, "east": 16},
    "requires": [["item:mStaff#20"]],
    "receive": ['magic:weak'],
  },
  {
    "room": {"north": 14, "east": 19},
    "requires": [["item:vAsh#6"]],
    "receive": ['armor:regenArmor'],
  },
  {
    "room": {"north": 16, "east": 22},
    "requires": [["item:vAsh#6"]],
    "receive": ['gold'],
  },
  {
    "room": {"north": 19, "east": 23},
    "receive": ['magic:fire'],
  },
  {
    "room": {"north": 18, "east": 21},
    "receive": ['food:gingerBread'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['item:ring of gold'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['misc:ring of health'],
  },
  {
    "room": {"north": 18, "east": 24},
    "receive": ['headstoneSwitch1'],
  },
  {
    "room": {"north": 16, "east": 16},
    "receive": ['headstoneSwitch2'],
  },
  {
    "room": {"north": 12, "east": 12},
    "receive": ['headstoneSwitch3'],
  },
  {
    "room": {"north": 10, "east": 25},
    "receive": ['headstoneSwitch4'],
  },
  {
    "room": {"north": 18, "east": 19},
    "receive": ['gold'],
  },
  {
    "room": {"north": 12, "east": 21},
    "receive": ['food:banana'],
  },
  {
    "room": {"north": 12, "east": 21},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 8, "east": 18},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 8, "east": 18},
    "receive": ['food:steak'],
  },
  {
    "room": {"north": 17, "east": 15},
    "receive": ['gold'],
  },
  {
    "room": {"north": 17, "east": 15},
    "receive": ['food:gingerBread'],
  },
  {
    "room": {"north": 8, "east": 10},
    "receive": ['gold'],
  },
  {
    "room": {"north": 8, "east": 10},
    "receive": ['food:beefJerky'],
  },
  {
    "room": {"north": 21, "east": 18},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 21, "east": 18},
    "receive": ['food:peppers'],
  },
  {
    "room": {"north": 9, "east": 25},
    "receive": ['gold'],
  },
  {
    "room": {"north": 9, "east": 25},
    "receive": ['food:elixir'],
  },
  {
    "room": {"north": 23, "east": 10},
    "receive": ['armor:alphaArmor'],
  },
  {
    "room": {"north": 3, "east": 26},
    "receive": ['food:elixir'],
  },
  {
    "room": {"north": 16, "east": 24},
    "receive": ['food:gummyBears'],
  },
  {
    "room": {"north": 16, "east": 24},
    "receive": ['gold'],
  },
  {
    "room": {"north": 16, "east": 25},
    "receive": ['food:steak'],
  },
  {
    "room": {"north": 16, "east": 25},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 12, "east": 25},
    "receive": ['food:gummyBears'],
  },
  {
    "room": {"north": 12, "east": 25},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 18, "east": 15},
    "receive": ['food:newtonsApple'],
  },
  {
    "room": {"north": 11, "east": 25},
    "receive": ['food:beefJerky'],
  },
  {
    "room": {"north": 16, "east": 15},
    "receive": ['armor:diamondArmor'],
  },
  {
    "room": {"north": 17, "east": 22},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 15, "east": 18},
    "receive": ['item:bombs'],
  },
  {
    "room": {"north": 15, "east": 18},
    "receive": ['food:chocolate'],
  },
  {
    "room": {"north": 12, "east": 12},
    "receive": ['magic:blessing'],
  },
  {
    "room": {"north": 19, "east": 18},
    "receive": ['rubies'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['gold'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:gingerBread'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:chocolate'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:steak'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:peppers'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:orange'],
  },
  {
    "room": {"north": 19, "east": 20},
    "receive": ['food:holyWater'],
  },
  {
    "room": {"north": 19, "east": 21},
    "receive": ['gold'],
  },
  {
    "room": {"north": 12, "east": 11},
    "receive": ['diamonds'],
  },
  {
    "room": {"north": 13, "east": 26},
    "receive": ['food:gingerBread'],
  },
  {
    "room": {"north": 6, "east": 12},
    "receive": ['skill:convert'],
  },
  {
    "room": {"north": 11, "east": 9},
    "receive": ['skill:warp'],
  },
  {
    "room": {"north": 9, "east": 22},
    "receive": ['food:orange'],
  },
  {
    "room": {"north": 9, "east": 22},
    "receive": ['food:peppers'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "requires": [["item:sClaw#7"], ["item:cFang#5"]],
    "receive": ['item:fire crystal'],
  },
  {
    "room": {"north": 4, "east": 26},
    "receive": ['skill:tough'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "requires": [["item:dScale#3"], ["item:sFrag#5"], ["item:fBone#10"]],
    "receive": ['item:ring of skill'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['item:ring of evasion'],
  },
  {
    "room": {"north": 15, "east": 18},
    "receive": ['food:beefJerky'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['craft:bomb'],
  },
  {
    "room": {"north": 14, "east": 18},
    "requires": [["weapon:royalSword"]],
    "receive": ['weapon:creeperCrusher'],
  },
  {
    "room": {"north": 14, "east": 18},
    "receive": ['pup'],
  },
  {
    "room": {"north": 14, "east": 18},
    "receive": ['gold'],
  },
  {
    "room": {"north": 13, "east": 17},
    "requires": [["armor:royalArmor"]],
    "receive": ['armor:nobleArmor'],
  },
  {
    "room": {"north": '?', "east": '?'},
    "receive": ['misc:bobbisPendant'],
  },
  {
    "room": {"north": 21, "east": 20},
    "receive": ['gold'],
  },
]
