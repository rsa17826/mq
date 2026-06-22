# import map.genGrid as _
import shuffle_exits
import patch_game
import gen_map

playercouldhave, edge_reached, door_reached, warp_reached, all_rooms = shuffle_exits.init()
patch_game.init()
gen_map.main()