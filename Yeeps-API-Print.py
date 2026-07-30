import yeeps
from yeeps import client

api = client.API("YWDS|3905")
login = api.login()
userData = login.userData
session = api.login()

data = session.raw


# --- 1. ROOT ACCOUNT METRICS ---
oculus_username = data.get('oculusID')
account_id = data.get('accountID')
player_stats = data.get('stats', {})

buttcoins = player_stats.get('currency', 0)
silver_beans = player_stats.get('beans', 0)

# Pull core nested fields
unlocked_items = player_stats.get('ownedPatterns', [])
favorited_items_dict = player_stats.get('ownedPatterns_favorite', {})
hidden_items = player_stats.get('ownedPatterns_hidden', [])
active_cosmetics = player_stats.get('activeCosmetics', [])
saved_outfits = player_stats.get('savedOutfits', [])
owned_bundles = player_stats.get('ownedBundles', [])

# Initialize comprehensive target categories for the master loop
paintbrushes = []
gadgets = []
cosmetics = []
weapons_and_bombs = []
music_and_audio = []
mobs_and_npcs = []
tools_and_props = []
blocks = []
leftovers = []

# --- 2. MASTER INVENTORY CATEGORIZATION LOOP ---
for item in unlocked_items:
    item_lower = item.lower()
    
    # Paintbrushes & Shapers
    if any(x in item_lower for x in ["paintbrush", "painter", "recolorer", "materialpaintbrush"]):
        paintbrushes.append(item)
        
    # Logic, Math Variables, Signs, Superchargers, & Tokens
    elif any(x in item_lower for x in [
        "logicgate", "wire", "pulse", "button", "delay", "extender", "receiver", "transmitter", 
        "flipflop", "randomizer", "computer", "screen", "console", "detector", "rotator", "shifter", 
        "copier", "paster", "sign", "alwayspowering", "lightbulb", "geigercounter", "playergate", 
        "barrier", "latch", "daylightsensor", "customlightingselector", "clock", "onstart", 
        "broadcaster", "achievementsconsole", "variable", "supercharger", "spawner_fuse", 
        "costmultiplier", "damagemultiplier", "refundcost", "gravityselector", "gravityzone", 
        "worldtoken", "token", "exchanger", "reward", "trigger_"
    ]):
        gadgets.append(item)
        
    # Cosmetics, Badges, & Uniform Apparel
    elif any(x in item_lower for x in [
        "helmet", "suit", "shirt", "zipper", "hoodie", "glasses", "crop", "sweater", "hazmat", 
        "pirate", "chef", "gorilla", "astronaut", "police", "badge", "innertube", "flipper", 
        "cosmetics", "spartan", "shield", "creatorpack", "mask", "hat", "overalls", "sleeves", 
        "ears", "goggles", "girl10", "spy", "voyager", "thief", "skater", "wings", "krampus", 
        "santa", "gingerbread", "belt", "outlaw", "sheriff", "pumashoe", "scientist", "ringmaster", 
        "anniversary26", "aviator"
    ]):
        cosmetics.append(item)
        
    # Weaponry, Explosives, & Projectile Traps
    elif any(x in item_lower for x in [
        "bomb", "gun", "cannon", "grenade", "machete", "detonator", "firework", "sparkler", 
        "confetti", "throwing", "spikes", "trap", "crossbow", "frisbee", "snowball", "dagger", 
        "arrow", "missile", "turret", "bazooka", "chainsaw", "landmine", "snowflake", "windup", 
        "freeray", "mace", "airgrabber", "shoelauncher", "shoot", "hammer", "chicken"
    ]):
        weapons_and_bombs.append(item)
        
    # Music & Acoustic Modulators
    elif any(x in item_lower for x in ["drum", "hihat", "crash", "speaker", "music", "tape", "record", "audio", "horn", "sound", "metronome", "soundboard", "bell"]):
        music_and_audio.append(item)
        
    # Living Spawners & Pets
    elif any(x in item_lower for x in ["pet", "spawn", "npc", "mob", "soldier", "grandma", "yak", "sheep", "wolf", "hippo", "bear", "minioncapsule"]):
        mobs_and_npcs.append(item)
        
    # Interactive Toys, Props, Maps, & Puzzle Board Items
    elif any(x in item_lower for x in [
        "grapplinghook", "glider", "umbrella", "wristpropellor", "surfboard", "sled", "broom", 
        "targetdummy", "radio", "microphone", "flower", "mushroom", "gnome", "pumpkin", "lantern", 
        "icicle", "skull", "rose", "coco", "buttjo", "fan", "teleporter", "pylon", "checkpoint", 
        "race", "boostpad", "omniboostpad", "freezeGlove", "hotcoco", "ziplinepylon", "snowman0", 
        "anchor", "steeringwheel", "prop_", "pie", "brush", "ball", "toy", "car", "letter", 
        "saddle", "handhold", "match", "candle", "lootsack", "movingbox", "jackinthebox", "painting", 
        "lostnote", "bowl", "trim", "skateboard", "egg", "hoop", "fieldgoal", "pitcher", "nametag", 
        "globe", "mistletoe", "banner", "sphere", "eye", "balloon", "ring", "portal", "trophie", 
        "vioconsole", "vipbarrier", "puzzlepiece", "board", "binder", "domino", "keyart", "art"
    ]):
        tools_and_props.append(item)
        
    # Material Blocks, Architectural Slopes, & Rail Tracks
    elif any(x in item_lower for x in [
        "wooden", "stuffed", "glass", "pipe", "rock", "sand", "ice", "water", "flowingwater", 
        "trampoline", "pad", "door", "bars", "pillar", "arch", "reinforced", "dispenser", "slab", 
        "bush", "coral", "clam", "crab", "starfish", "barrel", "web", "disintegratingblock", 
        "block", "store", "room", "stuffingstorage", "stuffingplant", "techweb", "prisonbars", 
        "resetmapblock", "present", "hohoho", "furnace", "cauldron", "stove", "oven", "funnel", 
        "diverter", "fantasy", "map", "rail", "sandstone", "dune", "passageway", "floor", "rug", 
        "keycard", "keyspawner", "carpet", "brick", "wardrobe", "cloud", "stair", "void", "metal", 
        "shaper", "breakable", "crater"
    ]):
        blocks.append(item)
        
    else:
        leftovers.append(item)


# --- 3. DIAGNOSTIC PROFILE DASHBOARD DISPLAY ---

# Unpack clean list data from favorites sub-dictionary list key "_"
fav_list = favorited_items_dict.get('_', [])

import os
import tempfile
import time

# 1. Gather all calculations securely using your active top-level variables
buttcoins = session.raw.get('stats', {}).get('currency', 0)
silver_beans = session.raw.get('stats', {}).get('beans', 0)

unlocked_items = session.raw.get('stats', {}).get('ownedPatterns', [])
fav_list = session.raw.get('stats', {}).get('ownedPatterns_favorite', {}).get('_', [])
hidden_items = session.raw.get('stats', {}).get('ownedPatterns_hidden', [])
active_cosmetics = session.raw.get('stats', {}).get('activeCosmetics', [])
saved_outfits = session.raw.get('stats', {}).get('savedOutfits', [])
owned_bundles = session.raw.get('stats', {}).get('ownedBundles', [])

# 2. Assemble the exact text string layout
dashboard_output = f"""==========================================================
Player: {oculus_username}
Currencies: {buttcoins} Butt-Coins | {silver_beans} Silver Beans
==========================================================
Paintbrushes:                {len(paintbrushes):<4}
Wiring Blocks:               {len(gadgets):<4}
Cosmetics:                   {len(cosmetics):<4}
Music:                       {len(music_and_audio):<4}
Mobs, Pets, NPCs:            {len(mobs_and_npcs):<4}
Weapons:                     {len(weapons_and_bombs):<4}
Interactive items & blocks:  {len(tools_and_props):<4}
Blocks:                      {len(blocks):<4}
Unclassified:                {len(leftovers):<4}
----------------------------------------------------------
Grand Inventory Total:       {len(unlocked_items):<4} items & blocks
==========================================================
Favorited Items:             {len(fav_list):<4} pinned items
Hidden Items:                {len(hidden_items):<4}
Cosmetics Equipped:          {len(active_cosmetics):<4}
Saved Outfits:               {len(saved_outfits):<4}
Total Owned Bundles:         {len(owned_bundles):<4}
==========================================================
"""

# 3. Print out to your monitor screen like usual
print(dashboard_output)

# 4. Generate the temporary physical file block
with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
    temp_file.write(dashboard_output)
    temp_file_path = temp_file.name

# 5. Hand it over to the physical Windows print spooler
os.startfile(temp_file_path, "print")

# 6. Keep the temporary spool alive until hardware rollers finish rolling
time.sleep(5)