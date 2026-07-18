from __future__ import annotations
from typing import Literal, NotRequired, TypedDict


class ExitBase(TypedDict):
  north: int | float
  east: int | float
  exits: ExitNode
  areas: NotRequired[list[AreaNode],]
  err: NotRequired[bool]


class ExitNode(TypedDict):
  west: list[DirNodeLR]
  east: list[DirNodeLR]
  north: list[DirNodeUD]
  south: list[DirNodeUD]
  warp: NotRequired[list[Pos],]


class Pos(TypedDict):
  north: int | float
  east: int | float


class DirNodeLR(TypedDict):
  top: int
  bottom: int
  newX: NotRequired[int]
  newY: NotRequired[int]


class DirNodeUD(TypedDict):
  left: int
  right: int
  newX: NotRequired[int]
  newY: NotRequired[int]


class AreaNode(TypedDict):
  reqs: list[list[str],]
  areas: list[list[AreaAreaNode],]


class AreaAreaNode(TypedDict):
  side: Literal[
    "east",
    "west",
    "south",
    "north",
  ]
  idx: int


GEOM: list[ExitBase] = [
  {
    "north": -1,
    "east": -1,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 3,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 23,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [
        {"left": 6, "right": 8},
      ],
    },
  },
  {
    "north": 3,
    "east": 24,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "west", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
          ],
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 5, "bottom": 6},
        {"top": 9, "bottom": 9},
      ],
      "north": [
        {"left": 6, "right": 7, "newY": 89},
      ],
    },
  },
  {
    "north": 3,
    "east": 25,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 1},
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 1},
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
        {"top": 9, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [
        {"left": 11, "right": 12},
      ],
    },
  },
  {
    "north": 3,
    "east": 26,
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 4, "right": 4},
        {"left": 6, "right": 6},
        {"left": 8, "right": 8},
        {"left": 10, "right": 10},
        {"left": 12, "right": 12},
      ],
    },
  },
  {
    "north": 4,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 23,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 8},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 8},
      ],
    },
  },
  {
    "north": 4,
    "east": 24,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 7, "right": 7},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [
        {"left": 11, "right": 11, "newY": 88},
      ],
    },
  },
  {
    "north": 4,
    "east": 25,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 11, "right": 12},
      ],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 4,
    "east": 26,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "south", "idx": 1},
            {"side": "south", "idx": 3},
          ],
          [
            {"side": "south", "idx": 2},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 4},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 2},
          ],
          [
            {"side": "south", "idx": 3},
          ],
          [
            {"side": "south", "idx": 4},
          ],
          [
            {"side": "south", "idx": 0},
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
      ],
      "south": [
        {"left": 4, "right": 4},
        {"left": 6, "right": 6},
        {"left": 8, "right": 8},
        {"left": 10, "right": 10},
        {"left": 12, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 9,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 2},
          ],
          [
            {"side": "east", "idx": 0},
            {"side": "east", "idx": 1},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 5,
    "east": 10,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "west", "idx": 1},
          ],
          [
            {"side": "west", "idx": 2},
            {"side": "east", "idx": 2},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 2},
            {"side": "east", "idx": 2},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "west", "idx": 1},
          ],
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 2},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 2},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 10, "right": 11},
      ],
    },
  },
  {
    "north": 5,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 8},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 11, "right": 11},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 9,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 6,
    "east": 10,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 11,
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newY": 94},
      ],
    },
  },
  {
    "north": 6,
    "east": 12,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 6,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 6,
    "east": 23,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 8, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 8},
      ],
    },
  },
  {
    "north": 7,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 11,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 12,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 7,
    "east": 18,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 20,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 7,
    "east": 21,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [
        {"top": 1, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 22,
    "areas": [
      {
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
        "reqs": [
          [
            "permit:shadowsoulEntrance",
            "weapon:royalSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:sunSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:shadowStaff",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:refreshStaff",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:orcBlade",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:creeperCrusher",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:twinFury",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:baneBlade",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:axe",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:bombSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:soulSword",
          ],
        ],
      },
      {
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
        "reqs": [
          [],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 3, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 23,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [
        {"left": 8, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 8},
      ],
      "east": [
        {"top": 4, "bottom": 5},
      ],
      "north": [
        {"left": 0, "right": 8},
      ],
    },
  },
  {
    "north": 7,
    "east": 25,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 9,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 8,
    "east": 10,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "east", "idx": 1},
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "east", "idx": 2},
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 5},
        {"top": 7, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 9},
        {"left": 11, "right": 13},
      ],
    },
  },
  {
    "north": 8,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 2},
            {"side": "east", "idx": 0},
            {"side": "west", "idx": 2},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
            {"side": "west", "idx": 1},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 5},
        {"top": 7, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
    },
  },
  {
    "north": 8,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 3, "bottom": 5},
      ],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 8,
    "east": 13,
    "exits": {
      "west": [
        {"top": 3, "bottom": 5},
      ],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 14,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 4, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 15,
    "exits": {
      "west": [
        {"top": 4, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 4},
      ],
    },
  },
  {
    "north": 8,
    "east": 16,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 17,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [
        {"left": 1, "right": 2},
        {"left": 11, "right": 12},
      ],
    },
  },
  {
    "north": 8,
    "east": 18,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 1},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "east", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [
        {"left": 6, "right": 7},
        {"left": 10, "right": 12},
      ],
    },
  },
  {
    "north": 8,
    "east": 19,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 12, "right": 12},
      ],
    },
  },
  {
    "north": 8,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 8, "newY": 144},
      ],
    },
  },
  {
    "north": 8,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 6, "bottom": 7},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 22,
    "exits": {
      "west": [
        {"top": 6, "bottom": 7},
      ],
      "south": [
        {"left": 3, "right": 13},
      ],
      "east": [
        {"top": 3, "bottom": 10},
      ],
      "north": [
        {"left": 7, "right": 9},
      ],
    },
  },
  {
    "north": 8,
    "east": 23,
    "exits": {
      "west": [
        {"top": 3, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 8,
    "east": 25,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 9,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 9,
    "east": 10,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 9},
        {"left": 11, "right": 13},
      ],
      "east": [
        {"top": 7, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 9,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "north", "idx": 2},
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 2},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 7, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
    },
  },
  {
    "north": 9,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 4},
      ],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 9,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 9,
    "east": 18,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 1},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4},
        {"top": 6, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 7},
        {"left": 10, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 12},
      ],
    },
  },
  {
    "north": 9,
    "east": 19,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [
            "flag:green secret code",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 12, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 9,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 9},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 9,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 22,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 7, "right": 9},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 5},
        {"left": 7, "right": 9},
      ],
    },
  },
  {
    "north": 9,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 2, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 24,
    "exits": {
      "west": [
        {"top": 2, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 2, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 12},
      ],
    },
  },
  {
    "north": 9,
    "east": 25,
    "areas": [
      {
        "reqs": [
          [
            "quest:curse.5",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 26,
    "areas": [
      {
        "reqs": [
          [
            "flag:magic only resist bypass",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newY": 148},
      ],
    },
  },
  {
    "north": 10,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 5},
        {"top": 7, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 10,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 2},
            {"side": "north", "idx": 2},
            {"side": "north", "idx": 1},
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
    },
  },
  {
    "north": 10,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 10,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 10,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 4, "bottom": 10},
      ],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 10,
    "east": 16,
    "exits": {
      "west": [
        {"top": 3, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 10,
    "east": 18,
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 12},
      ],
    },
  },
  {
    "north": 10,
    "east": 19,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 20,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 1},
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 1},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [
        {"left": 3, "right": 4},
        {"left": 11, "right": 12},
      ],
    },
  },
  {
    "north": 10,
    "east": 22,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 1},
            {"side": "south", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "south", "idx": 1},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 5},
        {"left": 7, "right": 9},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 23,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 7, "right": 11},
      ],
    },
  },
  {
    "north": 10,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 4},
      ],
    },
  },
  {
    "north": 10,
    "east": 25,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 2},
      ],
    },
  },
  {
    "north": 10,
    "east": 26,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 10,
    "east": 21,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 9,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 11,
    "east": 10,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 1},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [
        {"top": 0, "bottom": 3},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 11,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "south", "idx": 2},
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 2},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3},
      ],
      "south": [
        {"left": 1, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 5},
        {"left": 7, "right": 8},
        {"left": 10, "right": 13},
      ],
    },
  },
  {
    "north": 11,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 11,
    "east": 13,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1},
      ],
    },
  },
  {
    "north": 11,
    "east": 14,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 9},
      ],
    },
  },
  {
    "north": 11,
    "east": 15,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 11,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 17,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
            {"side": "west", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 18,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 10, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 19,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "east", "idx": 1},
          ],
          [
            {"side": "east", "idx": 2},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
          ],
          [
            {"side": "east", "idx": 2},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3},
        {"top": 5, "bottom": 6},
        {"top": 8, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 20,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 2},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 1},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
        {"top": 5, "bottom": 6},
        {"top": 8, "bottom": 9},
      ],
      "south": [
        {"left": 3, "right": 4},
        {"left": 11, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 7, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 4},
      ],
    },
  },
  {
    "north": 11,
    "east": 24,
    "areas": [
      {
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
        "reqs": [
          [
            "permit:shadowsoulEntrance",
            "weapon:royalSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:sunSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:shadowStaff",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:refreshStaff",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:orcBlade",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:creeperCrusher",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:twinFury",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:baneBlade",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:axe",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:bombSword",
          ],
          [
            "permit:shadowsoulEntrance",
            "weapon:soulSword",
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 4},
      ],
      "east": [
        {"top": 6, "bottom": 7},
      ],
      "north": [
        {"left": 3, "right": 4},
      ],
    },
  },
  {
    "north": 9.11,
    "east": 20,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 25,
    "exits": {
      "west": [
        {"top": 6, "bottom": 7},
      ],
      "south": [
        {"left": 1, "right": 2},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 26,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 12,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 2},
            {"side": "east", "idx": 1},
          ],
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 5},
        {"left": 7, "right": 8},
        {"left": 10, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 4},
        {"top": 6, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 12,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 4},
        {"top": 6, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 14,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 9},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 16,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 1},
        {"top": 5, "bottom": 9},
      ],
      "north": [
        {"left": 11, "right": 11},
      ],
    },
  },
  {
    "north": 12,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 1},
        {"top": 5, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 18,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8},
      ],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 12,
    "east": 19,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3},
      ],
      "north": [
        {"left": 10, "right": 10, "newY": 129},
      ],
    },
  },
  {
    "north": 12,
    "east": 21,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 11, "right": 11, "newY": 107},
      ],
    },
  },
  {
    "north": 12,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 12,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 4},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [
        {"left": 10, "right": 11},
      ],
    },
  },
  {
    "north": 12,
    "east": 24,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 3, "right": 4},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 25,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3},
      ],
      "north": [
        {"left": 5, "right": 8},
      ],
    },
  },
  {
    "north": 12,
    "east": 26,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [
            "flag:stomp code",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ]
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
      ],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 6},
      ],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 14,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 9, "right": 10},
      ],
    },
  },
  {
    "north": 13,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 5},
      ],
      "east": [
        {"top": 2, "bottom": 2},
      ],
      "north": [
        {"left": 2, "right": 2},
      ],
    },
  },
  {
    "north": 13,
    "east": 16,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 2},
      ],
      "south": [
        {"left": 11, "right": 11},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 17,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 6, "bottom": 7},
      ],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 13,
    "east": 18,
    "exits": {
      "west": [
        {"top": 6, "bottom": 7},
      ],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 13,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 13,
    "east": 20,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 13,
    "east": 21,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 11, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 10},
      ],
    },
  },
  {
    "north": 13,
    "east": 22,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11},
      ],
    },
  },
  {
    "north": 13,
    "east": 24,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 1, "right": 9},
      ],
    },
  },
  {
    "north": 13,
    "east": 25,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 5, "right": 8},
      ],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 5, "right": 8},
      ],
    },
  },
  {
    "north": 13,
    "east": 26,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 14,
    "exits": {
      "west": [
        {"top": 2, "bottom": 9},
      ],
      "south": [
        {"left": 9, "right": 10},
      ],
      "east": [
        {"top": 2, "bottom": 2},
      ],
      "north": [
        {"left": 5, "right": 5},
      ],
    },
  },
  {
    "north": 14,
    "east": 15,
    "exits": {
      "west": [
        {"top": 2, "bottom": 2},
      ],
      "south": [
        {"left": 2, "right": 2},
      ],
      "east": [
        {"top": 7, "bottom": 7},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 16,
    "exits": {
      "west": [
        {"top": 7, "bottom": 7},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 5},
      ],
    },
  },
  {
    "north": 14,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 9},
      ],
    },
  },
  {
    "north": 14,
    "east": 18,
    "areas": [
      {
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ]
        ],
        "reqs": [
          [
            "quest:gTree.10",
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 8, "newY": 85},
      ],
    },
  },
  {
    "north": 14,
    "east": 19,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 10},
      ],
    },
  },
  {
    "north": 14,
    "east": 20,
    "areas": [
      {
        "reqs": [
          [
            "weapon:sword",
          ],
          [
            "weapon:sKnife",
          ],
          [
            "weapon:sKnife",
          ],
          [
            "weapon:sKnife",
          ],
          [
            "weapon:pitchfork",
          ],
          [
            "weapon:royalSword",
          ],
          [
            "weapon:sunSword",
          ],
          [
            "weapon:shadowStaff",
          ],
          [
            "weapon:refreshStaff",
          ],
          [
            "weapon:orcBlade",
          ],
          [
            "weapon:creeperCrusher",
          ],
          [
            "weapon:twinFury",
          ],
          [
            "weapon:baneBlade",
          ],
          [
            "weapon:axe",
          ],
          [
            "weapon:bombSword",
          ],
          [
            "weapon:soulSword",
          ],
          [
            "quest:gTree.7",
          ],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 14,
    "east": 21,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 10},
      ],
      "east": [],
      "north": [
        {"left": 12, "right": 12},
      ],
    },
  },
  {
    "north": 14,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 7, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 23,
    "exits": {
      "west": [
        {"top": 7, "bottom": 9},
      ],
      "south": [
        {"left": 10, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 4},
        {"left": 6, "right": 7},
        {"left": 10, "right": 10},
      ],
    },
  },
  {
    "north": 14,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 9},
      ],
      "east": [
        {"top": 1, "bottom": 1},
        {"top": 3, "bottom": 3},
        {"top": 5, "bottom": 5},
        {"top": 7, "bottom": 7},
        {"top": 9, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 25,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 2},
            {"side": "west", "idx": 3},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 4},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 1},
        {"top": 3, "bottom": 3},
        {"top": 5, "bottom": 5},
        {"top": 7, "bottom": 7},
        {"top": 9, "bottom": 9},
      ],
      "south": [
        {"left": 5, "right": 8},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 14,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 5},
      ],
      "east": [
        {"top": 3, "bottom": 6},
      ],
      "north": [
        {"left": 2, "right": 2},
      ],
    },
  },
  {
    "north": 15,
    "east": 15,
    "exits": {
      "west": [
        {"top": 3, "bottom": 6},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 4},
      ],
      "north": [
        {"left": 4, "right": 4},
      ],
    },
  },
  {
    "north": 15,
    "east": 16,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4},
      ],
      "south": [
        {"left": 5, "right": 5},
      ],
      "east": [],
      "north": [
        {"left": 12, "right": 12},
      ],
    },
  },
  {
    "north": 15,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 9},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 18,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 8},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 19,
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 10},
      ],
      "east": [],
      "north": [
        {"left": 2, "right": 2},
      ],
    },
  },
  {
    "north": 15,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 15,
    "east": 21,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [
        {"left": 12, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 5},
      ],
      "north": [
        {"left": 2, "right": 2, "newY": 129},
      ],
    },
  },
  {
    "north": 15,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5},
      ],
      "south": [
        {"left": 4, "right": 4},
        {"left": 6, "right": 7},
        {"left": 10, "right": 10},
      ],
      "east": [
        {"top": 1, "bottom": 2},
      ],
      "north": [
        {"left": 1, "right": 1},
      ],
    },
  },
  {
    "north": 15,
    "east": 24,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "north", "idx": 1},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1},
        {"left": 9, "right": 12},
      ],
    },
  },
  {
    "north": 15,
    "east": 25,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6},
        {"left": 8, "right": 9},
      ],
    },
  },
  {
    "north": 16,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 6, "bottom": 8},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 11,
    "exits": {
      "west": [
        {"top": 6, "bottom": 8},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 3, "right": 4},
      ],
    },
  },
  {
    "north": 16,
    "east": 14,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [
            "quest:gTree.22",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 2, "right": 2},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 4, "newY": 125},
      ],
    },
  },
  {
    "north": 16,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 4},
      ],
      "east": [],
      "north": [
        {"left": 7, "right": 8},
      ],
    },
  },
  {
    "north": 16,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 12, "right": 12},
      ],
      "east": [
        {"top": 5, "bottom": 7},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 17,
    "exits": {
      "west": [
        {"top": 5, "bottom": 7},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 10, "right": 10},
      ],
    },
  },
  {
    "north": 16,
    "east": 18,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 1},
      ],
      "north": [
        {"left": 1, "right": 1},
      ],
    },
  },
  {
    "north": 16,
    "east": 19,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [
            "permit:bomb.2",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 1},
      ],
      "south": [
        {"left": 2, "right": 2},
      ],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 21,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 22,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
      ],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11},
      ],
    },
  },
  {
    "north": 16,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 1},
      ],
    },
  },
  {
    "north": 16,
    "east": 24,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "north", "idx": 1},
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1},
        {"left": 9, "right": 12},
      ],
      "east": [
        {"top": 3, "bottom": 6},
      ],
      "north": [
        {"left": 1, "right": 3},
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 16,
    "east": 25,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 1},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 3, "bottom": 6},
      ],
      "south": [
        {"left": 5, "right": 6},
        {"left": 8, "right": 9},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 9},
      ],
    },
  },
  {
    "north": 17,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 4},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 11,
    "exits": {
      "west": [
        {"top": 4, "bottom": 4},
      ],
      "south": [
        {"left": 3, "right": 4},
      ],
      "east": [],
      # "east": [{"top": 4, "bottom": 4},],
      "north": [
        {"left": 3, "right": 4},
      ],
    },
  },
  {
    "north": 17,
    "east": 14,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 7, "right": 8},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 7},
        {"left": 9, "right": 11},
      ],
    },
  },
  {
    "north": 17,
    "east": 16,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 17,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
      ],
      "south": [
        {"left": 10, "right": 10},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 18,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 3, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 20,
    "exits": {
      "west": [
        {"top": 3, "bottom": 6},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 17,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 5, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 22,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6},
      ],
      "south": [
        {"left": 10, "right": 11},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1},
      ],
      "east": [],
      "north": [
        {"left": 9, "right": 10},
      ],
    },
  },
  {
    "north": 17,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 3},
        {"left": 5, "right": 6},
      ],
      "east": [
        {"top": 1, "bottom": 2},
        {"top": 5, "bottom": 6},
        {"top": 8, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 25,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "west", "idx": 2},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
        {"top": 5, "bottom": 6},
        {"top": 8, "bottom": 9},
      ],
      "south": [
        {"left": 8, "right": 9},
      ],
      "east": [],
      "north": [
        {"left": 11, "right": 12},
      ],
    },
  },
  {
    "north": 18,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8},
      ],
      "north": [
        {"left": 1, "right": 2},
      ],
    },
  },
  {
    "north": 18,
    "east": 11,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8},
      ],
      "south": [
        {"left": 3, "right": 4},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 12,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 8, "right": 8},
      ],
    },
  },
  {
    "north": 18,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 18,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 18,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 7},
        {"left": 9, "right": 11},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 17,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newY": 309},
      ],
      "east": [
        {"top": 4, "bottom": 4},
      ],
      "north": [
        {"left": 4, "right": 5},
        {"left": 7, "right": 8},
      ],
    },
  },
  {
    "north": 18,
    "east": 18,
    "exits": {
      "west": [
        {"top": 4, "bottom": 4},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1},
        {"left": 11, "right": 11},
      ],
    },
  },
  {
    "north": 18,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9},
      ],
      "south": [
        {"left": 5, "right": 6},
      ],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [
        {"left": 1, "right": 12},
      ],
    },
  },
  {
    "north": 18,
    "east": 21,
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 4},
      ],
      "north": [
        {"left": 3, "right": 3},
        {"left": 8, "right": 8},
      ],
    },
  },
  {
    "north": 18,
    "east": 22,
    "areas": [
      {
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
        "reqs": [
          [
            "quest:gTree.3",
          ],
        ],
      },
      {
        "areas": [
          [
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "east", "idx": 0},
          ],
        ],
        "reqs": [
          [],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 23,
    "exits": {
      "west": [
        {"top": 1, "bottom": 9},
      ],
      "south": [
        {"left": 9, "right": 10},
      ],
      "east": [
        {"top": 7, "bottom": 8},
      ],
      "north": [
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 18,
    "east": 24,
    "exits": {
      "west": [
        {"top": 7, "bottom": 8},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 25,
    "exits": {
      "west": [],
      "south": [
        {"left": 11, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 10,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 2},
      ],
      "east": [
        {"top": 2, "bottom": 3},
      ],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 11,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 12,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 8},
      ],
      "east": [
        {"top": 3, "bottom": 7},
      ],
      "north": [
        {"left": 3, "right": 9},
      ],
    },
  },
  {
    "north": 19,
    "east": 13,
    "exits": {
      "west": [
        {"top": 3, "bottom": 7},
      ],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [
        {"top": 5, "bottom": 5, "newX": 600},
      ],
      "north": [],
    },
    "err": True,
  },
  {
    "north": 19,
    "east": 15,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 19,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newY": 200},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 17,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "south", "idx": 1},
            {"side": "east", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
        {"left": 7, "right": 8},
      ],
      "east": [
        {"top": 3, "bottom": 3},
      ],
      "north": [
        {"left": 1, "right": 8},
      ],
    },
  },
  {
    "north": 19,
    "east": 18,
    "areas": [
      {
        "reqs": [
          [
            "quest:rings.10",
          ],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 1},
          ],
          [
            {"side": "south", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "south", "idx": 1},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 3, "bottom": 3},
      ],
      "south": [
        {"left": 1, "right": 1},
        {"left": 11, "right": 11},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 12},
      ],
    },
  },
  {
    "north": 19,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 19,
    "east": 21,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 3},
        {"left": 8, "right": 8},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 6},
      ],
      "east": [
        {"top": 4, "bottom": 5},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 19,
    "east": 24,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5},
      ],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 12,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 9},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  # {
  #   "north": 20,
  #   "east": 16,
  #   "exits": {"west": [], "south": [], "east": [], "north": [],},
  # },
  # hard to make entrance rando work for 20 16 so it's gonna be unmodified and everything will be said to be in 19 16 instead
  {
    "north": 20,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 8},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 18,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
        {"left": 8, "right": 8},
        {"left": 10, "right": 10},
      ],
    },
  },
  {
    "north": 20,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 20,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 22,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb.2",
          ],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3},
      ],
      "north": [
        {"left": 8, "right": 9},
      ],
    },
  },
  {
    "north": 20,
    "east": 23,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3},
      ],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11},
      ],
    },
  },
  {
    "north": 21,
    "east": 9,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 21,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 21,
    "east": 12,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 7, "newY": 172, "newX": 308},
      ],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 13,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "east", "idx": 1},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 14,
    "exits": {
      "west": [
        {"top": 2, "bottom": 5},
        {"top": 7, "bottom": 8},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 11, "right": 12},
      ],
    },
  },
  {
    "north": 21,
    "east": 17,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 1},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 18,
    "exits": {
      "west": [
        {"top": 1, "bottom": 1},
      ],
      "south": [
        {"left": 6, "right": 6},
        {"left": 8, "right": 8},
        {"left": 10, "right": 10},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 9, "bottom": 9},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 21,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "east", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5},
      ],
      "south": [
        {"left": 10, "right": 11},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 22,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 22,
    "east": 10,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 22,
    "east": 11,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 22,
    "east": 12,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 22,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 22,
    "east": 14,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 11, "right": 12},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 23,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 23,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 23,
    "east": 11,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 23,
    "east": 12,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7},
      ],
    },
  },
  {
    "north": 23,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 23,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 6, "right": 6},
      ],
    },
  },
  {
    "north": 24,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2},
      ],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 11,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "west", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
      ],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 12,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7},
      ],
      "east": [
        {"top": 2, "bottom": 4},
      ],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 13,
    "exits": {
      "west": [
        {"top": 2, "bottom": 4},
      ],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 14,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 100,
    "east": 100,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12, "newX": 260, "newY": 315},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 200,
    "east": 200,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 4, "right": 9, "newY": 204},
      ],
    },
  },
  {
    "north": 201,
    "east": 200,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10.1,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 300,
    "east": 300,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12, "newX": 337, "newY": 132},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 500,
    "east": 500,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 8, "right": 10},
      ],
    },
  },
  {
    "north": 500,
    "east": 501,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6},
      ],
    },
  },
  {
    "north": 501,
    "east": 500,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 10},
      ],
      "east": [
        {"top": 1, "bottom": 4},
      ],
      "north": [],
    },
  },
  {
    "north": 501,
    "east": 501,
    "exits": {
      "west": [
        {"top": 1, "bottom": 4},
      ],
      "south": [
        {"left": 5, "right": 6},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 4,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 3,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 4,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 4,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 6,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 5,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 3,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 1, "right": 13},
      ],
    },
  },
  {
    "north": 7,
    "east": 19,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 0, "bottom": 10},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 9,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 2},
        {"left": 11, "right": 12},
      ],
      "east": [
        {"top": 4, "bottom": 4},
        {"top": 6, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 8,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 8},
      ],
      "east": [
        {"top": 0, "bottom": 9},
      ],
      "north": [
        {"left": 0, "right": 13},
      ],
    },
  },
  {
    "north": 21,
    "east": 22,
    "exits": {
      "west": [
        {"top": 1, "bottom": 2},
      ],
      "south": [
        {"left": 8, "right": 9},
      ],
      "east": [
        {"top": 4, "bottom": 5},
      ],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 14,
    "exits": {
      "west": [
        {"top": 6, "bottom": 6},
      ],
      "south": [
        {"left": 6, "right": 6},
      ],
      "east": [],
      "north": [],
    },
    "err": True,
  },
  {
    "north": 9,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 12,
    "east": 10,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 13},
      ],
      "east": [
        {"top": 1, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 10,
    "areas": [
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [
            {"side": "west", "idx": 1},
            {"side": "south", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 5},
        {"top": 7, "bottom": 10},
      ],
      "south": [
        {"left": 0, "right": 12},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12},
      ],
    },
  },
  {
    "north": 21,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6},
      ],
      "north": [
        {"left": 6, "right": 7},
      ],
    },
  },
  {
    "north": 12,
    "east": 13,
    "areas": [
      {
        "reqs": [
          [
            "permit:bomb",
          ],
        ],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "south", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {"side": "south", "idx": 0},
          ],
          [
            {"side": "north", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 6},
      ],
    },
  },
  {
    "north": 12,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5},
      ],
      "east": [
        {"top": 1, "bottom": 9},
      ],
      "north": [
        {"left": 5, "right": 5},
      ],
    },
  },
  {
    "north": 14,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 10},
      ],
      "north": [],
    },
  },
  {
    "north": 17.1,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [],
    },
  },
]


class Warp(TypedDict):
  reqs: NotRequired[list[list[str]]]
  connections: tuple[tuple[float | int, float | int, Literal["north", "south", "west", "east", "root"], int], ...]


WARPS: tuple[Warp, ...] = (
  {
    "reqs": [["permit:volcano"]],
    "connections": ((17, 17, "south", 0), (17, 17, "west", 0), (18, 17, "south", 0)),
  },
  {
    "connections": ((4, 13, "root", 0), (100, 100, "south", 0)),
  },
  {
    "connections": ((3, 16, "root", 0), (200, 200, "north", 0)),
  },
  {
    "connections": ((200, 200, "root", 0), (201, 200, "root", 0)),
  },
  {
    "reqs": [["magic:drain", "quest:aSword.1"]],
    "connections": ((18, 25, "root", 0), (500, 500, "north", 0)),
  },
  {
    "connections": ((6, 21, "root", 0), (300, 300, "south", 0)),
  },
  {
    "connections": ((10, 16, "root", 0), (11, 16, "south", 0)),
  },
  {
    "reqs": [["permit:bomb"]],
    "connections": ((11, 13, "root", 0), (11, 14, "south", 0)),
  },
  {
    "connections": ((11, 14, "root", 0), (9, 13, "root", 0)),
  },
  {
    "reqs": [["magic:drain"]],
    "connections": ((9, 13, "root", 0), (10, 13, "root", 0), (9, 14, "root", 0)),
  },
  {
    "reqs": [["magic:drain"]],
    "connections": ((9, 14, "root", 0), (10, 14, "north", 0)),
  },
  {
    "reqs": [["misc:fire crystal"]],
    "connections": ((8, 9, "root", 0), (7, 9, "south", 0)),
  },
  {
    "reqs": [["flag:lit torch 2", "flag:lit torch 1"]],
    "connections": ((6, 23, "root", 0), (5, 23, "south", 0)),
  },
  {
    "connections": ((17, 14, "south", 0), (18, 14, "north", 0)),
  },
  {
    "connections": ((20, 12, "root", 0), (21, 12, "south", 0)),
  },
  {
    "connections": ((22, 10, "root", 0), (22, 13, "east", 0), (22, 13, "north", 0)),
  },
  {
    "connections": ((21, 13, "east", 0), (22, 11, "south", 0), (22, 11, "north", 0)),
  },
  {
    "connections": ((22, 12, "root", 0), (21, 9, "north", 0)),
  },
  {
    "connections": ((18, 12, "north", 0), (18, 11, "west", 0)),
  },
  {
    "reqs": [["permit:bomb"]],
    "connections": ((10, 12, "root", 0), (7, 12, "south", 0)),
  },
  {
    "reqs": [["permit:bomb"]],
    "connections": ((12, 21, "west", 0), (11, 21, "root", 0)),
  },
  {
    "connections": ((18, 16, "root", 0), (19, 16, "south", 0)),
  },
  {
    "connections": ((19, 16, "south", 0), (19, 15, "north", 0)),
  },
  {
    "connections": ((9, 22, "north", 0), (9, 21, "root", 0)),
  },
  {
    "reqs": [["permit:bomb.2"]],
    "connections": ((12, 14, "root", 0), (9, 21, "root", 0)),
  },
  {
    "connections": ((21, 21, "east", 0), (20, 21, "root", 0)),
  },
  {
    "reqs": [["permit:bomb", "magic:lightning"]],
    "connections": ((20, 21, "root", 0), (19, 22, "root", 0)),
  },
  {
    "reqs": [["permit:bomb.2"]],
    "connections": ((12, 23, "north", 0), (12, 22, "north", 0)),
  },
  {
    "connections": ((24, 10, "east", 0), (23, 14, "north", 0)),
  },
  {
    # TODO !!! why map not show this correctly - should be able to get to 24 13 from 23 10
    "connections": ((24, 13, "south", 0), (23, 10, "root", 0)),
  },
  {
    "reqs": [["quest:gTree.9"]],
    "connections": ((17, 19, "east", 0), (17.1, 19, "root", 0)),
  },
  {
    "reqs": [["quest:gTree.9"]],
    "connections": ((15, 17, "south", 0), (17.1, 19, "root", 0)),
  },
  {
    "reqs": [["flag:10.1 code"]],
    "connections": ((10, 21, "root", 0), (10.1, 21, "root", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (18, 20, "east", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (15, 22, "north", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (12, 19, "east", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (14, 16, "west", 0)),
  },
  {
    "reqs": [["food:sunflowerSeeds"]],
    "connections": ((-1, -1, "root", 0), (11, 12, "east", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (10, 16, "west", 0)),
  },
  {
    "reqs": [["skill:warp"]],
    "connections": ((-1, -1, "root", 0), (12, 10, "south", 0)),
  },
  {
    "reqs": [["skill:warp", "quest:gTree.16"]],
    "connections": ((-1, -1, "root", 0), (7, 9, "south", 0)),
  },
  {
    "reqs": [["skill:warp", "quest:gTree.19"]],
    "connections": ((-1, -1, "root", 0), (11, 24, "east", 0)),
  },
  {
    "reqs": [["skill:warp", "quest:gTree.23"]],
    "connections": ((-1, -1, "root", 0), (19, 12, "east", 0)),
  },
  {
    "connections": ((20, 20, "root", 0), (-1, -1, "root", 0)),
  },
  {
    "connections": ((10.1, 21, "root", 0), (9.11, 20, "root", 0)),
  },
)
