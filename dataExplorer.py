import yeeps
from yeeps import client
import sys

print("==========================================================")
print("                  YEEPS CUSTOM STATS                  ")
print("==========================================================")
print("Type 'exit' or 'quit' at the prompt to close the program.\n")

while True:
    try:
        auth_input = input("Enter target account credentials (Username|MobileCode): ").strip()
        if auth_input.lower() in ['exit', 'quit', '']:
            print("Closing tracker session. Goodbye!")
            sys.exit()
        if "|" not in auth_input:
            print("Invalid format! Please type it exactly like: Username|MobileCode\n")
            continue

        api = client.API(auth_input)
        print("Connecting to backend proxy server...")
        login = api.login()
        userData = login.userData
        session = api.login()
        data = session.raw

        if not data or 'stats' not in data:
            print("Backend Error: Account lookup failed. Verify your code values!\n")
            continue

        oculus_username = data.get('oculusID')
        account_id = data.get('accountID')
        player_stats = data.get('stats', {})

        buttcoins = player_stats.get('currency', 0)
        silver_beans = player_stats.get('beans', 0)
        unlocked_items = player_stats.get('ownedPatterns', [])
        fav_list = player_stats.get('ownedPatterns_favorite', {}).get('_', [])
        hidden_items = player_stats.get('ownedPatterns_hidden', [])
        active_cosmetics = player_stats.get('activeCosmetics', [])
        saved_outfits = player_stats.get('savedOutfits', [])
        owned_bundles = player_stats.get('ownedBundles', [])

        times_logged_on = player_stats.get('sessionCount', 0)
        first_login_date = player_stats.get('firstLogin', "Unknown")
        ban_hours_left = player_stats.get('remainingBanHours', 0)
        
        role_timestamps = player_stats.get('roleGivenTimestamps', {})
        
        # Default fallback values for standard community accounts
        assigned_role = "Player"
        role_since_date = "N/A"
        
        # Priority tree matching official server rank naming conventions
        role_priority = [
            "administrator", 
            "admin",
            "moderator", 
            "jr_moderator", 
            "designer", 
            "super_star",       # Maps to Star Creator on display
            "content_creator",   # Content Creator Rank
            "star_program",      # Star Program Tier
            "tester"             # Lab Rat Beta Team
        ]
        
        if role_timestamps:
            for known_role in role_priority:
                if known_role in role_timestamps:
                    # Apply custom text adjustments for official brand changes
                    if known_role in ["administrator", "admin"]:
                        assigned_role = "Trass"
                    elif known_role == "super_star":
                        assigned_role = "Star Creator"
                    else:
                        assigned_role = known_role.replace("_", " ").title()
                        
                    role_since_date = role_timestamps[known_role]
                    break
            
            # Fallback catch-all for any unlisted custom developer badges
            if assigned_role == "Player" and role_timestamps.keys():
                first_custom_role = list(role_timestamps.keys())[0]
                assigned_role = first_custom_role.replace("_", " ").title()
                role_since_date = role_timestamps[first_custom_role]

        has_creator_pack = bool(player_stats.get('hasCreatorPack', 0))
        has_private_rooms = bool(player_stats.get('hasUnlockedPrivateRooms', 0))

        owner_in_cws = player_stats.get('cw_admin', [])
        staff_in_cws = player_stats.get('cw_staff', [])
        vip_in_cws = player_stats.get('cw_vip', [])
        favorite_cws = player_stats.get('cw_favorites', [])

        pets_dict = player_stats.get('pets', {})
        total_pets = len(pets_dict)
        pet_names = []
        total_pet_levels = 0
        for pet_type, pet_info in pets_dict.items():
            pet_names.append(pet_info.get('name', 'Unnamed'))
            total_pet_levels += pet_info.get('level', 1)
        avg_pet_level = round(total_pet_levels / total_pets) if total_pets > 0 else 0
        pet_names_str = ", ".join(pet_names)

        paintbrushes, gadgets, cosmetics, weapons_and_bombs = [], [], [], []
        music_and_audio, mobs_and_npcs, tools_and_props, blocks, leftovers = [], [], [], [], []

        # Shortened matching tuples completely protect against system auto-line-wrapping bugs
        for item in unlocked_items:
            item_lower = item.lower()
            if any(x in item_lower for x in ["paintbrush", "painter", "recolorer", "materialpaintbrush"]):
                paintbrushes.append(item)
            elif any(x in item_lower for x in ["logicgate", "wire", "pulse", "button", "delay", "extender", "receiver", "transmitter", "flipflop", "randomizer", "computer", "screen", "console", "detector", "rotator", "shifter", "copier", "paster", "sign", "alwayspowering", "lightbulb", "geigercounter", "playergate", "barrier", "latch", "daylightsensor", "customlightingselector", "clock", "onstart", "broadcaster", "achievementsconsole", "variable", "supercharger", "spawner_fuse", "costmultiplier", "damagemultiplier", "refundcost", "gravityselector", "gravityzone", "worldtoken", "token", "exchanger", "reward", "trigger_"]):
                gadgets.append(item)
            elif any(x in item_lower for x in ["helmet", "suit", "shirt", "zipper", "hoodie", "glasses", "crop", "sweater", "hazmat", "pirate", "chef", "gorilla", "astronaut", "police", "badge", "innertube", "flipper", "cosmetics", "spartan", "shield", "creatorpack", "mask", "hat", "overalls", "sleeves", "ears", "goggles", "girl10", "spy", "voyager", "thief", "skater", "wings", "krampus", "santa", "gingerbread", "belt", "outlaw", "sheriff", "pumashoe", "scientist", "ringmaster", "anniversary26", "aviator"]):
                cosmetics.append(item)
            elif any(x in item_lower for x in ["bomb", "gun", "cannon", "grenade", "machete", "detonator", "firework", "sparkler", "confetti", "throwing", "spikes", "trap", "crossbow", "frisbee", "snowball", "dagger", "arrow", "missile", "turret", "bazooka", "chainsaw", "landmine", "snowflake", "windup", "freeray", "mace", "airgrabber", "shoelauncher", "shoot", "hammer", "chicken"]):
                weapons_and_bombs.append(item)
            elif any(x in item_lower for x in ["drum", "hihat", "crash", "speaker", "music", "tape", "record", "audio", "horn", "sound", "metronome", "soundboard", "bell"]):
                music_and_audio.append(item)
            elif any(x in item_lower for x in ["pet", "spawn", "npc", "mob", "soldier", "grandma", "yak", "sheep", "wolf", "hippo", "bear", "minioncapsule"]):
                mobs_and_npcs.append(item)
            elif any(x in item_lower for x in ["grapplinghook", "glider", "umbrella", "wristpropellor", "surfboard", "sled", "broom", "witchesbroom", "targetdummy", "radio", "microphone", "flower", "mushroom", "gnome", "pumpkin", "lantern", "icicle", "skull", "rose", "coco", "buttjo", "fan", "teleporter", "pylon", "checkpoint", "race", "boostpad", "omniboostpad", "freezeglove", "hotcoco", "ziplinepylon", "snowman0", "anchor", "steeringwheel", "prop_", "pie", "brush", "ball", "toy", "car", "letter", "saddle", "handhold", "match", "candle", "lootsack", "movingbox", "jackinthebox", "painting", "lostnote", "bowl", "trim", "skateboard", "egg", "hoop", "fieldgoal", "pitcher", "nametag", "globe", "mistletoe", "banner", "sphere", "eye", "balloon", "ring", "portal", "trophie", "vioconsole", "vipbarrier", "puzzlepiece", "board", "binder", "domino", "keyart", "art"]):
                tools_and_props.append(item)
            elif any(x in item_lower for x in ["wooden", "stuffed", "glass", "pipe", "rock", "sand", "ice", "water", "flowingwater", "trampoline", "pad", "door", "bars", "pillar", "arch", "reinforced", "dispenser", "slab", "bush", "coral", "clam", "crab", "starfish", "barrel", "web", "disintegratingblock", "block", "store", "room", "stuffingstorage", "stuffingplant", "techweb", "prisonbars", "resetmapblock", "present", "hohoho", "furnace", "cauldron", "stove", "oven", "funnel", "diverter", "fantasy", "map", "rail", "sandstone", "dune", "passageway", "floor", "rug", "keycard", "keyspawner", "carpet", "brick", "wardrobe", "cloud", "stair", "void", "metal", "shaper", "breakable", "crater"]):
                blocks.append(item)
            else:
                leftovers.append(item)

        print(f"\n==========================================================")
        print(f"Player: {oculus_username:<20} | Total Logins: {times_logged_on}")
        print(f"First Join: {first_login_date:<16} | {assigned_role} Since: {role_since_date}")
        print(f"Wallet: {buttcoins} Butt-Coins | {silver_beans} Silver Beans")
        print(f"==========================================================")
        print(f"Paintbrushes:                {len(paintbrushes):<4}")
        print(f"Wiring Blocks:               {len(gadgets):<4}")
        print(f"Cosmetics:                   {len(cosmetics):<4} (Equipped: {len(active_cosmetics)})")
        print(f"Music:                       {len(music_and_audio):<4}")
        print(f"Mobs, Pets, NPCs:            {len(mobs_and_npcs):<4} (Pets Owned: {total_pets})")
        print(f"Weapons:                     {len(weapons_and_bombs):<4}")
        print(f"Interactive items & blocks:  {len(tools_and_props):<4} (Pinned: {len(fav_list)})")
        print(f"Blocks:                      {len(blocks):<4}")
        print(f"Unclassified:                {len(leftovers):<4}")
        print(f"----------------------------------------------------------")
        print(f"Grand Inventory Total:       {len(unlocked_items):<4} items & blocks")
        print(f"==========================================================")
        print(f"Owned Community Worlds:      {len(owner_in_cws):<4} | Staff In: {len(staff_in_cws)}")
        print(f"Favorited Worlds:            {len(favorite_cws):<4} | VIP In:   {len(vip_in_cws)}")
        print(f"Creator Pack Unlocked:       {str(has_creator_pack):<4} | Private Rooms: {str(has_private_rooms)}")
        print(f"Total Owned Store Bundles:   {len(owned_bundles):<4} | Saved Outfits: {len(saved_outfits)}")
        print(f"----------------------------------------------------------")
        print(f"Pet Registry: {pet_names_str}")
        print(f"Average Companion Level:     {avg_pet_level}")
        print(f"==========================================================\n")

    except KeyboardInterrupt: print("\nSession aborted."); sys.exit()
    except Exception as err: print(f"\nConnection Error: {err}\n")
