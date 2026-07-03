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
    "north": 3,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
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
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
      ],
      "north": [
        {"left": 6, "right": 8, "newX": 355, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
      ],
      "north": [
        {
          "left": 6,
          "right": 7,
          "newX": 355,
          "newY": 89,
        },
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
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 458},
        {"top": 9, "bottom": 9, "newX": 659, "newY": 280},
      ],
      "south": [],
      "east": [
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
      ],
      "north": [
        {"left": 11, "right": 12, "newX": 583, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 26,
    "exits": {
      "west": [
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 4, "right": 4, "newX": 202, "newY": 509},
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
        {"left": 8, "right": 8, "newX": 405, "newY": 509},
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
        {"left": 12, "right": 12, "newX": 608, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 17,
    "exits": {
      "west": [
        {
          "top": 0,
          "bottom": 10,
        },
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 8, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 6, "right": 8, "newX": 355, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 7, "right": 7, "newX": 329, "newY": 89},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [
        {
          "left": 11,
          "right": 11,
          "newY": 88,
          "newX": 557,
        },
      ],
    },
  },
  {
    "north": 4,
    "east": 25,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 11, "right": 12, "newX": 583, "newY": 0},
      ],
      "east": [
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 3,
            },
          ],
          [
            {
              "side": "south",
              "idx": 2,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 4,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 2,
            },
          ],
          [
            {
              "side": "south",
              "idx": 3,
            },
          ],
          [
            {
              "side": "south",
              "idx": 4,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [
        {"left": 4, "right": 4, "newX": 202, "newY": 0},
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
        {"left": 8, "right": 8, "newX": 405, "newY": 0},
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
        {"left": 12, "right": 12, "newX": 608, "newY": 0},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 2,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 1,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
        {"top": 7, "bottom": 8, "newX": 0, "newY": 381},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 1,
            },
          ],
          [
            {
              "side": "west",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 2,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "west",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 2,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 1,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
        {"top": 7, "bottom": 8, "newX": 659, "newY": 381},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
        {"top": 7, "bottom": 8, "newX": 0, "newY": 381},
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
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 2,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 2,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
        {"top": 7, "bottom": 8, "newX": 659, "newY": 381},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 10, "right": 11, "newX": 532, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 8, "newX": 355, "newY": 0},
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
        {"left": 11, "right": 11, "newX": 557, "newY": 88},
      ],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 10,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
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
        {"left": 10, "right": 11, "newX": 532, "newY": 0},
      ],
      "east": [],
      "north": [
        {
          "left": 6,
          "right": 7,
          "newX": 329,
          "newY": 94,
        },
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
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 19,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
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
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 8, "right": 13, "newX": 532, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 8, "newX": 202, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
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
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 11,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 94},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
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
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 18,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 20,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 21,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 9, "newX": 0, "newY": 254},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
        "reqs": [
          [
            "permit:shadowsoulEntrance",
          ],
        ],
      },
      {
        "areas": [
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
        "reqs": [
          [],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 9, "newX": 659, "newY": 254},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 3, "right": 13, "newX": 405, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 23,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [
        {"left": 8, "right": 13, "newX": 532, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {
          "left": 0,
          "right": 13,
        },
      ],
    },
  },
  {
    "north": 7,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 8, "newX": 202, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 8, "newX": 202, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 25,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
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
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 2,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 3, "newX": 0, "newY": 76},
        {"top": 5, "bottom": 5, "newX": 0, "newY": 254},
        {"top": 7, "bottom": 9, "newX": 0, "newY": 407},
      ],
      "north": [
        {"left": 0, "right": 9, "newX": 228, "newY": 509},
        {"left": 11, "right": 13, "newX": 608, "newY": 509},
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
            {
              "side": "north",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 2,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 1,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3, "newX": 659, "newY": 76},
        {"top": 5, "bottom": 5, "newX": 659, "newY": 254},
        {"top": 7, "bottom": 9, "newX": 659, "newY": 407},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 2, "newX": 50, "newY": 509},
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
        {"left": 7, "right": 13, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 3, "bottom": 5, "newX": 0, "newY": 203},
      ],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 13,
    "exits": {
      "west": [
        {"top": 3, "bottom": 5, "newX": 659, "newY": 203},
      ],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 14,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 10, "newX": 0, "newY": 356},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 15,
    "exits": {
      "west": [
        {"top": 4, "bottom": 10, "newX": 659, "newY": 356},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 1, "right": 4, "newX": 126, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 16,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 1, "right": 2, "newX": 76, "newY": 509},
        {"left": 11, "right": 12, "newX": 583, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
        {"left": 10, "right": 12, "newX": 557, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 19,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 12, "right": 12, "newX": 608, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {
          "left": 8,
          "right": 8,
          "newX": 380,
          "newY": 144,
        },
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
        {"top": 6, "bottom": 7, "newX": 0, "newY": 330},
      ],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 22,
    "exits": {
      "west": [
        {"top": 6, "bottom": 7, "newX": 659, "newY": 330},
      ],
      "south": [
        {"left": 3, "right": 13, "newX": 405, "newY": 0},
      ],
      "east": [
        {"top": 3, "bottom": 10, "newX": 0, "newY": 330},
      ],
      "north": [
        {"left": 7, "right": 9, "newX": 405, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 23,
    "exits": {
      "west": [
        {"top": 3, "bottom": 10, "newX": 659, "newY": 330},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 25,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 10,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 9, "newX": 228, "newY": 0},
        {"left": 11, "right": 13, "newX": 608, "newY": 0},
      ],
      "east": [
        {"top": 7, "bottom": 10, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
          ],
          [
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "north",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 2,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 7, "bottom": 10, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 0, "right": 2, "newX": 50, "newY": 0},
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
        {"left": 7, "right": 13, "newX": 507, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 2, "newX": 76, "newY": 509},
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
        {"left": 7, "right": 13, "newX": 507, "newY": 509},
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
        {"left": 1, "right": 4, "newX": 126, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4, "newX": 659, "newY": 203},
        {"top": 6, "bottom": 6, "newX": 659, "newY": 305},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
        {"left": 10, "right": 12, "newX": 557, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 12, "newX": 557, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 12, "right": 12, "newX": 608, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 9, "newX": 405, "newY": 144},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 7, "right": 9, "newX": 405, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 5, "newX": 152, "newY": 509},
        {"left": 7, "right": 9, "newX": 405, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 10, "newX": 0, "newY": 305},
      ],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 24,
    "exits": {
      "west": [
        {"top": 2, "bottom": 10, "newX": 659, "newY": 305},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 10, "newX": 0, "newY": 305},
      ],
      "north": [
        {"left": 1, "right": 12, "newX": 329, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 10, "newX": 659, "newY": 305},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 26,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [],
      "east": [],
      "north": [
        {
          "left": 6,
          "right": 7,
          "newX": 329,
          "newY": 148,
        },
      ],
    },
  },
  {
    "north": 10,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 5, "newX": 0, "newY": 127},
        {"top": 7, "bottom": 10, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 2,
            },
            {
              "side": "north",
              "idx": 2,
            },
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 2, "newX": 76, "newY": 0},
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
        {"left": 7, "right": 13, "newX": 507, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 2, "newX": 228, "newY": 509},
        {"left": 4, "right": 5, "newX": 76, "newY": 509},
        {"left": 7, "right": 13, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
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
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 10, "newX": 0, "newY": 330},
      ],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 16,
    "exits": {
      "west": [
        {"top": 3, "bottom": 10, "newX": 659, "newY": 356},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
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
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 18,
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 12, "newX": 557, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 12, "newX": 557, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 19,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 1,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
        {"left": 11, "right": 12, "newX": 583, "newY": 509},
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
            {
              "side": "south",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 1,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 5, "newX": 152, "newY": 0},
        {"left": 7, "right": 9, "newX": 405, "newY": 0},
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
        {"left": 7, "right": 11, "newX": 456, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
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
        {"left": 1, "right": 2, "newX": 76, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 26,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 148},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 10,
    "east": 21,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 3, "newX": 0, "newY": 76},
        {"top": 5, "bottom": 10, "newX": 0, "newY": 381},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3, "newX": 659, "newY": 76},
        {"top": 5, "bottom": 10, "newX": 659, "newY": 381},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 3, "newX": 0, "newY": 76},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "south",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 2,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 3, "newX": 659, "newY": 76},
      ],
      "south": [
        {"left": 1, "right": 2, "newX": 76, "newY": 0},
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
        {"left": 7, "right": 13, "newX": 507, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 5, "newX": 126, "newY": 509},
        {"left": 7, "right": 8, "newX": 380, "newY": 509},
        {"left": 10, "right": 13, "newX": 583, "newY": 509},
      ],
    },
  },
  {
    "north": 11,
    "east": 12,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 9, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 11,
    "east": 13,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 9, "newX": 431, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
      ],
    },
  },
  {
    "north": 11,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 10, "right": 12, "newX": 557, "newY": 0},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 1,
            },
          ],
          [
            {
              "side": "east",
              "idx": 2,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
          ],
          [
            {
              "side": "east",
              "idx": 2,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
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
            {
              "side": "west",
              "idx": 2,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 3, "right": 4, "newX": 177, "newY": 0},
        {"left": 11, "right": 12, "newX": 583, "newY": 0},
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
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 7, "right": 11, "newX": 456, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 4, "newX": 126, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
        "reqs": [
          [
            "permit:shadowsoulEntrance",
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 4, "newX": 177, "newY": 0},
      ],
      "east": [
        {
          "top": 6,
          "bottom": 7,
        },
      ],
      "north": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
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
        {"top": 6, "bottom": 7, "newX": 659, "newY": 330},
      ],
      "south": [
        {"left": 1, "right": 2, "newX": 76, "newY": 0},
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
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
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
            {
              "side": "south",
              "idx": 2,
            },
            {
              "side": "east",
              "idx": 1,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 5, "newX": 126, "newY": 0},
        {"left": 7, "right": 8, "newX": 380, "newY": 0},
        {"left": 10, "right": 13, "newX": 583, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 4, "newX": 0, "newY": 127},
        {"top": 6, "bottom": 10, "newX": 0, "newY": 407},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 4, "newX": 659, "newY": 127},
        {"top": 6, "bottom": 10, "newX": 659, "newY": 407},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
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
        {"left": 8, "right": 9, "newX": 431, "newY": 0},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 9, "newX": 659, "newY": 254},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 1, "newX": 0, "newY": 50},
        {"top": 5, "bottom": 9, "newX": 0, "newY": 356},
      ],
      "north": [
        {"left": 11, "right": 11, "newX": 557, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 1, "newX": 659, "newY": 50},
        {"top": 5, "bottom": 9, "newX": 659, "newY": 356},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8, "newX": 0, "newY": 407},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 18,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8, "newX": 659, "newY": 407},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8, "newX": 0, "newY": 407},
      ],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 19,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8, "newX": 659, "newY": 407},
      ],
      "south": [],
      "east": [
        {"top": 8, "bottom": 8, "newX": 0, "newY": 407},
      ],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8, "newX": 659, "newY": 407},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
      ],
      "north": [
        {
          "left": 10,
          "right": 10,
          "newY": 129,
        },
      ],
    },
  },
  {
    "north": 12,
    "east": 21,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
      ],
      "south": [],
      "east": [],
      "north": [
        {
          "left": 11,
          "right": 11,
          "newX": 557,
          "newY": 107,
        },
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
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 4, "newX": 126, "newY": 0},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 10, "right": 11, "newX": 532, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 24,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 3, "right": 4, "newX": 177, "newY": 0},
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
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
      ],
      "north": [
        {"left": 5, "right": 8, "newX": 329, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ]
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
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
        {"left": 3, "right": 6, "newX": 228, "newY": 0},
      ],
      "east": [
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 9, "right": 10, "newX": 481, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 5, "newX": 253, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 2, "newX": 0, "newY": 101},
      ],
      "north": [
        {"left": 2, "right": 2, "newX": 101, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 2, "newX": 659, "newY": 101},
      ],
      "south": [
        {"left": 11, "right": 11, "newX": 557, "newY": 0},
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
        {"top": 6, "bottom": 7, "newX": 0, "newY": 330},
      ],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 18,
    "exits": {
      "west": [
        {"top": 6, "bottom": 7, "newX": 659, "newY": 330},
      ],
      "south": [
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
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
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 20,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 4, "right": 5, "newX": 507, "newY": 129},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 11, "right": 11, "newX": 557, "newY": 107},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 22,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
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
        {"left": 10, "right": 11, "newX": 532, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11, "newX": 532, "newY": 509},
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
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 9, "newX": 253, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 25,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 5, "right": 8, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 5, "right": 8, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 13,
    "east": 26,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
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
        {"top": 2, "bottom": 9, "newX": 659, "newY": 305},
      ],
      "south": [
        {"left": 9, "right": 10, "newX": 481, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 2, "newX": 0, "newY": 101},
      ],
      "north": [
        {"left": 5, "right": 5, "newX": 253, "newY": 509},
      ],
    },
  },
  {
    "north": 14,
    "east": 15,
    "exits": {
      "west": [
        {"top": 2, "bottom": 2, "newX": 659, "newY": 101},
      ],
      "south": [
        {"left": 2, "right": 2, "newX": 101, "newY": 0},
      ],
      "east": [
        {"top": 7, "bottom": 7, "newX": 0, "newY": 356},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 16,
    "exits": {
      "west": [
        {"top": 7, "bottom": 7, "newX": 659, "newY": 356},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 5, "newX": 253, "newY": 509},
      ],
    },
  },
  {
    "north": 14,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 9, "newX": 329, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
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
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 8, "newX": 405, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 14,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 12, "right": 12, "newX": 608, "newY": 509},
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
        {"top": 7, "bottom": 9, "newX": 0, "newY": 407},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 23,
    "exits": {
      "west": [
        {"top": 7, "bottom": 9, "newX": 659, "newY": 407},
      ],
      "south": [
        {"left": 10, "right": 11, "newX": 532, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 4, "right": 4, "newX": 202, "newY": 509},
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 14,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 9, "newX": 253, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 1, "newX": 0, "newY": 50},
        {"top": 3, "bottom": 3, "newX": 0, "newY": 152},
        {"top": 5, "bottom": 5, "newX": 0, "newY": 254},
        {"top": 7, "bottom": 7, "newX": 0, "newY": 356},
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 2,
            },
            {
              "side": "west",
              "idx": 3,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 4,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 1, "newX": 659, "newY": 50},
        {"top": 3, "bottom": 3, "newX": 659, "newY": 152},
        {"top": 5, "bottom": 5, "newX": 659, "newY": 254},
        {"top": 7, "bottom": 7, "newX": 659, "newY": 356},
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [
        {"left": 5, "right": 8, "newX": 329, "newY": 0},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 5, "newX": 253, "newY": 0},
      ],
      "east": [
        {"top": 3, "bottom": 6, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 2, "right": 2, "newX": 101, "newY": 509},
      ],
    },
  },
  {
    "north": 15,
    "east": 15,
    "exits": {
      "west": [
        {"top": 3, "bottom": 6, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 4, "newX": 0, "newY": 203},
      ],
      "north": [
        {"left": 4, "right": 4, "newX": 202, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4, "newX": 659, "newY": 203},
      ],
      "south": [
        {"left": 5, "right": 5, "newX": 253, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 12, "right": 12, "newX": 608, "newY": 509},
      ],
    },
  },
  {
    "north": 15,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 9, "newX": 329, "newY": 0},
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
        {"left": 8, "right": 8, "newX": 405, "newY": 0},
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
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 2, "right": 2, "newX": 101, "newY": 509},
      ],
    },
  },
  {
    "north": 15,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 12, "right": 12, "newX": 608, "newY": 0},
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
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
      ],
      "north": [
        {
          "left": 2,
          "right": 2,
          "newX": 329,
          "newY": 129,
        },
      ],
    },
  },
  {
    "north": 15,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
      ],
      "south": [
        {"left": 4, "right": 4, "newX": 202, "newY": 0},
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
      ],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
      ],
    },
  },
  {
    "north": 15,
    "east": 24,
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
        {"left": 9, "right": 12, "newX": 532, "newY": 509},
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
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
        {"left": 8, "right": 9, "newX": 431, "newY": 509},
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
        {"top": 6, "bottom": 8, "newX": 0, "newY": 356},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 11,
    "exits": {
      "west": [
        {"top": 6, "bottom": 8, "newX": 659, "newY": 356},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
      ],
    },
  },
  {
    "north": 16,
    "east": 14,
    "exits": {
      "west": [],
      "south": [
        {"left": 2, "right": 2, "newX": 101, "newY": 0},
      ],
      "east": [],
      "north": [
        {
          "left": 3,
          "right": 4,
          "newX": 329,
          "newY": 125,
        },
      ],
    },
  },
  {
    "north": 16,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 4, "newX": 202, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 7, "right": 8, "newX": 380, "newY": 509},
      ],
    },
  },
  {
    "north": 16,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {"left": 12, "right": 12, "newX": 608, "newY": 0},
      ],
      "east": [
        {"top": 5, "bottom": 7, "newX": 0, "newY": 305},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 17,
    "exits": {
      "west": [
        {"top": 5, "bottom": 7, "newX": 659, "newY": 305},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
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
        {"top": 1, "bottom": 1, "newX": 0, "newY": 50},
      ],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 1, "newX": 659, "newY": 50},
      ],
      "south": [
        {"left": 2, "right": 2, "newX": 101, "newY": 0},
      ],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 21,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
      ],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 22,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 101, "newY": 129},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11, "newX": 532, "newY": 509},
      ],
    },
  },
  {
    "north": 16,
    "east": 23,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "north",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
        {"left": 9, "right": 12, "newX": 532, "newY": 0},
      ],
      "east": [
        {"top": 3, "bottom": 6, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 1, "right": 3, "newX": 101, "newY": 509},
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
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
            {
              "side": "south",
              "idx": 1,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 3, "bottom": 6, "newX": 659, "newY": 229},
      ],
      "south": [
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
        {"left": 8, "right": 9, "newX": 431, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 8, "right": 9, "newX": 431, "newY": 509},
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
        {"top": 4, "bottom": 4, "newX": 0, "newY": 203},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 11,
    "exits": {
      "west": [
        {"top": 4, "bottom": 4, "newX": 659, "newY": 203},
      ],
      "south": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
      ],
      "east": [],
      # "east": [{"top": 4, "bottom": 4,},],
      "north": [
        {"left": 3, "right": 4, "newX": 177, "newY": 509},
      ],
    },
  },
  {
    "north": 17,
    "east": 14,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 177, "newY": 125},
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
        {"left": 7, "right": 8, "newX": 380, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 7, "newX": 253, "newY": 509},
        {"left": 9, "right": 11, "newX": 507, "newY": 509},
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
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 17,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
      ],
      "south": [
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
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
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
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
        {"top": 3, "bottom": 6, "newX": 0, "newY": 229},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 20,
    "exits": {
      "west": [
        {"top": 3, "bottom": 6, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
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
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 22,
    "exits": {
      "west": [
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 10, "right": 11, "newX": 532, "newY": 0},
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
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 9, "right": 10, "newX": 481, "newY": 509},
      ],
    },
  },
  {
    "north": 17,
    "east": 24,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 3, "newX": 101, "newY": 0},
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
        {"top": 5, "bottom": 6, "newX": 0, "newY": 280},
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
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
            {
              "side": "west",
              "idx": 2,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
        {"top": 5, "bottom": 6, "newX": 659, "newY": 280},
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 8, "right": 9, "newX": 431, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 11, "right": 12, "newX": 583, "newY": 509},
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
        {"top": 8, "bottom": 8, "newX": 0, "newY": 407},
      ],
      "north": [
        {"left": 1, "right": 2, "newX": 76, "newY": 509},
      ],
    },
  },
  {
    "north": 18,
    "east": 11,
    "exits": {
      "west": [
        {"top": 8, "bottom": 8, "newX": 659, "newY": 407},
      ],
      "south": [
        {"left": 3, "right": 4, "newX": 177, "newY": 0},
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
        {"left": 8, "right": 8, "newX": 405, "newY": 509},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 18,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 7, "newX": 253, "newY": 0},
        {"left": 9, "right": 11, "newX": 507, "newY": 0},
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
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
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
            {
              "side": "north",
              "idx": 1,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {
          "left": 6,
          "right": 7,
          "newX": 329,
          "newY": 309,
        },
      ],
      "east": [
        {"top": 4, "bottom": 4, "newX": 0, "newY": 203},
      ],
      "north": [
        {"left": 4, "right": 5, "newX": 228, "newY": 509},
        {"left": 7, "right": 8, "newX": 380, "newY": 509},
      ],
    },
  },
  {
    "north": 18,
    "east": 18,
    "exits": {
      "west": [
        {"top": 4, "bottom": 4, "newX": 659, "newY": 203},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 1, "right": 1, "newX": 50, "newY": 509},
        {"left": 11, "right": 11, "newX": 557, "newY": 509},
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
        {"top": 8, "bottom": 9, "newX": 0, "newY": 432},
      ],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 20,
    "exits": {
      "west": [
        {"top": 8, "bottom": 9, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
      ],
      "east": [
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
      ],
      "north": [
        {"left": 1, "right": 12, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 18,
    "east": 21,
    "exits": {
      "west": [
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 4, "newX": 0, "newY": 203},
      ],
      "north": [
        {"left": 3, "right": 3, "newX": 152, "newY": 509},
        {"left": 8, "right": 8, "newX": 405, "newY": 509},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
        "reqs": [
          [
            "quest:gTree.2",
          ],
        ],
      },
      {
        "areas": [
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
        "reqs": [
          [],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 4, "newX": 659, "newY": 203},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 9, "newX": 0, "newY": 254},
      ],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 23,
    "exits": {
      "west": [
        {"top": 1, "bottom": 9, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 9, "right": 10, "newX": 481, "newY": 0},
      ],
      "east": [
        {"top": 7, "bottom": 8, "newX": 0, "newY": 381},
      ],
      "north": [
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
      ],
    },
  },
  {
    "north": 18,
    "east": 24,
    "exits": {
      "west": [
        {"top": 7, "bottom": 8, "newX": 659, "newY": 381},
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
        {"left": 11, "right": 12, "newX": 583, "newY": 0},
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
        {"left": 1, "right": 2, "newX": 76, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
      ],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 11,
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
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
        {"left": 8, "right": 8, "newX": 405, "newY": 0},
      ],
      "east": [
        {"top": 3, "bottom": 7, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 3, "right": 9, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 19,
    "east": 13,
    "exits": {
      "west": [
        {
          "top": 3,
          "bottom": 7,
        },
      ],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
      ],
      "east": [
        {
          "top": 5,
          "bottom": 5,
          "newY": 305,
          "newX": 600,
        },
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
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
      ],
    },
  },
  {
    "north": 19,
    "east": 16,
    "exits": {
      "west": [],
      "south": [
        {
          "left": 6,
          "right": 7,
          "newX": 329,
          "newY": 200,
        },
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 1,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
        {"left": 7, "right": 8, "newX": 380, "newY": 0},
      ],
      "east": [
        {"top": 3, "bottom": 3, "newX": 0, "newY": 152},
      ],
      "north": [
        {"left": 1, "right": 8, "newX": 228, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 1,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {
          "top": 3,
          "bottom": 3,
        },
      ],
      "south": [
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
        {"left": 11, "right": 11, "newX": 557, "newY": 0},
      ],
      "east": [],
      "north": [
        {
          "left": 8,
          "right": 12,
        },
      ],
    },
  },
  {
    "north": 19,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 12, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 19,
    "east": 21,
    "exits": {
      "west": [],
      "south": [
        {"left": 3, "right": 3, "newX": 152, "newY": 0},
        {"left": 8, "right": 8, "newX": 405, "newY": 0},
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
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 19,
    "east": 24,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
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
        {"left": 3, "right": 9, "newX": 304, "newY": 0},
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
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
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
        {"left": 1, "right": 8, "newX": 228, "newY": 0},
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
        {"left": 8, "right": 12, "newX": 507, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
        {"left": 8, "right": 8, "newX": 405, "newY": 509},
        {"left": 10, "right": 10, "newX": 507, "newY": 509},
      ],
    },
  },
  {
    "north": 20,
    "east": 20,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
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
            {
              "side": "east",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 2, "bottom": 3, "newX": 0, "newY": 127},
      ],
      "north": [
        {"left": 8, "right": 9, "newX": 431, "newY": 509},
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
            {
              "side": "south",
              "idx": 0,
            },
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 2, "bottom": 3, "newX": 659, "newY": 127},
      ],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 10, "right": 11, "newX": 532, "newY": 509},
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
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "east",
              "idx": 0,
            },
          ]
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 21,
    "east": 12,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {
          "left": 6,
          "right": 7,
          "newY": 172,
          "newX": 308,
        },
      ],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
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
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "east",
              "idx": 1,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [],
      "east": [
        {"top": 2, "bottom": 5, "newX": 0, "newY": 178},
        {"top": 7, "bottom": 8, "newX": 0, "newY": 381},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 14,
    "exits": {
      "west": [
        {"top": 2, "bottom": 5, "newX": 659, "newY": 178},
        {"top": 7, "bottom": 8, "newX": 659, "newY": 381},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 11, "right": 12, "newX": 583, "newY": 509},
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
        {"top": 1, "bottom": 1, "newX": 0, "newY": 50},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 18,
    "exits": {
      "west": [
        {"top": 1, "bottom": 1, "newX": 659, "newY": 50},
      ],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
        {"left": 8, "right": 8, "newX": 405, "newY": 0},
        {"left": 10, "right": 10, "newX": 507, "newY": 0},
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
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 9, "bottom": 9, "newX": 0, "newY": 458},
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
            {
              "side": "east",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9, "newX": 659, "newY": 458},
      ],
      "south": [],
      "east": [
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
      ],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 23,
    "exits": {
      "west": [
        {"top": 4, "bottom": 5, "newX": 659, "newY": 229},
      ],
      "south": [
        {"left": 10, "right": 11, "newX": 532, "newY": 0},
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
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 22,
    "east": 10,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
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
        {"left": 6, "right": 7, "newX": 329, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
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
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 22,
    "east": 14,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 11, "right": 12, "newX": 583, "newY": 0},
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
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 23,
    "east": 12,
    "exits": {
      "west": [
        {"top": 4, "bottom": 6, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 5, "right": 7, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 23,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 24,
    "east": 9,
    "exits": {
      "west": [],
      "south": [
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
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
        {"top": 1, "bottom": 2, "newX": 0, "newY": 76},
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
            {
              "side": "west",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
      ],
      "south": [
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
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
        {"left": 5, "right": 7, "newX": 304, "newY": 0},
      ],
      "east": [
        {"top": 2, "bottom": 4, "newX": 0, "newY": 152},
      ],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 13,
    "exits": {
      "west": [
        {"top": 2, "bottom": 4, "newX": 659, "newY": 152},
      ],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
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
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
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
        {
          "left": 1,
          "right": 12,
          "newX": 260,
          "newY": 315,
        },
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
        {"left": 4, "right": 9, "newX": 329, "newY": 204},
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
        {
          "left": 1,
          "right": 12,
          "newX": 337,
          "newY": 132,
        },
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
        {"left": 8, "right": 10, "newX": 456, "newY": 509},
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
        {"left": 5, "right": 6, "newX": 278, "newY": 509},
      ],
    },
  },
  {
    "north": 501,
    "east": 500,
    "exits": {
      "west": [],
      "south": [
        {"left": 8, "right": 10, "newX": 456, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 4, "newX": 0, "newY": 127},
      ],
      "north": [],
    },
  },
  {
    "north": 501,
    "east": 501,
    "exits": {
      "west": [
        {"top": 1, "bottom": 4, "newX": 659, "newY": 127},
      ],
      "south": [
        {"left": 5, "right": 6, "newX": 278, "newY": 0},
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
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 21,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {
          "top": 0,
          "bottom": 10,
        },
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 19,
    "exits": {
      "west": [
        {
          "top": 0,
          "bottom": 10,
        },
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 16,
    "exits": {
      "west": [
        {
          "top": 0,
          "bottom": 10,
        },
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 4,
    "east": 16,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 18,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 17,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {
          "left": 0,
          "right": 13,
        },
      ],
      "east": [
        {
          "top": 0,
          "bottom": 10,
        },
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 17,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 6,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 14,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 5,
    "east": 13,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 13, "newX": 355, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 15,
    "exits": {
      "west": [
        {"top": 0, "bottom": 9, "newX": 659, "newY": 229},
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 3,
    "east": 14,
    "exits": {
      "west": [
        {
          "top": 0,
          "bottom": 9,
        },
      ],
      "south": [],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
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
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 1, "right": 13, "newX": 355, "newY": 509},
      ],
    },
  },
  {
    "north": 7,
    "east": 19,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
      ],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 20,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 10, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 9,
    "east": 17,
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 2, "newX": 76, "newY": 0},
        {"left": 11, "right": 12, "newX": 583, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 4, "newX": 0, "newY": 203},
        {"top": 6, "bottom": 6, "newX": 0, "newY": 305},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 8,
    "east": 24,
    "exits": {
      "west": [
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 8, "newX": 202, "newY": 0},
      ],
      "east": [
        {"top": 0, "bottom": 9, "newX": 0, "newY": 229},
      ],
      "north": [
        {"left": 0, "right": 13, "newX": 329, "newY": 509},
      ],
    },
  },
  {
    "north": 21,
    "east": 22,
    "exits": {
      "west": [
        {"top": 1, "bottom": 2, "newX": 659, "newY": 76},
      ],
      "south": [
        {"left": 8, "right": 9, "newX": 431, "newY": 0},
      ],
      "east": [
        {"top": 4, "bottom": 5, "newX": 0, "newY": 229},
      ],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 14,
    "exits": {
      "west": [
        {"top": 6, "bottom": 6, "newX": 600, "newY": 254},
      ],
      "south": [
        {"left": 6, "right": 6, "newX": 304, "newY": 0},
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
        {"top": 0, "bottom": 10, "newX": 659, "newY": 254},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 10,
    "exits": {
      "west": [
        {"top": 1, "bottom": 10, "newX": 659, "newY": 280},
      ],
      "south": [
        {"left": 0, "right": 13, "newX": 329, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 10, "newX": 0, "newY": 280},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "west",
              "idx": 0,
            },
          ],
          [
            {
              "side": "west",
              "idx": 1,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 0, "bottom": 5, "newX": 659, "newY": 127},
        {"top": 7, "bottom": 10, "newX": 659, "newY": 432},
      ],
      "south": [
        {"left": 0, "right": 12, "newX": 304, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 0, "right": 12, "newX": 304, "newY": 509},
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
        {"top": 4, "bottom": 6, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 6, "right": 7, "newX": 329, "newY": 509},
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
            {
              "side": "north",
              "idx": 0,
            },
            {
              "side": "south",
              "idx": 0,
            },
          ]
        ],
      },
      {
        "reqs": [
          [],
        ],
        "areas": [
          [
            {
              "side": "south",
              "idx": 0,
            },
          ],
          [
            {
              "side": "north",
              "idx": 0,
            },
          ],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [
        {"left": 1, "right": 1, "newX": 50, "newY": 0},
      ],
      "east": [],
      "north": [
        {"left": 3, "right": 6, "newX": 228, "newY": 509},
      ],
    },
  },
  {
    "north": 12,
    "east": 15,
    "exits": {
      "west": [],
      "south": [
        {"left": 4, "right": 5, "newX": 228, "newY": 0},
      ],
      "east": [
        {"top": 1, "bottom": 9, "newX": 0, "newY": 254},
      ],
      "north": [
        {"left": 5, "right": 5, "newX": 253, "newY": 509},
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
        {
          "top": 2,
          "bottom": 10,
          "newX": 0,
          "newY": 280,
        },
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
