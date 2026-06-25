from __future__ import annotations
from typing import Literal, NotRequired, TypedDict


class ExitBase(TypedDict):
  north: int | float
  east: int | float
  exits: ExitNode
  areas: NotRequired[list[AreaNode]]
  err: NotRequired[bool]


class ExitNode(TypedDict):
  west: list[DirNodeLR]
  east: list[DirNodeLR]
  north: list[DirNodeUD]
  south: list[DirNodeUD]


class DirNodeLR(TypedDict):
  top: int
  bottom: int
  newX: NotRequired[int]


class DirNodeUD(TypedDict):
  left: int
  right: int
  newY: NotRequired[int]


class AreaNode(TypedDict):
  reqs: list[list[str]]
  areas: list[list[AreaAreaNode]]


class AreaAreaNode(TypedDict):
  side: Literal["east", "west", "south", "north"]
  idx: int


GEOM: list[ExitBase] = [
  {
    "north": 3,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 19,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 20,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 23,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 9, "bottom": 9}],
      "north": [{"left": 6, "right": 8}],
    },
  },
  {
    "north": 3,
    "east": 24,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "east", "idx": 1}, {"side": "west", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 0}],
          [{"side": "east", "idx": 1}],
          [{"side": "east", "idx": 0}],
          [{"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 9, "bottom": 9}],
      "south": [],
      "east": [{"top": 5, "bottom": 6}, {"top": 9, "bottom": 9}],
      "north": [{"left": 6, "right": 7, "newY": 89}],
    },
  },
  {
    "north": 3,
    "east": 25,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "west", "idx": 1}, {"side": "east", "idx": 0}],
          [{"side": "west", "idx": 0}, {"side": "north", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 1}, {"side": "east", "idx": 0}],
          [{"side": "west", "idx": 0}],
          [{"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 5, "bottom": 6}, {"top": 9, "bottom": 9}],
      "south": [],
      "east": [{"top": 9, "bottom": 9}],
      "north": [{"left": 11, "right": 12}],
    },
  },
  {
    "north": 3,
    "east": 26,
    "exits": {
      "west": [{"top": 9, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [
        {"left": 12, "right": 12},
        {"left": 10, "right": 10},
        {"left": 8, "right": 8},
        {"left": 6, "right": 6},
        {"left": 4, "right": 4},
      ],
    },
  },
  {
    "north": 4,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 14,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 15,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 17,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 19,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 23,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}],
          [{"side": "east", "idx": 0}, {"side": "north", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 8}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [{"left": 6, "right": 8}],
    },
  },
  {
    "north": 4,
    "east": 24,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "east", "idx": 0}],
          [{"side": "west", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}],
          [{"side": "south", "idx": 0}],
          [{"side": "north", "idx": 0}],
          [{"side": "west", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 7, "right": 7}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [{"left": 11, "right": 11, "newY": 88}],
    },
  },
  {
    "north": 4,
    "east": 25,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 11, "right": 12}],
      "east": [{"top": 9, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 4,
    "east": 26,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "south", "idx": 3},
            {"side": "south", "idx": 1},
            {"side": "south", "idx": 2},
          ],
          [{"side": "south", "idx": 4}],
          [{"side": "west", "idx": 0}, {"side": "south", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}],
          [{"side": "south", "idx": 1}],
          [{"side": "south", "idx": 4}],
          [{"side": "south", "idx": 2}, {"side": "south", "idx": 3}],
          [{"side": "west", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 9, "bottom": 9}],
      "south": [
        {"left": 12, "right": 12},
        {"left": 10, "right": 10},
        {"left": 6, "right": 6},
        {"left": 4, "right": 4},
        {"left": 8, "right": 8},
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
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "east", "idx": 2}, {"side": "east", "idx": 1}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 7, "bottom": 8},
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
      ],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 5,
    "east": 10,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "west", "idx": 0}, {"side": "east", "idx": 0}],
          [{"side": "east", "idx": 1}, {"side": "west", "idx": 1}],
          [{"side": "west", "idx": 2}, {"side": "east", "idx": 2}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 2}, {"side": "east", "idx": 2}],
          [{"side": "east", "idx": 1}, {"side": "west", "idx": 1}],
          [{"side": "west", "idx": 0}],
          [{"side": "east", "idx": 0}],
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
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "west", "idx": 2}, {"side": "west", "idx": 0}],
          [{"side": "west", "idx": 1}, {"side": "north", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 1}],
          [{"side": "west", "idx": 2}, {"side": "west", "idx": 0}],
          [{"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [
        {"top": 7, "bottom": 8},
        {"top": 1, "bottom": 2},
        {"top": 4, "bottom": 5},
      ],
      "south": [],
      "east": [],
      "north": [{"left": 10, "right": 11}],
    },
  },
  {
    "north": 5,
    "east": 15,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 20,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 8}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 24,
    "exits": {
      "west": [],
      "south": [{"left": 11, "right": 11}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 6,
    "east": 10,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
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
      "south": [{"left": 10, "right": 11}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 12,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 6,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 18,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 19,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 21,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 6,
    "east": 23,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 8, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 24,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 0, "right": 8}],
    },
  },
  {
    "north": 7,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
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
      "east": [{"top": 5, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 11,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 12,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 15,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 7,
    "east": 18,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 7,
    "east": 20,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 7,
    "east": 21,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [{"top": 1, "bottom": 9}],
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
        "reqs": [["permit:shadowsoul entrance"]],
      }
    ],
    "exits": {
      "west": [{"top": 1, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 3, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 23,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [{"left": 8, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 24,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 8}],
      "east": [{"top": 4, "bottom": 5}],
      "north": [{"left": 0, "right": 8}],
    },
  },
  {
    "north": 7,
    "east": 25,
    "exits": {
      "west": [{"top": 4, "bottom": 5}],
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
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 8,
    "east": 10,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "east", "idx": 2},
            {"side": "east", "idx": 1},
            {"side": "north", "idx": 1},
          ],
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [
        {"top": 7, "bottom": 9},
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 5},
      ],
      "north": [{"left": 0, "right": 9}, {"left": 11, "right": 13}],
    },
  },
  {
    "north": 8,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [{"side": "west", "idx": 2}, {"side": "north", "idx": 2}],
          [{"side": "north", "idx": 1}, {"side": "west", "idx": 1}],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 7, "bottom": 9},
        {"top": 0, "bottom": 3},
        {"top": 5, "bottom": 5},
      ],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [
        {"left": 7, "right": 13},
        {"left": 0, "right": 2},
        {"left": 4, "right": 5},
      ],
    },
  },
  {
    "north": 8,
    "east": 12,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 3, "bottom": 5}],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 8,
    "east": 13,
    "exits": {
      "west": [{"top": 3, "bottom": 5}],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 14,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 4, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 15,
    "exits": {
      "west": [{"top": 4, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [{"left": 1, "right": 4}],
    },
  },
  {
    "north": 8,
    "east": 16,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 17,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "north", "idx": 1}],
          [{"side": "north", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 8, "bottom": 9}],
      "north": [{"left": 11, "right": 12}, {"left": 1, "right": 2}],
    },
  },
  {
    "north": 8,
    "east": 18,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
          ],
          [{"side": "north", "idx": 1}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}],
          [{"side": "north", "idx": 1}],
          [{"side": "east", "idx": 0}, {"side": "west", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [],
      "east": [{"top": 8, "bottom": 9}],
      "north": [{"left": 10, "right": 12}, {"left": 6, "right": 7}],
    },
  },
  {
    "north": 8,
    "east": 19,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 12, "right": 12}],
    },
  },
  {
    "north": 8,
    "east": 20,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 8, "right": 8, "newY": 144}],
    },
  },
  {
    "north": 8,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 6, "bottom": 7}],
      "north": [],
    },
  },
  {
    "north": 8,
    "east": 22,
    "exits": {
      "west": [{"top": 6, "bottom": 7}],
      "south": [{"left": 3, "right": 13}],
      "east": [{"top": 3, "bottom": 10}],
      "north": [{"left": 7, "right": 9}],
    },
  },
  {
    "north": 8,
    "east": 23,
    "exits": {
      "west": [{"top": 3, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 8,
    "east": 25,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 9,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 9,
    "east": 10,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 11, "right": 13}, {"left": 0, "right": 9}],
      "east": [{"top": 7, "bottom": 10}],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 9,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ],
          [{"side": "north", "idx": 1}],
          [{"side": "south", "idx": 1}],
          [
            {"side": "north", "idx": 2},
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 2},
          ],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 7, "bottom": 10}],
      "south": [
        {"left": 0, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
      "east": [{"top": 0, "bottom": 10}],
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
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 9,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 4}],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 9,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 9,
    "east": 18,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 0}],
          [{"side": "west", "idx": 1}, {"side": "south", "idx": 1}],
          [{"side": "north", "idx": 0}, {"side": "south", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 4}, {"top": 6, "bottom": 6}],
      "south": [{"left": 10, "right": 12}, {"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 10, "right": 12}],
    },
  },
  {
    "north": 9,
    "east": 19,
    "exits": {
      "west": [],
      "south": [{"left": 12, "right": 12}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 9,
    "east": 20,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 9}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 9,
    "east": 21,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 9,
    "east": 22,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}],
          [{"side": "north", "idx": 1}],
          [{"side": "south", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 7, "right": 9}],
      "east": [],
      "north": [{"left": 7, "right": 9}, {"left": 1, "right": 5}],
    },
  },
  {
    "north": 9,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 2, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 24,
    "exits": {
      "west": [{"top": 2, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 2, "bottom": 10}],
      "north": [{"left": 1, "right": 12}],
    },
  },
  {
    "north": 9,
    "east": 25,
    "areas": [
      {
        "reqs": [["quest:2p.?"]],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "west", "idx": 0}],
          [{"side": "east", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 2, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [{"top": 4, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 9,
    "east": 26,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 7, "newY": 148}],
    },
  },
  {
    "north": 10,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 7, "bottom": 10}, {"top": 0, "bottom": 5}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 10,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 2},
            {"side": "north", "idx": 2},
            {"side": "north", "idx": 1},
            {"side": "south", "idx": 1},
          ],
          [{"side": "north", "idx": 0}, {"side": "south", "idx": 0}],
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
      "east": [{"top": 0, "bottom": 10}],
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
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 10,
    "east": 13,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 10,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 10,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 4, "bottom": 10}],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 10,
    "east": 16,
    "exits": {
      "west": [{"top": 3, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 17,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 10,
    "east": 18,
    "exits": {
      "west": [],
      "south": [{"left": 10, "right": 12}],
      "east": [],
      "north": [{"left": 10, "right": 12}],
    },
  },
  {
    "north": 10,
    "east": 19,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 20,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
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
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}],
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
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 8, "bottom": 9}],
      "north": [{"left": 11, "right": 12}, {"left": 3, "right": 4}],
    },
  },
  {
    "north": 10,
    "east": 22,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "south", "idx": 1}, {"side": "south", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "south", "idx": 1}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 7, "right": 9}, {"left": 1, "right": 5}],
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
      "north": [{"left": 7, "right": 11}],
    },
  },
  {
    "north": 10,
    "east": 24,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 12}],
      "east": [],
      "north": [{"left": 3, "right": 4}],
    },
  },
  {
    "north": 10,
    "east": 25,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 1, "right": 2}],
    },
  },
  {
    "north": 10,
    "east": 26,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 10,
    "east": 21,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
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
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}, {"side": "east", "idx": 1}],
          [{"side": "east", "idx": 0}, {"side": "south", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 5, "bottom": 10}, {"top": 0, "bottom": 3}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 11,
    "east": 10,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
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
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 1}, {"side": "south", "idx": 0}],
          [
            {"side": "west", "idx": 0},
            {"side": "north", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 0, "bottom": 3}, {"top": 5, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [{"top": 0, "bottom": 3}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 11,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}, {"side": "west", "idx": 0}],
          [{"side": "north", "idx": 1}, {"side": "south", "idx": 0}],
          [{"side": "south", "idx": 1}],
          [
            {"side": "south", "idx": 2},
            {"side": "east", "idx": 0},
            {"side": "north", "idx": 2},
          ],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 0, "bottom": 3}],
      "south": [
        {"left": 1, "right": 2},
        {"left": 4, "right": 5},
        {"left": 7, "right": 13},
      ],
      "east": [{"top": 0, "bottom": 10}],
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
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [{"top": 9, "bottom": 9}],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 11,
    "east": 13,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 1, "right": 1}],
    },
  },
  {
    "north": 11,
    "east": 14,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "south", "idx": 0}, {"side": "north", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 8, "right": 9}],
    },
  },
  {
    "north": 11,
    "east": 15,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "south", "idx": 0}, {"side": "north", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 5}],
      "east": [],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 11,
    "east": 16,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 17,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
            {"side": "west", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "west", "idx": 0}],
          [{"side": "east", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 4, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 18,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "west", "idx": 0}], [{"side": "south", "idx": 0}]],
      }
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 10, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 19,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "east", "idx": 1}, {"side": "east", "idx": 2}],
          [{"side": "east", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}],
          [{"side": "east", "idx": 1}],
          [{"side": "east", "idx": 2}],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [
        {"top": 8, "bottom": 9},
        {"top": 5, "bottom": 6},
        {"top": 2, "bottom": 3},
      ],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 20,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 2}, {"side": "south", "idx": 0}],
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
      "south": [{"left": 3, "right": 4}, {"left": 11, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 21,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 11,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 4, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 23,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 7, "right": 11}],
      "east": [],
      "north": [{"left": 1, "right": 4}],
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
        "reqs": [["permit:shadowsoul entrance"]],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}, {"side": "east", "idx": 0}],
          [{"side": "south", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 3, "right": 4}],
      "east": [{"top": 6, "bottom": 7}],
      "north": [{"left": 3, "right": 4}],
    },
  },
  {
    "north": 11,
    "east": 25,
    "exits": {
      "west": [{"top": 6, "bottom": 7}],
      "south": [{"left": 1, "right": 2}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 11,
    "east": 26,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 12,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 2}, {"side": "east", "idx": 1}],
          [{"side": "east", "idx": 0}, {"side": "south", "idx": 1}],
          [{"side": "south", "idx": 0}, {"side": "west", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [
        {"left": 0, "right": 5},
        {"left": 7, "right": 8},
        {"left": 10, "right": 13},
      ],
      "east": [{"top": 1, "bottom": 4}, {"top": 6, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 12,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 0}],
          [{"side": "west", "idx": 1}, {"side": "south", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 1, "bottom": 4}, {"top": 6, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 14,
    "exits": {
      "west": [],
      "south": [{"left": 8, "right": 9}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 16,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "east", "idx": 1}, {"side": "west", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 1, "bottom": 9}],
      "south": [],
      "east": [{"top": 1, "bottom": 1}, {"top": 5, "bottom": 9}],
      "north": [{"left": 11, "right": 11}],
    },
  },
  {
    "north": 12,
    "east": 17,
    "exits": {
      "west": [{"top": 5, "bottom": 9}, {"top": 1, "bottom": 1}],
      "south": [],
      "east": [{"top": 8, "bottom": 8}],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 18,
    "exits": {
      "west": [{"top": 8, "bottom": 8}],
      "south": [],
      "east": [{"top": 8, "bottom": 8}],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 12,
    "east": 19,
    "exits": {
      "west": [{"top": 8, "bottom": 8}],
      "south": [],
      "east": [{"top": 8, "bottom": 8}],
      "north": [],
    },
  },
  {
    "north": 12,
    "east": 20,
    "exits": {
      "west": [{"top": 8, "bottom": 8}],
      "south": [],
      "east": [{"top": 2, "bottom": 3}],
      "north": [{"left": 10, "right": 10, "newY": 129}],
    },
  },
  {
    "north": 12,
    "east": 21,
    "exits": {
      "west": [{"top": 2, "bottom": 3}],
      "south": [],
      "east": [],
      "north": [{"left": 11, "right": 11, "newY": 107}],
    },
  },
  {
    "north": 12,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 5, "right": 6}],
    },
  },
  {
    "north": 12,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 4}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [{"left": 10, "right": 11}],
    },
  },
  {
    "north": 12,
    "east": 24,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 3, "right": 4}],
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
      "east": [{"top": 2, "bottom": 3}],
      "north": [{"left": 5, "right": 8}],
    },
  },
  {
    "north": 12,
    "east": 26,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "west", "idx": 0}]],
      },
      {
        "reqs": [["misc:stomp code"]],
        "areas": [[{"side": "south", "idx": 0}, {"side": "west", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [{"top": 2, "bottom": 3}],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 3, "right": 6}],
      "east": [{"top": 5, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 14,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "north", "idx": 0}, {"side": "west", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "north", "idx": 0}], [{"side": "west", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [],
      "east": [],
      "north": [{"left": 9, "right": 10}],
    },
  },
  {
    "north": 13,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 5}],
      "east": [{"top": 2, "bottom": 2}],
      "north": [{"left": 2, "right": 2}],
    },
  },
  {
    "north": 13,
    "east": 16,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "west", "idx": 0}], [{"side": "south", "idx": 0}]],
      }
    ],
    "exits": {
      "west": [{"top": 2, "bottom": 2}],
      "south": [{"left": 11, "right": 11}],
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
      "east": [{"top": 6, "bottom": 7}],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 13,
    "east": 18,
    "exits": {
      "west": [{"top": 6, "bottom": 7}],
      "south": [{"left": 5, "right": 7}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 13,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 5, "bottom": 6}],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 13,
    "east": 20,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 4, "right": 5}],
      "east": [],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 13,
    "east": 21,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "north", "idx": 0}, {"side": "south", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 11, "right": 11}],
      "east": [],
      "north": [{"left": 10, "right": 10}],
    },
  },
  {
    "north": 13,
    "east": 22,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 13,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 10, "right": 11}],
      "east": [],
      "north": [{"left": 10, "right": 11}],
    },
  },
  {
    "north": 13,
    "east": 24,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 1, "right": 9}],
    },
  },
  {
    "north": 13,
    "east": 25,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 5, "right": 8}],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 5, "right": 8}],
    },
  },
  {
    "north": 13,
    "east": 26,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 14,
    "exits": {
      "west": [{"top": 2, "bottom": 9}],
      "south": [{"left": 9, "right": 10}],
      "east": [{"top": 2, "bottom": 2}],
      "north": [{"left": 5, "right": 5}],
    },
  },
  {
    "north": 14,
    "east": 15,
    "exits": {
      "west": [{"top": 2, "bottom": 2}],
      "south": [{"left": 2, "right": 2}],
      "east": [{"top": 7, "bottom": 7}],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 16,
    "exits": {
      "west": [{"top": 7, "bottom": 7}],
      "south": [],
      "east": [],
      "north": [{"left": 5, "right": 5}],
    },
  },
  {
    "north": 14,
    "east": 17,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 7}],
      "east": [],
      "north": [{"left": 4, "right": 9}],
    },
  },
  {
    "north": 14,
    "east": 18,
    "areas": [
      {
        "areas": [[{"side": "north", "idx": 0}, {"side": "south", "idx": 0}]],
        "reqs": [["quest:kingWasStolen"]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 8, "right": 8}],
    },
  },
  {
    "north": 14,
    "east": 19,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "north", "idx": 0}], [{"side": "south", "idx": 0}]],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 5}],
      "east": [],
      "north": [{"left": 10, "right": 10}],
    },
  },
  {
    "north": 14,
    "east": 20,
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 5}],
      "east": [],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 14,
    "east": 21,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "south", "idx": 0}, {"side": "north", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 10, "right": 10}],
      "east": [],
      "north": [{"left": 12, "right": 12}],
    },
  },
  {
    "north": 14,
    "east": 22,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 7, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 23,
    "exits": {
      "west": [{"top": 7, "bottom": 9}],
      "south": [{"left": 10, "right": 11}],
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
      "south": [{"left": 1, "right": 9}],
      "east": [
        {"top": 9, "bottom": 9},
        {"top": 7, "bottom": 7},
        {"top": 5, "bottom": 5},
        {"top": 3, "bottom": 3},
        {"top": 1, "bottom": 1},
      ],
      "north": [],
    },
  },
  {
    "north": 14,
    "east": 25,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 0}],
          [
            {"side": "west", "idx": 1},
            {"side": "west", "idx": 2},
            {"side": "west", "idx": 3},
            {"side": "south", "idx": 0},
          ],
          [{"side": "west", "idx": 4}],
        ],
      }
    ],
    "exits": {
      "west": [
        {"top": 9, "bottom": 9},
        {"top": 7, "bottom": 7},
        {"top": 5, "bottom": 5},
        {"top": 3, "bottom": 3},
        {"top": 1, "bottom": 1},
      ],
      "south": [{"left": 5, "right": 8}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 14,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "east", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}],
          [{"side": "south", "idx": 0}, {"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 5}],
      "east": [{"top": 3, "bottom": 6}],
      "north": [{"left": 2, "right": 2}],
    },
  },
  {
    "north": 15,
    "east": 15,
    "exits": {
      "west": [{"top": 3, "bottom": 6}],
      "south": [],
      "east": [{"top": 4, "bottom": 4}],
      "north": [{"left": 4, "right": 4}],
    },
  },
  {
    "north": 15,
    "east": 16,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 0},
            {"side": "north", "idx": 0},
          ]
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "west", "idx": 0}],
          [{"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 4}],
      "south": [{"left": 5, "right": 5}],
      "east": [],
      "north": [{"left": 12, "right": 12}],
    },
  },
  {
    "north": 15,
    "east": 17,
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 9}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 18,
    "exits": {
      "west": [],
      "south": [{"left": 8, "right": 8}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 15,
    "east": 19,
    "exits": {
      "west": [],
      "south": [{"left": 10, "right": 10}],
      "east": [],
      "north": [{"left": 2, "right": 2}],
    },
  },
  {
    "north": 15,
    "east": 20,
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 5}],
      "east": [{"top": 8, "bottom": 9}],
      "north": [{"left": 4, "right": 5}],
    },
  },
  {
    "north": 15,
    "east": 21,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "west", "idx": 0}], [{"side": "south", "idx": 0}]],
      }
    ],
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [{"left": 12, "right": 12}],
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
      "east": [{"top": 4, "bottom": 5}],
      "north": [{"left": 2, "right": 2, "newY": 129}],
    },
  },
  {
    "north": 15,
    "east": 23,
    "exits": {
      "west": [{"top": 4, "bottom": 5}],
      "south": [
        {"left": 10, "right": 10},
        {"left": 6, "right": 7},
        {"left": 4, "right": 4},
      ],
      "east": [{"top": 1, "bottom": 2}],
      "north": [{"left": 1, "right": 1}],
    },
  },
  {
    "north": 15,
    "east": 24,
    "exits": {
      "west": [{"top": 1, "bottom": 2}],
      "south": [],
      "east": [],
      "north": [{"left": 9, "right": 12}, {"left": 1, "right": 1}],
    },
  },
  {
    "north": 15,
    "east": 25,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 8, "right": 9}, {"left": 5, "right": 6}],
    },
  },
  {
    "north": 16,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 6, "bottom": 8}],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 11,
    "exits": {
      "west": [{"top": 6, "bottom": 8}],
      "south": [],
      "east": [],
      "north": [{"left": 3, "right": 4}],
    },
  },
  {
    "north": 16,
    "east": 14,
    "exits": {
      "west": [],
      "south": [{"left": 2, "right": 2}],
      "east": [],
      "north": [{"left": 3, "right": 4, "newY": 125}],
    },
  },
  {
    "north": 16,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 4}],
      "east": [],
      "north": [{"left": 7, "right": 8}],
    },
  },
  {
    "north": 16,
    "east": 16,
    "exits": {
      "west": [],
      "south": [{"left": 12, "right": 12}],
      "east": [{"top": 5, "bottom": 7}],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 17,
    "exits": {
      "west": [{"top": 5, "bottom": 7}],
      "south": [],
      "east": [],
      "north": [{"left": 10, "right": 10}],
    },
  },
  {
    "north": 16,
    "east": 18,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 1, "bottom": 1}],
      "north": [{"left": 1, "right": 1}],
    },
  },
  {
    "north": 16,
    "east": 19,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "south", "idx": 0}],
          [{"side": "west", "idx": 0}],
        ],
      },
      {
        "reqs": [["permit:bomb.2"]],
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
      "west": [{"top": 1, "bottom": 1}],
      "south": [{"left": 2, "right": 2}],
      "east": [{"top": 8, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 20,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [{"left": 4, "right": 5}],
      "east": [{"top": 8, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 21,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [],
      "east": [{"top": 2, "bottom": 3}],
      "north": [],
    },
  },
  {
    "north": 16,
    "east": 22,
    "exits": {
      "west": [{"top": 2, "bottom": 3}],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 10, "right": 11}],
    },
  },
  {
    "north": 16,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 1}],
      "east": [],
      "north": [{"left": 1, "right": 1}],
    },
  },
  {
    "north": 16,
    "east": 24,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 0}, {"side": "south", "idx": 1}],
          [{"side": "north", "idx": 0}, {"side": "south", "idx": 0}],
          [{"side": "north", "idx": 1}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 1}, {"left": 9, "right": 12}],
      "east": [{"top": 3, "bottom": 6}],
      "north": [{"left": 5, "right": 6}, {"left": 1, "right": 3}],
    },
  },
  {
    "north": 16,
    "east": 25,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "south", "idx": 1}, {"side": "west", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 3, "bottom": 6}],
      "south": [{"left": 8, "right": 9}, {"left": 5, "right": 6}],
      "east": [],
      "north": [{"left": 8, "right": 9}],
    },
  },
  {
    "north": 17,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 4, "bottom": 4}],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 11,
    "exits": {
      "west": [{"top": 4, "bottom": 4}],
      "south": [{"left": 3, "right": 4}],
      "east": [],
      # "east": [{"top": 4, "bottom": 4}],
      "north": [{"left": 3, "right": 4}],
    },
    "err": True,
  },
  {
    "north": 17,
    "east": 14,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 7, "right": 8}],
      "east": [],
      "north": [{"left": 3, "right": 7}, {"left": 9, "right": 11}],
    },
  },
  {
    "north": 17,
    "east": 16,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 1, "bottom": 2}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 17,
    "east": 17,
    "exits": {
      "west": [{"top": 1, "bottom": 2}],
      "south": [{"left": 10, "right": 10}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 18,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 1}],
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
      "east": [{"top": 3, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 20,
    "exits": {
      "west": [{"top": 3, "bottom": 6}],
      "south": [],
      "east": [],
      "north": [{"left": 5, "right": 6}],
    },
  },
  {
    "north": 17,
    "east": 21,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 5, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 22,
    "exits": {
      "west": [{"top": 5, "bottom": 6}],
      "south": [{"left": 10, "right": 11}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 17,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 1}],
      "east": [],
      "north": [{"left": 9, "right": 10}],
    },
  },
  {
    "north": 17,
    "east": 24,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 6}, {"left": 1, "right": 3}],
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
        "reqs": [[]],
        "areas": [
          [{"side": "west", "idx": 2}],
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
      "south": [{"left": 8, "right": 9}],
      "east": [],
      "north": [{"left": 11, "right": 12}],
    },
  },
  {
    "north": 18,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 8, "bottom": 8}],
      "north": [{"left": 1, "right": 2}],
    },
  },
  {
    "north": 18,
    "east": 11,
    "exits": {
      "west": [{"top": 8, "bottom": 8}],
      "south": [{"left": 3, "right": 4}],
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
      "north": [{"left": 8, "right": 8}],
    },
  },
  {
    "north": 18,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 18,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 18,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 3, "right": 7}, {"left": 9, "right": 11}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 16,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 17,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}],
          [
            {"side": "north", "idx": 1},
            {"side": "south", "idx": 0},
            {"side": "east", "idx": 0},
          ],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 4, "bottom": 4}],
      "north": [{"left": 7, "right": 8}, {"left": 4, "right": 5}],
    },
  },
  {
    "north": 18,
    "east": 18,
    "exits": {
      "west": [{"top": 4, "bottom": 4}],
      "south": [],
      "east": [],
      "north": [{"left": 1, "right": 1}, {"left": 11, "right": 11}],
    },
  },
  {
    "north": 18,
    "east": 19,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 8, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 20,
    "exits": {
      "west": [{"top": 8, "bottom": 9}],
      "south": [{"left": 5, "right": 6}],
      "east": [{"top": 9, "bottom": 9}],
      "north": [{"left": 1, "right": 12}],
    },
  },
  {
    "north": 18,
    "east": 21,
    "exits": {
      "west": [{"top": 9, "bottom": 9}],
      "south": [],
      "east": [{"top": 4, "bottom": 4}],
      "north": [{"left": 3, "right": 3}, {"left": 8, "right": 8}],
    },
  },
  {
    "north": 18,
    "east": 22,
    "areas": [
      {
        "areas": [[{"side": "west", "idx": 0}, {"side": "east", "idx": 0}]],
        "reqs": [["quest:gTree.2"]],
      },
      {
        "areas": [[{"side": "west", "idx": 0}], [{"side": "east", "idx": 0}]],
        "reqs": [[]],
      },
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 4}],
      "south": [],
      "east": [{"top": 1, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 18,
    "east": 23,
    "exits": {
      "west": [{"top": 1, "bottom": 9}],
      "south": [{"left": 9, "right": 10}],
      "east": [{"top": 7, "bottom": 8}],
      "north": [{"left": 5, "right": 6}],
    },
  },
  {
    "north": 18,
    "east": 24,
    "exits": {
      "west": [{"top": 7, "bottom": 8}],
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
      "south": [{"left": 11, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 10,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 2}],
      "east": [{"top": 2, "bottom": 3}],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 11,
    "exits": {
      "west": [{"top": 2, "bottom": 3}],
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
      "south": [{"left": 8, "right": 8}],
      "east": [{"top": 3, "bottom": 7}],
      "north": [{"left": 3, "right": 9}],
    },
  },
  {
    "north": 19,
    "east": 13,
    "exits": {
      "west": [{"top": 3, "bottom": 7}],
      "south": [{"left": 6, "right": 6}],
      "east": [{"top": 5, "bottom": 5, "newX": 600}],
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
      "north": [{"left": 5, "right": 6}],
    },
  },
  {
    "north": 19,
    "east": 16,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 17,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 1}, {"side": "north", "idx": 0}],
          [{"side": "south", "idx": 0}, {"side": "east", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [],
      "south": [{"left": 7, "right": 8}, {"left": 4, "right": 5}],
      "east": [{"top": 3, "bottom": 3}],
      "north": [{"left": 1, "right": 8}],
    },
  },
  {
    "north": 19,
    "east": 18,
    "areas": [
      {
        "reqs": [["fireNPCPass?"]],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
            {"side": "south", "idx": 1},
          ],
          [{"side": "south", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "south", "idx": 0}],
          [{"side": "south", "idx": 1}, {"side": "west", "idx": 0}],
          [{"side": "north", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 3, "bottom": 3}],
      "south": [{"left": 1, "right": 1}, {"left": 11, "right": 11}],
      "east": [],
      "north": [{"left": 8, "right": 12}],
    },
  },
  {
    "north": 19,
    "east": 20,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 12}],
      "east": [],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 19,
    "east": 21,
    "exits": {
      "west": [],
      "south": [{"left": 3, "right": 3}, {"left": 8, "right": 8}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 22,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 19,
    "east": 23,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 6}],
      "east": [{"top": 4, "bottom": 5}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 19,
    "east": 24,
    "exits": {
      "west": [{"top": 4, "bottom": 5}],
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
      "south": [{"left": 3, "right": 9}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 16,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 20,
    "east": 17,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 8}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 20,
    "east": 18,
    "exits": {
      "west": [],
      "south": [{"left": 8, "right": 12}],
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
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 20,
    "east": 21,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 20,
    "east": 22,
    "areas": [
      {
        "reqs": [["permit:bomb.2"]],
        "areas": [[{"side": "east", "idx": 0}, {"side": "north", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "east", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 2, "bottom": 3}],
      "north": [{"left": 8, "right": 9}],
    },
  },
  {
    "north": 20,
    "east": 23,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [
          [{"side": "south", "idx": 0}, {"side": "north", "idx": 0}],
          [{"side": "west", "idx": 0}],
        ],
      },
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}],
          [{"side": "south", "idx": 0}],
          [{"side": "west", "idx": 0}],
        ],
      },
    ],
    "exits": {
      "west": [{"top": 2, "bottom": 3}],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 10, "right": 11}],
    },
  },
  {
    "north": 21,
    "east": 9,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 21,
    "east": 11,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [
            {"side": "north", "idx": 0},
            {"side": "west", "idx": 0},
            {"side": "east", "idx": 0},
          ]
        ],
      }
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 21,
    "east": 12,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 6, "right": 7}],
      "east": [{"top": 4, "bottom": 6}],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 13,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "east", "idx": 1}],
          [{"side": "east", "idx": 0}, {"side": "west", "idx": 0}],
        ],
      }
    ],
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [],
      "east": [{"top": 7, "bottom": 8}, {"top": 2, "bottom": 5}],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 14,
    "exits": {
      "west": [{"top": 2, "bottom": 5}, {"top": 7, "bottom": 8}],
      "south": [],
      "east": [],
      "north": [{"left": 11, "right": 12}],
    },
  },
  {
    "north": 21,
    "east": 17,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 1, "bottom": 1}],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 18,
    "exits": {
      "west": [{"top": 1, "bottom": 1}],
      "south": [
        {"left": 8, "right": 8},
        {"left": 10, "right": 10},
        {"left": 6, "right": 6},
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
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 9, "bottom": 9}],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 21,
    "areas": [
      {
        "reqs": [[]],
        "areas": [[{"side": "east", "idx": 0}], [{"side": "west", "idx": 0}]],
      }
    ],
    "exits": {
      "west": [{"top": 9, "bottom": 9}],
      "south": [],
      "east": [{"top": 1, "bottom": 2}],
      "north": [],
    },
  },
  {
    "north": 21,
    "east": 23,
    "exits": {
      "west": [{"top": 4, "bottom": 5}],
      "south": [{"left": 10, "right": 11}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 22,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 7}],
      "east": [],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 22,
    "east": 10,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 22,
    "east": 11,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 7}],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 22,
    "east": 12,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 22,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 22,
    "east": 14,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 11, "right": 12}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 23,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 7}],
      "east": [],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 23,
    "east": 10,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 23,
    "east": 11,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 6}],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 23,
    "east": 12,
    "exits": {
      "west": [{"top": 4, "bottom": 6}],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [{"left": 5, "right": 7}],
    },
  },
  {
    "north": 23,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 23,
    "east": 14,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 6, "right": 6}],
    },
  },
  {
    "north": 24,
    "east": 9,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 7}],
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
      "east": [{"top": 1, "bottom": 2}],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 11,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "west", "idx": 0}, {"side": "south", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "west", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [{"top": 1, "bottom": 2}],
      "south": [{"left": 5, "right": 7}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 12,
    "exits": {
      "west": [],
      "south": [{"left": 5, "right": 7}],
      "east": [{"top": 2, "bottom": 4}],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 13,
    "exits": {
      "west": [{"top": 2, "bottom": 4}],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 24,
    "east": 14,
    "exits": {
      "west": [],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 100,
    "east": 100,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 12}],
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
      "north": [{"left": 4, "right": 9}],
    },
  },
  {
    "north": 201,
    "east": 200,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    # Pocket room between the two stairsDown warps near 10_21 / 9_20.
    # Not part of the grid (no GEOM-adjacent edges reference it, see _exits.py),
    # only reachable via door entries in EXITS["doors"]. Fully open inside,
    # so no "areas" key.
    "north": 10.1,
    "east": 21,
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 300,
    "east": 300,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 12}],
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
      "north": [{"left": 8, "right": 10}],
    },
  },
  {
    "north": 500,
    "east": 501,
    "exits": {
      "west": [],
      "south": [],
      "east": [],
      "north": [{"left": 5, "right": 6}],
    },
  },
  {
    "north": 501,
    "east": 500,
    "exits": {
      "west": [],
      "south": [{"left": 8, "right": 10}],
      "east": [{"top": 1, "bottom": 4}],
      "north": [],
    },
  },
  {
    "north": 501,
    "east": 501,
    "exits": {
      "west": [{"top": 1, "bottom": 4}],
      "south": [{"left": 5, "right": 6}],
      "east": [],
      "north": [],
    },
  },
  {
    "north": 5,
    "east": 21,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 4,
    "east": 21,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 3,
    "east": 21,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 4,
    "east": 20,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 19,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 18,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 18,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 17,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 4,
    "east": 16,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 17,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 18,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 17,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 17,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 15,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 14,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 6,
    "east": 14,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 14,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 5,
    "east": 13,
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 15,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 14,
    "exits": {
      "west": [{"top": 0, "bottom": 9}],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 3,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 1, "right": 13}],
    },
  },
  {
    "north": 7,
    "east": 19,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 6,
    "east": 20,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 0, "bottom": 10}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 9,
    "east": 17,
    "exits": {
      "west": [],
      "south": [{"left": 11, "right": 12}, {"left": 1, "right": 2}],
      "east": [{"top": 4, "bottom": 4}, {"top": 6, "bottom": 6}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 8,
    "east": 24,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 8}],
      "east": [{"top": 0, "bottom": 9}],
      "north": [{"left": 0, "right": 13}],
    },
  },
  {
    "north": 21,
    "east": 22,
    "exits": {
      "west": [{"top": 1, "bottom": 2}],
      "south": [{"left": 8, "right": 9}],
      "east": [{"top": 4, "bottom": 5}],
      "north": [],
    },
  },
  {
    "north": 19,
    "east": 14,
    "exits": {
      "west": [{"top": 6, "bottom": 6}],
      "south": [{"left": 6, "right": 6}],
      "east": [],
      "north": [],
    },
    "err": True,
  },
  {
    "north": 9,
    "east": 12,
    "exits": {
      "west": [{"top": 0, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 12,
    "east": 10,
    "exits": {
      "west": [{"top": 1, "bottom": 10}],
      "south": [{"left": 0, "right": 13}],
      "east": [{"top": 1, "bottom": 10}],
      "north": [],
    },
  },
  {
    "north": 10,
    "east": 10,
    "areas": [
      {
        "reqs": [[]],
        "areas": [
          [{"side": "north", "idx": 0}, {"side": "west", "idx": 0}],
          [{"side": "west", "idx": 1}, {"side": "south", "idx": 0}],
        ],
      }
    ],
    "exits": {"west": [], "south": [], "east": [], "north": []},
  },
  {
    "north": 10,
    "east": 10,
    "exits": {
      "west": [{"top": 0, "bottom": 5}, {"top": 7, "bottom": 10}],
      "south": [{"left": 0, "right": 12}],
      "east": [],
      "north": [{"left": 0, "right": 12}],
    },
  },
  {
    "north": 21,
    "east": 10,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 4, "bottom": 6}],
      "north": [{"left": 6, "right": 7}],
    },
  },
  {
    "north": 12,
    "east": 13,
    "areas": [
      {
        "reqs": [["permit:bomb"]],
        "areas": [[{"side": "north", "idx": 0}, {"side": "south", "idx": 0}]],
      },
      {
        "reqs": [[]],
        "areas": [[{"side": "south", "idx": 0}], [{"side": "north", "idx": 0}]],
      },
    ],
    "exits": {
      "west": [],
      "south": [{"left": 1, "right": 1}],
      "east": [],
      "north": [{"left": 3, "right": 6}],
    },
  },
  {
    "north": 12,
    "east": 15,
    "exits": {
      "west": [],
      "south": [{"left": 4, "right": 5}],
      "east": [{"top": 1, "bottom": 9}],
      "north": [{"left": 5, "right": 5}],
    },
  },
  {
    "north": 14,
    "east": 13,
    "exits": {
      "west": [],
      "south": [],
      "east": [{"top": 2, "bottom": 10}],
      "north": [],
    },
  },
]
