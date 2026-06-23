# import map.genGrid as _
import shuffle_exits
import patch_game
import gen_map
import patch_items_advanced
import shuffle_items

playercouldhave, edge_reached, door_reached, warp_reached, all_rooms = shuffle_exits.init()

# shuffle_items.init()
patch_game.init()
# patch_items_advanced.init()


gen_map.main()