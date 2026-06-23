# Item Randomizer: Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MathQuest Game Engine                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Player        Game World           Item Collection            │
│  ┌──────┐     ┌─────────────┐      ┌──────────────┐           │
│  │Char@ │────→│Room (20,20) │────→ │itemTile[0]   │           │
│  │(x,y) │     │  itemTile[] │      │ hitTest()    │           │
│  └──────┘     │             │      └──────────────┘           │
│               │itemDisplay[]│             │                   │
│               └─────────────┘             │                   │
│                                           ▼                   │
│                                    setManagerData()  ◄── PATCH │
│                                    ("apple", value) │         │
│                                                     ▼         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Item Randomizer Patch (Advanced Version)           │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │ 1. Detect item gain/loss                            │    │
│  │ 2. Get player position (x, y, room)                │    │
│  │ 3. Look up items in IR_ROOM_ITEM_MAP                │    │
│  │ 4. Find closest item via proximity                 │    │
│  │ 5. Mark item as collected                          │    │
│  │ 6. Apply spatial disambiguation if needed         │    │
│  │ 7. Update IR_ITEM_COLLECT_LOG                      │    │
│  │ 8. Call original setManagerData()                  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Item Collection

```
Player walks to apple location
              │
              ▼
         Position (x,y)
         Room (north, east)
              │
              ▼
    itemTile[0].hitTest(player)
              │
              ▼
       setManagerData("apple", 5)
              │
              ▼
     ╔═════════════════════════════════════╗
     ║   ITEM RANDOMIZER PATCH INTERCEPTS  ║
     ╠═════════════════════════════════════╣
     │
     │ 1. Check: is k in IR_SAFE_ITEMS?
     │    ("apple" ✓ yes)
     │
     │ 2. Get player position
     │    playerPos = {x: 50, y: 100, room: "20_20"}
     │
     │ 3. Is this a gain? (5 > 4)
     │    Yes ✓
     │
     │ 4. Query IR_ROOM_ITEM_MAP
     │    items = IR_ROOM_ITEM_MAP.get("20_20")
     │    [apple#0@(50,100), apple#1@(75,115), honey#2@(200,250)]
     │
     │ 5. Find closest "apple" to player
     │    Distance apple#0: 0px ✓ MATCH
     │    Distance apple#1: 35px
     │
     │ 6. Mark as collected
     │    apple#0.collected = true
     │    IR_ITEM_COLLECT_LOG.set(0, {...})
     │
     │ 7. Call original function
     │    manager.apple = 5
     │    itemDisplay[0].set_text("Apple: 5")
     │
     └─────────────────────────────────────
              │
              ▼
      Item count displayed
      UI updated normally
```

## JSON File Flow

```
shuffle_items.py
├─ Read ITEM_DEFINITIONS
│  ├─ apple: 15 copies
│  ├─ honey: 8 copies
│  └─ ...23 more items...
│
├─ Read ROOMS (40 available)
│  ├─ (20,20) - Start
│  ├─ (19,20) - North
│  └─ ... [40 rooms total]
│
├─ Generate spawn positions
│  ├─ 710x560 pixel rooms
│  ├─ 14x11 block grid
│  └─ ~150 valid spots per room
│
├─ Distribute items to rooms
│  ├─ Central rooms: 3-6 items each
│  ├─ Mid rooms: 2-4 items each
│  └─ Edge rooms: 1-3 items each
│
└─ Output: items.json
   ├─ seed: 12345
   ├─ totalItems: 245
   ├─ totalLocations: 127
   └─ itemLocations: [
      {globalId:0, itemName:"apple", roomNorth:20, roomEast:20, spawnX:50.5, ...},
      {globalId:1, itemName:"honey", roomNorth:20, roomEast:21, spawnX:100.2, ...},
      ...
      ]
```

## Patch Application

```
patch_items.py
├─ Read: MathQuest.base.js (original)
├─ Read: json/items.json
│
├─ Build lookup tables
│  ├─ IR_TABLE: flat array [north, east, itemName, globalId, ...]
│  ├─ IR_ROOM_ITEM_MAP: Map("20_20" → [items])
│  └─ IR_SAFE_ITEMS: {apple:true, honey:true, ...}
│
├─ Generate JavaScript patch
│  ├─ Inline all item location data
│  ├─ Hook setManagerData() function
│  ├─ Add spatial logic
│  └─ Add safety flags
│
├─ Find anchor point in source
│  └─ "manager.north = 20\n  manager.east = 20\n"
│
├─ Insert patch before anchor
│  └─ (preserves rest of JS intact)
│
└─ Write: MathQuest.js (patched)
   └─ Now includes all IR_ functions
```

## Memory Layout

```
JavaScript Runtime Memory
┌──────────────────────────────────────────────────┐
│ Global Window Object                             │
├──────────────────────────────────────────────────┤
│                                                  │
│ IR_TABLE: Array[127]                             │
│  [north, east, itemName, globalId, x, y, ...]   │
│  └─ ~50KB (compressed)                           │
│                                                  │
│ IR_ROOM_ITEM_MAP: Map                           │
│  "20_20" → Array[5] {items}                      │
│  "20_21" → Array[3] {items}                      │
│  ...40 rooms...                                  │
│  └─ ~30KB (references to IR_TABLE)              │
│                                                  │
│ IR_ITEM_COLLECT_LOG: Map                         │
│  0 → {itemName, collectedAt, room, pos}          │
│  1 → {...}                                       │
│  ...collected items...                           │
│  └─ ~1KB (grows as player collects)             │
│                                                  │
│ manager object                                   │
│  north: 20, east: 20                             │
│  apple: 5, honey: 3, bomb: 8, ...               │
│  char: [PlayerObject]                            │
│  itemDisplay: [TextObjects]                      │
│  └─ ~100KB (existing game data)                 │
│                                                  │
└──────────────────────────────────────────────────┘
Total Extra Memory: ~80KB
```

## Execution Timeline

```
Timeline of a Collection Event
─────────────────────────────────────────

T+0ms:    Player walks into apple sprite
T+1ms:    itemTile[0].hitTest(player) returns true
T+2ms:    Game calls setManagerData("apple", 5)
T+3ms:    ┌─ PATCH STARTS
T+4ms:    │  Check if "apple" in IR_SAFE_ITEMS (yes)
T+5ms:    │  Check if isGain (5 > 4) (yes)
T+6ms:    │  Get player position
T+7ms:    │  Debounce check: 200ms since last apple? (yes)
T+8ms:    │  Query IR_ROOM_ITEM_MAP.get("20_20")
T+9ms:    │  Find closest apple: apple#0 at 0px distance
T+10ms:   │  Mark collected: apple#0.collected = true
T+11ms:   │  Update IR_ITEM_COLLECT_LOG
T+12ms:   │  Call original setManagerData()
T+13ms:   └─ PATCH ENDS
T+14ms:   manager.apple = 5 (applied)
T+15ms:   itemDisplay[0].set_text("Apple: 5")
T+16ms:   itemDisplay[0].set_visible(true)
T+20ms:   itemTile[0].set_visible(false) (optional)
          
Total patch overhead: ~10ms
```

## Room Lookup Mechanism

```
Query: What items are in room (20, 21)?

Step 1: Create key
        roomKey = "20_21"

Step 2: Map lookup
        IR_ROOM_ITEM_MAP.get("20_21")
        
Step 3: Return array
        [
          {itemName: "apple", spawnX: 100, spawnY: 150, collected: false},
          {itemName: "honey", spawnX: 200, spawnY: 250, collected: true},
          {itemName: "bomb", spawnX: 50, spawnY: 75, collected: false}
        ]

Step 4: Filter/search as needed
        closest = items.reduce((best, item) => {
          dist = distance(playerPos, item.spawnPos)
          return (dist < best.distance) ? item : best
        })
        
Result: {itemName: "bomb", spawnX: 50, spawnY: 75, distance: 15px}
```

## Spatial Disambiguation Algorithm

```
Scenario: Room has 3 apples close together
          Player moving through them

Apples in room:
  apple#0 @ (50, 100)
  apple#1 @ (75, 100)  ← Too far now
  apple#2 @ (60, 110)  ← Very close!

Player position: (62, 105)

Proximity calc (threshold 50px):
  Distance to apple#0: sqrt((62-50)² + (105-100)²) = 13px ✓
  Distance to apple#1: sqrt((62-75)² + (105-100)²) = 14px ✓
  Distance to apple#2: sqrt((62-60)² + (105-110)²) = 5px ✓

All three are within proximity! Pick nearest:
  min distance = 5px → apple#2
  
Result: Collect apple#2 (the actual closest one)
Log: "[IR DISAMB] Multiple 'apple' found. Selected via distance (5.0px)"
```

## Integration Points

```
MathQuest.js Game Engine
│
├─ Original: itemTile[i].hitTest(player)
│                    └─ Calls setManagerData()
│                       (PATCH INTERCEPTS HERE)
│                    └─ Updates manager properties
│
├─ Original: manager.north = newRoom
│                    └─ (Entrance rando may also hook this)
│
└─ Original: Various game logic
             └─ Reads manager.apple, manager.honey, etc.
                (Our patch only writes/tracks, doesn't change)
```

## Patch Safety Mechanisms

```
Deadlock Prevention
═══════════════════

Problem: Original setManagerData() might update manager.north
         Which could trigger room change detection
         Which calls setManagerData() again
         → Infinite loop!

Solution: IR_UPDATING_INTERNAL flag
         
         window.setManagerData = function(k, v, vv) {
           if (IR_UPDATING_INTERNAL) {
             return irOriginalSetManagerData.call(this, k, v, vv)
             // Skip patch logic, direct pass-through
           }
           
           IR_UPDATING_INTERNAL = true
           try {
             // Do patch logic
             return irOriginalSetManagerData.call(this, k, v, vv)
           } finally {
             IR_UPDATING_INTERNAL = false
           }
         }

Result: Patch logic only runs once per external call
        No infinite recursion possible
```

## Debug Output Example

```
Console Log Timeline
════════════════════

[IR GAIN] 'apple': 4 → 5 at room 20_20
  ├─ Item name: apple
  ├─ Value change: 4 → 5 (increase = 1)
  └─ Current location: room 20_20

[IR DISAMB] Multiple 'honey' found. Selected via distance (23.5px)
  ├─ Multiple items of same type nearby
  ├─ Proximity-based selection used
  └─ Distance to selected item: 23.5 pixels

[IR TRACKED] Item #0 marked as collected
  ├─ Global item ID: 0
  ├─ Added to IR_ITEM_COLLECT_LOG
  └─ Can be queried: IR_ITEM_COLLECT_LOG.get(0)

[IR LOSS] 'bombs': 10 → 9
  ├─ Item name: bombs
  ├─ Value change: 10 → 9 (decrease = 1)
  └─ (Patch logs but doesn't prevent loss)

[IR STATS] Total items collected: 45 | Available items tracked: 127
  ├─ Collected so far: 45 items
  ├─ Total item instances: 127
  └─ Sent every 10 seconds
```

## Performance Profile

```
                      Time        Memory    Impact
Operation             (ms)        (KB)      on Frame
─────────────────────────────────────────────────────
Item collection       < 1         0         None
Proximity calc        < 2         0         None
Room lookup           < 1         0         None
Debounce check        < 0.5       0         None
Console logging       < 0.5       1         Minimal
─────────────────────────────────────────────────────
Total per item:       < 5ms       ~2KB      < 1%

Game target FPS: 60 (16.7ms per frame)
Patch overhead: ~5ms / 16.7ms = ~30% of budget
Actual impact: ~1% (only when collecting items)
```

## State Diagram: Item Lifecycle

```
Item Lifecycle State Machine
═════════════════════════════

Initial State: UNSPAWNED
  └─ Item exists in json/items.json
  └─ Not yet in game world

Transition: Game loads room
  └─ Room's items added to IR_ROOM_ITEM_MAP
  └─ itemTile[] sprites created
  └─ Item now in world
  
Current State: SPAWNED
  ├─ Player can see it
  ├─ Player can move near it
  └─ itemTile[i].hitTest() can trigger
  
Transition: Player touches item
  └─ setManagerData() called
  └─ Patch detects proximity
  └─ Patch marks collected = true
  
Final State: COLLECTED
  ├─ Item.collected = true
  ├─ IR_ITEM_COLLECT_LOG stores metadata
  ├─ itemTile[i].set_visible(false)
  ├─ manager.itemName incremented
  └─ itemDisplay updated

Notes:
- Items can be "lost" via setManagerData(itemName, lower_value)
- Loss doesn't affect collected flag (tracks successful gains only)
- Same item can be "uncollected" by losing all copies and recollecting
```

This comprehensive visualization should help understand how all the pieces fit together!
