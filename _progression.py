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
      "item:aurastone",
      "item:key",
      "item:gold",
    ],
    "info": "can be got anywhere",
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
    "receive": ["armor:vest"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["armor:magic robe"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["armor:iron armour"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:apple"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:honey"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [["item:gold"]],
    "receive": ["food:grapes"],
  },
  {"room": {"north": 18, "east": 20}, "info": "warp skill warp point"},
  {
    "room": {"north": 18, "east": 20},
    "requires": [["item:key"]],
    "receive": ["item:gold#30"],
  },
  {
    "room": {"north": 18, "east": 19},
    "requires": [["item:emerald#1"]],
    "receive": ["item:gold#?", "food:strawberry#1"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["skill:dig"]],
    "receive": ["item:gold#25"],
  },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["item:diamond#20"]],
  #   "receive": ["quest:pam.?"],
  # },
  {
    "room": {"north": 16, "east": 22},
    "requires": [["item:gold#400"]],
    "receive": ["item:key#1"],
  },
  {
    "room": {"north": 15, "east": 19},
    "requires": [["item:ring of health"]],
    "receive": ["item:gold#300", "item:bomb#10", "food:banana#5"],
    "info": "???",
  },
  {
    "room": {"north": 14, "east": 19},
    "requires": [["item:troll wristband#1", "entrance.north0"]],
    "receive": ["item:broken alpha club#1"],
  },
  {
    "room": {"north": 14, "east": 19},
    "requires": [["item:key#1", "entrance.south0"]],
    "receive": ["armour:regen armor"],
  },
  {
    "room": {"north": 15, "east": 21},
    "requires": [["item:key#1", "entrance.south0"]],
    "receive": ["item:gold#65", "item:bomb#5"],
  },
  {
    "room": {"north": 14, "east": 21},
    "requires": [
      ["item:key#1", "entrance.north0"],
      ["permit:bomb", "item:key#1", "entrance.south0"],
    ],
    "receive": ["item:gold#100", "item:bomb#12", "food:apple#30"],
  },
  {
    "room": {"north": 12, "east": 21},
    "requires": [["item:emerald#1", "permit:bomb"]],
    "receive": ["item:diamond#1", "food:banana#20"],
  },
  {"room": {"north": 12, "east": 19}, "info": "warp skill warp point"},
  {
    "room": {"north": 13, "east": 16},
    "requires": [["item:key#1", "entrance.west0"]],
    "receive": ["weapon:survival knife"],
  },
  {
    "room": {"north": 14, "east": 15},
    "requires": [["item:key#1"]],
    "receive": ["food:orange#12"],
  },
  {"room": {"north": 14, "east": 16}, "info": "warp skill warp point"},
  {
    "room": {"north": 15, "east": 16},
    "requires": [["permit:bomb", "???"]],
    "receive": ["magic:ice"],
  },
  {
    "room": {"north": 13, "east": 14},
    "requires": [
      ["magic:fire.3?", "quest:?", "entrance.east0"],
      ["magic:fire.3?", "quest:?", "entrance.north0", "permit:bomb"],
    ],
    "receive": ["???"],
  },
  {
    "room": {"north": 13, "east": 13},
    "requires": [["armor:alpha armor", "???"]],
    "receive": ["armour:alpha armour.+inf"],
  },
  {
    "room": {"north": 11, "east": 13},
    "requires": [["item:mage staff#1"]],
    "receive": ["food:blueberry#1"],
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
    "receive": ["food:beef jerkey"],
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
    "receive": ["armor:sun armour"],
  },
  {
    "room": {"north": 12, "east": 9},
    "requires": [["item:gold"]],
    "receive": ["armor:speed vest"],
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
    "room": {"north": 11, "east": 11},
    "requires": [["???"]],
    "receive": ["quest:???"],
  },
  {
    "room": {"north": 10, "east": 9},
    "requires": [["permit:bomb.2", "item:key#1"]],
    "receive": ["food:steak#30"],
  },
  {
    "room": {"north": 9, "east": 10},
    "requires": [["permit:bomb", "item:key#1"]],
    "receive": ["item:gold#750"],
  },
  {
    "room": {"north": 8, "east": 10},
    "requires": [
      ["item:emerald#1", "entrance.north1"],
      ["item:emerald#1", "entrance.east1"],
      ["item:emerald#1", "entrance.east2"],
    ],
    "receive": ["item:gold#750"],
  },
  {
    "room": {"north": 6, "east": 12},
    "requires": [["item:key#1"]],
    "receive": ["item:quartz geode#2"],
  },
  {
    "room": {"north": 6, "east": 10},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["food:chocolate#3"],
  },
  {
    "room": {"north": 5, "east": 9},
    "requires": [
      ["item:minotour horn", "entrance.north0"],
      ["item:minotour horn", "entrance.east0"],
    ],
    "receive": ["item:broken alpha axe#1"],
  },
  {
    "room": {"north": 6, "east": 13},
    "requires": [["item:key#1"]],
    "receive": ["food:grapes#5", "food:strawberry#1"],
  },
  {
    "room": {"north": 8, "east": 14},
    "requires": [["item:shark tooth#30", "item:gold#800", "skill:tough"]],
    "receive": ["skill:tough.+1"],
  },
  {
    "room": {"north": 5, "east": 15},
    "requires": [["skill:reveal"]],
    "receive": ["red chest"],
  },
  {
    "room": {"north": 9, "east": 15},
    "requires": [["item:key#1"]],
    "receive": ["armor:phantom coat"],
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
  {"room": {"north": 8, "east": 17}, "receive": ["green secret code"]},
  {
    "room": {"north": 8, "east": 18},
    "requires": [["item:emerald#1", "entrance.north1"]],
    "receive": ["food:steak#?", "item:bomb#25"],
  },
  {
    "room": {"north": 11, "east": 18},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#6000"],
  },
  {
    "room": {"north": 11, "east": 17},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["item:bomb#8", "item:gold#200"],
  },
  {
    "room": {"north": 7, "east": 10},
    "requires": [["permit:bomb", "???"]],
    "receive": ["item:orb of ???"],
  },
  {
    "room": {"north": 10, "east": 19},
    "requires": [["???"]],
    "receive": ["item:orb of ???"],
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
    "requires": [["item:key#1", "entrance.north1"]],
    "receive": ["magic:double down"],
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
    "receive": ["craft.elixir"],
  },
  {
    "room": {"north": 10, "east": 25},
    "requires": [["quest:rings.1"]],
    "receive": ["misc:headstone 3"],
  },
  # {
  #   # "room": {"north": 11, "east": 20},
  #   # "requires": [["quest:pam.?"]],
  #   # "receive": ["food:beef jerkey#20"],
  # },
  {"room": {"north": 11, "east": 24}, "info": "warp skill warp point"},
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["skill:dig"]],
  #   "receive": ["ring:gold", "quest:rings.?"],
  # },
  {
    "room": {"north": 11, "east": 21},
    "requires": [["item:key#1"]],
    "receive": ["item:bomb#15"],
  },
  {
    "room": {"north": 11, "east": 19},
    "requires": [["item:key#1", "entrance.east0"]],
    "receive": ["food:sunflower seed#?", "food:strawberry#1"],
  },
  {
    "room": {"north": 11, "east": 22},
    "requires": [["item:shark tooth#10", "skill:craft"]],
    "receive": ["craft.emerald"],
  },
  {
    "room": {"north": 12, "east": 25},
    "requires": [["item:shark tooth#10", "skill:craft"]],
    "receive": ["food:gummy bear#10", "item:diamond#50"],
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
    "room": {"north": 9, "east": 26},
    "requires": [["item:key#1"]],
    "receive": ["food:blueberry#?"],
  },
  {
    "room": {"north": 15, "east": 24},
    "requires": [["item:key#1"]],
    "receive": ["item:gold#93"],
  },
  # {
  #   # "room": {"north": 16, "east": 20},
  #   # "requires": [["quest:pam.?"]],
  #   # "receive": ["item:diamond#5", "food:steak#12"],
  # },
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
  # {
  #   # "room": {"north": 16, "east": 20},
  #   # "requires": [["quest:pam.?", "entrance.north1"]],
  #   # "receive": ["food:gummy bear#13", "item:gold#1001"],
  # },
  {
    "room": {"north": 18, "east": 23},
    "requires": [["permit:bomb", "item:key#1"]],
    "receive": ["weapon:warlock staff"],
  },
  {
    "room": {"north": 21, "east": 23},
    "requires": [["item:key#1"]],
    "receive": ["item:diamond#2", "item:gold#300"],
  },
  {
    "room": {"north": 21, "east": 23},
    "requires": [["skill:dig"]],
    "receive": ["item:diamond#1"],
  },
  {
    "room": {"north": 21, "east": 22},
    "requires": [["ring:gold", "item:troll wristband#5", "item:gator skin#2"]],
    "receive": ["craft.ring of gold"],
  },
  {
    "room": {"north": 20, "east": 22},
    "requires": [["item:gold#500"]],
    "receive": ["item:ruby#1"],
  },
  {
    "room": {"north": 20, "east": 23},
    "requires": [["skill:reveal", "entrance.east0"]],
    "receive": ["red chest"],
  },
  {
    "room": {"north": 19, "east": 22},
    "requires": [["???"]],
    "receive": ["skill:reveal"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["quest:dig.3", "item:bear tooth#1"]],
    "receive": ["item:gold#18"],
  },
  {"room": {"north": 19, "east": 20}, "receive": ["quest:pam.1"]},
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 1"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 2"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 3"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 4"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 5"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 6"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 7"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 8"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 9"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 10"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 11"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 12"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 13"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?", "misc:blue flower 14"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   # "room": {"north": 19, "east": 20},
  #   # "requires": [["quest:pam.?", "???"]],
  #   # "receive": ["???"],
  # },
  {
    "room": {"north": 17, "east": 20},
    "requires": [["permit:bomb", "item:key#1"]],
    "receive": ["food:beef jerkey#5", "item:gold#200"],
  },
  # {
  #   "room": {"north": 17, "east": 19},
  #   "requires": [["???"]],
  #   "receive": ["quest:pendant.?"],
  # },
  {
    "room": {"north": 21, "east": 21},
    "requires": [["entrance.west0", "???"]],
    "receive": ["skill:craft"],
  },
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
    "requires": [["food:honey#20"]],
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
  # {
  #   "room": {"north": 19, "east": 18},
  #   "requires": [
  #     ["???", "entrance.north0"],
  #     ["???", "entrance.south1"],
  #     ["???", "entrance.east0"],
  #   ],
  #   "receive": ["misc:npc debugger 1"],
  #   "info": "npc has to move out the way before other npc works",
  # },
  {
    "room": {"north": 21, "east": 18},
    "requires": [["item:emerald#1"]],
    "receive": ["item:diamond#2", "food:peppers#20"],
  },
  {
    "room": {"north": 21, "east": 17},
    "requires": [["item:aurastone#1", "item:gold#500"]],
    "receive": ["item:ruby#1"],
  },
  # {
  #   # "room": {"north": 19, "east": 10},
  #   # "requires": [["quest:pam.?", "entrance.south0"]],
  #   # "receive": ["item:ruby#4"],
  # },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.1", "item:dragon scale#5", "item:medallion#3"]],
    "receive": ["skill.firewall.2"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.2", "item:dragon scale#10", "item:medallion#6"]],
    "receive": ["skill.firewall.3"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.3", "item:dragon scale#15", "item:medallion#9"]],
    "receive": ["skill.firewall.4"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.4", "item:dragon scale#20", "item:medallion#12"]],
    "receive": ["skill.firewall.5"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.5", "item:dragon scale#25", "item:medallion#15"]],
    "receive": ["skill.firewall.6"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.6", "item:dragon scale#30", "item:medallion#18"]],
    "receive": ["skill.firewall.7"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.7", "item:dragon scale#35", "item:medallion#21"]],
    "receive": ["skill.firewall.8"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.8", "item:dragon scale#40", "item:medallion#24"]],
    "receive": ["skill.firewall.9"],
  },
  {
    "room": {"north": 20, "east": 15},
    "requires": [["skill:firewall.9", "item:dragon scale#45", "item:medallion#27"]],
    "receive": ["skill.firewall.10"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#20"]],
    "receive": ["item:ruby#1"],
  },
  {
    "room": {"north": 19, "east": 15},
    "requires": [["item:medallion#3"]],
    "receive": ["skill:hint"],
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
  # {
  # "room": {"north": 18, "east": 10},
  # "requires": [["quest:pam.?"]],
  # "receive": ["food:newton apple#15"],
  # "info": "fill refresh too",
  # },
  {
    "room": {"north": 17, "east": 16},
    "requires": [["item:key#1"]],
    "receive": ["item:diamond#5"],
  },
  {
    "room": {"north": 16, "east": 16},
    "requires": [["quest:rings.1"]],
    "receive": ["misc:headstone 1"],
  },
  # {
  #   "room": {"north": 16, "east": 10},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["armor:diamond armour"],
  # },
  {
    "room": {"north": 17, "east": 15},
    "requires": [["item:emerald#1"]],
    "receive": ["item:gold#100", "food:coolie#50"],
  },
  {
    "room": {"north": 18, "east": 13},
    "requires": [["item:cotton thread#10", "item:shadow crest#5", "skill:reveal"]],
    "receive": ["misc:max bombs.149"],
  },
  {"room": {"north": 19, "east": 12}, "info": "warp skill warp point"},
  {
    "room": {"north": 24, "east": 14},
    "requires": [["item:key#1"]],
    "receive": ["armor:grim gear"],
  },
  {
    "room": {"north": 23, "east": 10},
    "requires": [["item:emerald#1"]],
    "receive": ["armour:alpha armour"],
  },
  {
    "room": {"north": 23, "east": 10},
    "requires": [["item:key#1"]],
    "receive": ["food:newton apple#3", "item:diamond#3"],
  },
  {
    "room": {"north": 21, "east": 11},
    "requires": [["item:key#1", "entrance.north0"]],
    "receive": ["food:gummy bear#?"],
  },
  {
    "room": {"north": 24, "east": 11},
    "requires": [["item:key#1", "permit:bomb"]],
    "receive": ["weapon:bane blade"],
  },
  {"room": {"north": 24, "east": 9}, "receive": ["misc:final boss"]},
  {
    "room": {"north": 17, "east": 10},
    "requires": [["item:void ash#6"]],
    "receive": ["food:gummy bear#5"],
  },
  # {
  #   # "room": {"north": 17, "east": 10},
  #   # "requires": [["quest:pam.?"]],
  #   # "receive": ["food:holy water#1"],
  #   "info": "right 11",
  # },
  {
    "room": {"north": 500, "east": 501},
    "requires": [["weapon:bane blade", "skill:reveal"]],
    "receive": ["quest:alpha blade.1"],
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
  # {
  #   # "room": {"north": 3, "east": 20},
  #   # "requires": [["quest:pam.?"]],
  #   # "receive": ["food:exixir"],
  # },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:orange"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:gingerbread"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:gold"]],
    "receive": ["food:strawberry"],
  },
  {
    "room": {"north": 4, "east": 13},
    "requires": [["item:shark tooth#5", "item:viking horn#5", "item:tentacle#5"]],
    "receive": ["craft.newton apple"],
  },
  {
    "room": {"north": 9, "east": 13},
    "requires": [["item:key#1"]],
    "receive": ["item:bomb#10"],
  },
  # {
  #   # "room": {"north": 15, "east": 10},
  #   # "requires": [["quest:pam.?", "permit:bomb.2"]],
  #   # "receive": ["item:bomb#50", "food:chocolate#?"],
  # },
  {
    "room": {"north": 11, "east": 15},
    "requires": [["skill:craft", "item:troll wristband#5", "item:wolf pelt#2"]],
    "receive": ["craft.key"],
  },
  # {
  #   "room": {"north": 9, "east": 25},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 18},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 21, "east": 17},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 18, "east": 19},
  #   "requires": [["quest:seeds.?"]],
  #   "receive": ["quest:seeds.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 23},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 23},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 12, "east": 22},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 6, "east": 12},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 6, "east": 12},
  #   "requires": [["quest:seeds.?"]],
  #   "receive": ["quest:seeds.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 17},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 21},
  #   "requires": [["quest:bBomb.?", "entrance.south0"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 18},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 17},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 23},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  {
    "room": {"north": 18, "east": 19},
    "requires": [[]],
    "receive": ["quest:gTree.1"],
  },
  # {
  #   "room": {"north": 18, "east": 19},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 14},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 23},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 12, "east": 26},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 7, "east": 11},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 9, "east": 26},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 4, "east": 19},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 16, "east": 21},
  #   "requires": [["quest:dig.?"]],
  #   "receive": ["quest:dig.?"],
  # },
  # {
  #   "room": {"north": 5, "east": 20},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 16, "east": 15},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 11},
  #   "requires": [["quest:hWater.?"]],
  #   "receive": ["quest:hWater.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 17},
  #   "requires": [["quest:hWater.?"]],
  #   "receive": ["quest:hWater.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 17},
  #   "requires": [["quest:hWater.?"]],
  #   "receive": ["quest:hWater.?"],
  # },
  # {
  #   "room": {"north": 16, "east": 15},
  #   "requires": [["quest:hWater.?"]],
  #   "receive": ["quest:hWater.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 20},
  #   "requires": [["quest:pam.?"]],
  #   "receive": ["quest:pam.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 21},
  #   "requires": [["quest:dig.?"]],
  #   "receive": ["quest:dig.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 17},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 12, "east": 11},
  #   "requires": [["quest:canteen.?"]],
  #   "receive": ["quest:canteen.?"],
  # },
  # {
  #   "room": {"north": 20, "east": 17},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 16},
  #   "requires": [["quest:access.?"]],
  #   "receive": ["quest:access.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 16},
  #   "requires": [["quest:access.?"]],
  #   "receive": ["quest:access.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 26},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 26},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 18},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 18},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 6, "east": 12},
  #   "requires": [["quest:geo.?"]],
  #   "receive": ["quest:geo.?"],
  # },
  # {
  #   "room": {"north": 6, "east": 12},
  #   "requires": [["quest:geo.?"]],
  #   "receive": ["quest:geo.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 14},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 14},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 10},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 10},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 16},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 16},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 9},
  #   "requires": [["quest:warp.?"]],
  #   "receive": ["quest:warp.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 9},
  #   "requires": [["quest:warp.?"]],
  #   "receive": ["quest:warp.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 17},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 12, "east": 9},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 19},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 7, "east": 10},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 7, "east": 10},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 100, "east": 100},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 100, "east": 100},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 4, "east": 26},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 4, "east": 26},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 201, "east": 200},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 201, "east": 200},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 201, "east": 200},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 300, "east": 300},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 300, "east": 300},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 300, "east": 300},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 8, "east": 12},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 8, "east": 12},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 9, "east": 18},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 22},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 18, "east": 12},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 18},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 20, "east": 18},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 20, "east": 18},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 11},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 18},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 21, "east": 20},
  #   "requires": [["quest:geo.?"]],
  #   "receive": ["quest:geo.?"],
  # },
  {
    "room": {"north": 21, "east": 20},
    "requires": [["entrance.south0"]],
    "receive": ["quest:bBomb.1"],
  },
  # {
  #   "room": {"north": 12, "east": 22},
  #   "requires": [["quest:curse.?"]],
  #   "receive": ["quest:curse.?"],
  # },
  # {
  #   "room": {"north": 19, "east": 14},
  #   "requires": [["quest:hWater.?"]],
  #   "receive": ["quest:hWater.?"],
  # },
  # {
  #   "room": {"north": 16, "east": 14},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 16, "east": 14},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 16},
  #   "requires": [["quest:rings.?"]],
  #   "receive": ["quest:rings.?"],
  # },
  # {
  #   "room": {"north": 12, "east": 14},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 18},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 18},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 18},
  #   "requires": [["quest:bBomb.?"]],
  #   "receive": ["quest:bBomb.?"],
  # },
  # {
  #   "room": {"north": 14, "east": 18},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 17},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 17},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 17},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 25},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 15, "east": 24},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 23},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 15},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 15},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 10, "east": 15},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 21},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 21},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 17, "east": 19},
  #   "requires": [["quest:oMan.?"]],
  #   "receive": ["quest:oMan.?"],
  # },
  # {
  #   "room": {"north": 18, "east": 19},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 18, "east": 22},
  #   "requires": [["quest:gTree.?"]],
  #   "receive": ["quest:gTree.?"],
  # },
  # {
  #   "room": {"north": 11, "east": 23},
  #   "requires": [["quest:dream.?"]],
  #   "receive": ["quest:dream.?"],
  # },
  # {
  #   "room": {"north": 7, "east": 28},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 8, "east": 21},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 13, "east": 14},
  #   "requires": [["quest:mChal.?"]],
  #   "receive": ["quest:mChal.?"],
  # },
  # {
  #   "room": {"north": 3, "east": 20},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 3, "east": 19},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  # {
  #   "room": {"north": 4, "east": 19},
  #   "requires": [["quest:isles.?"]],
  #   "receive": ["quest:isles.?"],
  # },
  {
    "room": {"north": 19, "east": 21},
    "requires": [[]],
    "receive": ["quest:dig.1"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["skill:dig", "quest:dig.1"]],
    "receive": ["misc:small locket", "quest:dig.2"],
  },
  {
    "room": {"north": 19, "east": 21},
    "requires": [["misc:small locket", "quest:dig.2"]],
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
    "requires": [["quest:gTree.14", "item:scorpiion claw#7", "item:cobra fang#5"]],
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
    "requires": [["item:fire crystal"]],
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
    "receive": ["quest:gTree.16"],
  },
  {
    "room": {"north": 7, "east": 10},
    "requires": [["quest:gTree.16", "permit:bomb"]],
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
    "receive": ["quest:gTree.23", "goal:boss dead"],
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
    "room": {"north": 20, "east": 20},
    "requires": [["quest:canteen.1"]],
    "receive": ["quest:canteen.2"],
    # TODO
    "info": "not 20 20 but anywhere with water",
  },
  {
    "room": {"north": 12, "east": 11},
    "requires": [["quest:canteen.2"]],
    "receive": ["quest:canteen.3", "item:diamnond#1"],
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
    "receive": ["ring.evasion"],
  },
  {
    "room": {"north": 20, "east": 20},
    "requires": [[]],
    "receive": ["item:cotton thread", "item:shadow crest", "item:orc coin"],
    # TODO sort mob drops
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
        "misc:geomana",
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
    "receive": ["quest:rings.13"],
  },
]
