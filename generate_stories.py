import json
import random

# Base Story Data
STORIES = [
    {
        "id": "adventure",
        "title": "The Lost Treasure of Captain Byte",
        "theme": "Adventure / Exploration",
        "emoji": "🏴‍☠️",
        "description": "You've discovered Captain Byte's ancient map — a legendary pirate who hid a digital treasure across uncharted islands. Navigate jungles, decode ciphers, and survive traps to claim the treasure before it's lost forever."
    },
    {
        "id": "fantasy",
        "title": "The Enchanted Algorithm",
        "theme": "Fantasy / Magic",
        "emoji": "🔮",
        "description": "The Great Source Code of the realm has been shattered by the Dark Compiler. You must travel through enchanted forests and haunted servers to collect the broken fragments and restore magic to the kingdom."
    },
    {
        "id": "scifi",
        "title": "Mission: Deep Space Rescue",
        "theme": "Sci-Fi / Problem-Solving",
        "emoji": "🚀",
        "description": "A distress signal has been received from the outer colonies. As the lead engineer of the USS Voyager, you must navigate asteroid fields, repair broken AI systems, and rescue the stranded colonists."
    },
    {
        "id": "espionage",
        "title": "The Shadow Protocol",
        "theme": "Espionage / Thriller",
        "emoji": "🕵️",
        "description": "An international hacking syndicate known as 'The Null Pointers' has stolen classified global data. Your mission as an elite cyber-spy is to infiltrate their network, crack their security, and recover the files without being detected."
    }
]

# Generate 20 unique chapters per story
def generate_adventure_chapters():
    chapters = []
    
    # 10 Text Puzzles
    text_puzzles = [
        ("The Map Fragment", "You find a torn piece of parchment. A riddle reads: 'I speak without a mouth and hear without ears. What am I?'", "Solve the riddle.", "text", "echo", "Think about sound bouncing."),
        ("The Ancient Lock", "A stone door has numbers carved: 2, 4, 8, 16, ? What is the next number?", "Find the next number.", "text", "32", "Powers of 2."),
        ("The Pirate's Password", "A skeletal parrot squawks: 'The password is the reverse of 'ocean'.'", "What is the password?", "text", "naeco", "Spell it backwards."),
        ("The Compass Rose", "The map says: 'Walk 10 paces North, then 10 East, then 10 South.' What direction are you from the start?", "What direction are you?", "text", "east", "Draw a map on paper."),
        ("The Hidden Message", "A message in a bottle reads: 'H E L L O' but shifted by 1 letter forward.", "Decode the message.", "text", "ifmmp", "Shift every letter by 1."),
        ("The Captain's Age", "The captain was 20 years old 10 years ago. How old is he now?", "Find the captain's age.", "text", "30", "Simple math."),
        ("The River Crossing", "A boat holds 2 people. You have 3 people. How many trips across the river are needed?", "How many trips?", "text", "3", "One person must row back."),
        ("The Golden Coins", "You have 10 coins, 1 is fake and lighter. You have a balance scale. How many weighings to find the fake?", "How many weighings?", "text", "3", "Divide into groups of 3."),
        ("The Cave Riddle", "I have keys but no locks. I have space but no room. You can enter but not go outside. What am I?", "Solve the riddle.", "text", "keyboard", "Think about typing."),
        ("The Final Chest", "A chest requires a 3 digit code. 682: one digit is right and in place. 614: one digit is right but in wrong place. 206: two digits right but wrong place. 738: nothing is correct. 780: one digit right but wrong place.", "What is the code?", "text", "042", "Write down all conditions.")
    ]
    
    # 10 Image Challenges
    image_challenges = [
        ("The Jungle Path", "The jungle requires proof of life. Capture a green guardian.", "Take a picture of a plant or leaf.", "image", "plant", "Any plant will do."),
        ("The Thirst Trap", "You must stay hydrated on this adventure. Show me your water source.", "Take a picture of a cup or bottle.", "image", "bottle", "A glass or bottle."),
        ("The Explorer's Tool", "An explorer needs to record their journey. Show me a writing tool.", "Take a picture of a pen or pencil.", "image", "pen", "A pen or pencil."),
        ("The Rations", "You need energy. Show me some rations.", "Take a picture of a snack or fruit.", "image", "food", "Any food item."),
        ("The Light Source", "The cave is dark. Show me a source of light.", "Take a picture of a lamp or flashlight.", "image", "light", "A lamp, flashlight, or candle."),
        ("The Navigation Device", "You need to find your way. Show me a navigation device.", "Take a picture of a watch or compass.", "image", "watch", "A watch, compass, or phone."),
        ("The Key", "You need a physical key to unlock a chest.", "Take a picture of a key.", "image", "key", "Any metal key."),
        ("The Shield", "You need protection. Show me something that covers you.", "Take a picture of a jacket or hat.", "image", "clothing", "A jacket, hat, or scarf."),
        ("The Artifact", "You found an ancient artifact! Show me something old.", "Take a picture of a book or coin.", "image", "book", "A physical book or coin."),
        ("The Window", "You need to see outside to find the stars.", "Take a picture of a window.", "image", "window", "A window with light.")
    ]
    
    combined = text_puzzles + image_challenges
    random.seed(42) # Deterministic for consistency
    random.shuffle(combined)
    
    for i, item in enumerate(combined):
        chapters.append({
            "id": f"adv_ch{i+1}",
            "title": item[0],
            "narrative": item[1],
            "challenge": item[2],
            "answer_type": item[3],
            "expected_answer": item[4],
            "hint": item[5],
            "difficulty": random.randint(1, 3),
            "points": random.randint(10, 50)
        })
    return chapters


def generate_fantasy_chapters():
    chapters = []
    
    # 10 Text Puzzles
    text_puzzles = [
        ("The Goblin's Riddle", "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "Solve the riddle.", "text", "map", "Think of navigation."),
        ("The Dragon's Math", "If 3 dragons lay 3 eggs in 3 days, how many dragons lay 100 eggs in 100 days?", "Solve the math.", "text", "3", "Rates of work."),
        ("The Spell Book", "A spell requires reversing the word 'MAGIC'.", "Reverse the word.", "text", "cigam", "Read backwards."),
        ("The Elven Sequence", "Elves count: 1, 1, 2, 3, 5, 8, ? What is next?", "Find the next number.", "text", "13", "Fibonacci sequence."),
        ("The Troll Bridge", "A troll demands a toll: 'What has a head and a tail but no body?'", "Solve the riddle.", "text", "coin", "Currency."),
        ("The Wizard's Age", "The wizard is twice as old as his apprentice. The apprentice is 50. How old is the wizard?", "Find the wizard's age.", "text", "100", "Multiplication."),
        ("The Magic Square", "A 3x3 magic square sums to 15. What goes in the center?", "Find the center number.", "text", "5", "Average of 1-9."),
        ("The Potion Mix", "Mix 2 parts red, 3 parts blue. How many parts total?", "Find the sum.", "text", "5", "Addition."),
        ("The Enchanted Mirror", "A mirror shows '101' backwards. What is the number?", "Read the mirror.", "text", "101", "It's a palindrome."),
        ("The King's Crown", "The king's crown is pure gold. It weighs 10kg. The density is 19.3. What is the volume?", "Calculate volume.", "text", "0.51", "Mass / Density.")
    ]
    
    # 10 Image Challenges
    image_challenges = [
        ("The Healing Herb", "Find a healing herb to cure the curse.", "Take a picture of a plant.", "image", "plant", "Any green plant."),
        ("The Magic Wand", "You need a wand to cast the spell.", "Take a picture of a pen, pencil, or stick.", "image", "wand", "A straight stick-like object."),
        ("The Crystal Ball", "Peer into the future. Show me a crystal ball.", "Take a picture of something spherical.", "image", "sphere", "A ball, apple, or globe."),
        ("The Spell Scroll", "You need a scroll to read the ancient text.", "Take a picture of a book or rolled paper.", "image", "scroll", "Paper or a book."),
        ("The Potion Flask", "You need a container for your potion.", "Take a picture of a cup or bottle.", "image", "flask", "A bottle or cup."),
        ("The Guardian's Shield", "Defend against the dragon's fire.", "Take a picture of a plate or flat object.", "image", "shield", "A plate, book cover, etc."),
        ("The Enchanted Ring", "A ring of power is required.", "Take a picture of a ring or circular object.", "image", "ring", "A jewelry ring, key ring, or coin."),
        ("The Familiar", "Summon an animal familiar.", "Take a picture of a pet or stuffed animal.", "image", "animal", "A dog, cat, or plushie."),
        ("The Portal", "Open a portal to the next realm.", "Take a picture of a door or window.", "image", "door", "A doorway or window."),
        ("The Magical Flame", "You need fire to forge the sword.", "Take a picture of a light source.", "image", "fire", "A candle, lamp, or bulb.")
    ]
    
    combined = text_puzzles + image_challenges
    random.seed(43)
    random.shuffle(combined)
    
    for i, item in enumerate(combined):
        chapters.append({
            "id": f"fan_ch{i+1}",
            "title": item[0],
            "narrative": item[1],
            "challenge": item[2],
            "answer_type": item[3],
            "expected_answer": item[4],
            "hint": item[5],
            "difficulty": random.randint(1, 3),
            "points": random.randint(10, 50)
        })
    return chapters


def generate_scifi_chapters():
    chapters = []
    
    # 10 Text Puzzles
    text_puzzles = [
        ("The AI Core", "The AI says: 'Translate binary 1010 to decimal.'", "Convert binary to decimal.", "text", "10", "1*8 + 0*4 + 1*2 + 0*1."),
        ("The Airlock", "The airlock code is prime numbers under 10. What are they?", "List the primes.", "text", "2,3,5,7", "Numbers only divisible by 1 and themselves."),
        ("The Warp Drive", "To engage warp, calculate the square root of 144.", "Calculate the root.", "text", "12", "What number times itself is 144?"),
        ("The Alien Message", "Aliens send: 'Zpv bsf opu bmpof'. Shift back by 1.", "Decode the message.", "text", "you are not alone", "Shift every letter backwards by 1."),
        ("The Navigation Error", "You are at coordinates (0,0). Move +5 X, -3 Y, +2 X. What is your X coordinate?", "Find the X coordinate.", "text", "7", "Add the X movements."),
        ("The Power Grid", "Grid capacity is 100%. Engine takes 40%, Life Support 30%. How much is left?", "Calculate remaining power.", "text", "30", "100 - 40 - 30."),
        ("The Gravity Plating", "Gravity is 9.8 m/s^2. An object falls for 2 seconds. Velocity?", "Calculate velocity.", "text", "19.6", "Multiply g by time."),
        ("The Hologram", "A hologram shows a cube. How many edges does a cube have?", "Count the edges.", "text", "12", "Count them in your head."),
        ("The Time Dilation", "Time runs twice as slow. 1 hour for you is how many for them?", "Calculate time.", "text", "2", "Multiply by 2."),
        ("The Password Override", "The password is the 4th planet from the sun.", "Name the planet.", "text", "mars", "My Very Educated Mother...")
    ]
    
    # 10 Image Challenges
    image_challenges = [
        ("The Tricorder", "Scan the environment. Show a scanning device.", "Take a picture of a phone or remote.", "image", "device", "A smartphone or TV remote."),
        ("The Core Crystal", "Find a power source for the ship.", "Take a picture of a battery or charger.", "image", "battery", "A battery, charger, or plug."),
        ("The Specimen", "Collect a biological specimen.", "Take a picture of a plant or food.", "image", "specimen", "A leaf, fruit, or vegetable."),
        ("The Comm Link", "Establish communications.", "Take a picture of headphones or a speaker.", "image", "audio", "Headphones, earbuds, or speaker."),
        ("The Spacesuit", "Prepare for EVA. Show me protective gear.", "Take a picture of gloves or a jacket.", "image", "gear", "Gloves, jacket, or hat."),
        ("The Viewing Port", "Look out into space.", "Take a picture of a window.", "image", "window", "A window looking outside."),
        ("The Data Disk", "Recover the ship's logs.", "Take a picture of a flash drive, CD, or book.", "image", "data", "Storage media or a physical book."),
        ("The Hull Repair", "Find a tool to fix the breach.", "Take a picture of a tool or tape.", "image", "tool", "Tape, screwdriver, or pen."),
        ("The Rations Replicator", "Replicate some food.", "Take a picture of a packaged snack.", "image", "food", "Any food item."),
        ("The Navigation Star", "Find a celestial body.", "Take a picture of a light bulb.", "image", "star", "A light source representing a star.")
    ]
    
    combined = text_puzzles + image_challenges
    random.seed(44)
    random.shuffle(combined)
    
    for i, item in enumerate(combined):
        chapters.append({
            "id": f"sci_ch{i+1}",
            "title": item[0],
            "narrative": item[1],
            "challenge": item[2],
            "answer_type": item[3],
            "expected_answer": item[4],
            "hint": item[5],
            "difficulty": random.randint(1, 3),
            "points": random.randint(10, 50)
        })
    return chapters


def generate_espionage_chapters():
    chapters = []
    
    # 10 Text Puzzles
    text_puzzles = [
        ("The Drop Point", "The contact says: 'Meet at the 5th prime number street.'", "Find the prime number.", "text", "11", "2, 3, 5, 7, ..."),
        ("The Encrypted File", "Decrypt: 'ZzZ' to 'AaA'. Shift +1.", "What is shift +1 of 'C'?", "text", "D", "Next letter in alphabet."),
        ("The Safe Combo", "The combination is the first 3 digits of Pi.", "What is the combo?", "text", "314", "3.14159..."),
        ("The Laser Grid", "Grid is 5x5. You start at 1,1. Move to 5,5. How many steps minimum? (diagonal allowed)", "Count the steps.", "text", "4", "You can move diagonally."),
        ("The Wire Cut", "Cut the wire that is not red, blue, or green. The options are red, blue, green, yellow.", "Which wire?", "text", "yellow", "Process of elimination."),
        ("The Fingerprint", "A fingerprint has 3 loops and 2 whorls. How many total patterns?", "Add them up.", "text", "5", "Basic addition."),
        ("The Dead Drop", "The dead drop is under the bench with 4 legs. If there are 10 benches, how many legs total?", "Calculate total legs.", "text", "40", "Multiply benches by legs."),
        ("The Surveillance", "Camera 1 rotates 360 degrees in 60s. Degrees per second?", "Calculate rate.", "text", "6", "Divide 360 by 60."),
        ("The Escape Route", "You run 10km/h. The extraction is 5km away. How many minutes?", "Calculate time.", "text", "30", "Half an hour."),
        ("The Identity", "Your alias is 'Mr. Smith'. The reverse is?", "Reverse the string.", "text", "htims .rm", "Read backwards.")
    ]
    
    # 10 Image Challenges
    image_challenges = [
        ("The Gadget", "Show me your spy gadget.", "Take a picture of a phone or watch.", "image", "gadget", "A smartwatch or phone."),
        ("The Disguise", "You need to blend in. Show me a disguise.", "Take a picture of sunglasses or a hat.", "image", "disguise", "Glasses, hat, or scarf."),
        ("The Intel", "Capture the enemy intel.", "Take a picture of a document or screen.", "image", "intel", "Paper with writing or a monitor."),
        ("The Keycard", "Access the secure facility.", "Take a picture of a card (ID, credit card).", "image", "card", "Any plastic card."),
        ("The Escape Vehicle", "We need a ride.", "Take a picture of keys or a car/bike.", "image", "vehicle", "Car keys or a bicycle."),
        ("The Hiding Spot", "Conceal yourself.", "Take a picture of a closet or under a table.", "image", "hide", "A dark space or enclosure."),
        ("The Distraction", "Create a diversion.", "Take a picture of a coin or small object.", "image", "distraction", "A coin, keys, or noisy object."),
        ("The Weapon", "Self-defense is necessary.", "Take a picture of a pen (mightier than the sword).", "image", "pen", "A simple pen or pencil."),
        ("The Wiretap", "Listen to their conversation.", "Take a picture of headphones or a mic.", "image", "audio", "Headphones or earbuds."),
        ("The Safe", "Find where they keep the secrets.", "Take a picture of a box or drawer.", "image", "safe", "A cardboard box or desk drawer.")
    ]
    
    combined = text_puzzles + image_challenges
    random.seed(45)
    random.shuffle(combined)
    
    for i, item in enumerate(combined):
        chapters.append({
            "id": f"esp_ch{i+1}",
            "title": item[0],
            "narrative": item[1],
            "challenge": item[2],
            "answer_type": item[3],
            "expected_answer": item[4],
            "hint": item[5],
            "difficulty": random.randint(1, 3),
            "points": random.randint(10, 50)
        })
    return chapters


def main():
    stories = []
    for base in STORIES:
        story = base.copy()
        if base["id"] == "adventure":
            story["chapters"] = generate_adventure_chapters()
        elif base["id"] == "fantasy":
            story["chapters"] = generate_fantasy_chapters()
        elif base["id"] == "scifi":
            story["chapters"] = generate_scifi_chapters()
        elif base["id"] == "espionage":
            story["chapters"] = generate_espionage_chapters()
        stories.append(story)
        
    with open("stories.json", "w") as f:
        json.dump({"stories": stories}, f, indent=2)
        
    print(f"Generated stories.json with {len(stories)} stories and 20 chapters each.")

if __name__ == "__main__":
    main()
