# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
# JOSHUA VILLARUEL COMPUTER PROGRAMMING 2  FINAL
import random
import time

accessories_data = {
    "Iron Ring": {"rarity": "Common", "dmg_bonus": 0.05, "desc": "+5% Damage"},
    "Leather Belt": {"rarity": "Common", "hp_bonus": 0.05, "desc": "+5% Health"},
    "Jagged Tooth": {"rarity": "Common", "bleed": True, "desc": "Applies Bleed (3 dmg/turn)"},
    
    "Steel Gauntlet": {"rarity": "Rare", "dmg_bonus": 0.10, "desc": "+10% Damage"},
    "Vitality Amulet": {"rarity": "Rare", "hp_bonus": 0.10, "desc": "+10% Health"},
    "Hunter's Charm": {"rarity": "Rare", "crit_chance": 0.25, "crit_mult": 1.2, "desc": "25% chance to Crit (1.2x dmg)"},
    "Heavy Pommel": {"rarity": "Rare", "stun": True, "desc": "20% chance to Stun enemy"},
    
    "Warlord's Crest": {"rarity": "Epic", "dmg_bonus": 0.20, "desc": "+20% Damage"},
    "Titan's Heart": {"rarity": "Epic", "hp_bonus": 0.20, "desc": "+20% Health"},
    "Executioner's Eye": {"rarity": "Epic", "crit_chance": 0.35, "crit_mult": 1.5, "desc": "35% chance to Crit (1.5x dmg)"}
}

player = {
    "name": "Hero",
    "hp": 30,
    "max_hp": 30,
    "base_attack": 8,
    "potions": 3,
    "accessories": []
}


def update_max_hp():
    bonus_percentage = 0.0
    for item in player["accessories"]:
        if "hp_bonus" in accessories_data[item]:
            bonus_percentage += accessories_data[item]["hp_bonus"]
            
    new_max = int(30 + (30 * bonus_percentage))
    
    hp_difference = new_max - player["max_hp"]
    player["max_hp"] = new_max
    player["hp"] = player["hp"] + hp_difference
    
    if player["hp"] > player["max_hp"]:
        player["hp"] = player["max_hp"]


def spawn_enemy(floor, is_boss):
    if is_boss:
        return {
            "name": "The Dungeon Lord",
            "hp": 50 + (floor * 5),
            "attack": 8 + (floor * 2)
        }
    else:
        names = ["Goblin", "Skeleton", "Orc", "Slime", "Wraith"]
        enemy_name = random.choice(names)
        return {
            "name": enemy_name,
            "hp": random.randint(10, 15) + (floor * 3),
            "attack": random.randint(2, 5) + (floor * 2)
        }


def drop_loot():
    if random.random() < 0.60:
        item_list = list(accessories_data.keys())
        new_item = random.choice(item_list)
        stats = accessories_data[new_item]
        
        print("\n*** LOOT FOUND! ***")
        print(f"You found a [{stats['rarity']}] {new_item}: {stats['desc']}")
        
        if new_item in player["accessories"]:
            print("You already have this equipped. You leave it behind.")
            return

        if len(player["accessories"]) < 3:
            player["accessories"].append(new_item)
            update_max_hp()
            print(f"Equipped {new_item}!")
        else:
            print("\nYour accessory slots are full (Max 3).")
            print("Current Accessories:")
            for i in range(len(player["accessories"])):
                current_item = player["accessories"][i]
                print(f"{i + 1}. {current_item} ({accessories_data[current_item]['desc']})")
                
            choice = input(f"Enter 1, 2, or 3 to replace an item, or 0 to discard the new item: ")
            
            if choice == '1' or choice == '2' or choice == '3':
                index = int(choice) - 1
                old_item = player["accessories"][index]
                player["accessories"][index] = new_item
                update_max_hp()
                print(f"You dropped {old_item} and equipped {new_item}.")
            else:
                print(f"You left the {new_item} behind.")


def play_game():
    print("\n" + "="*40)
    print("   THE DUNGEON DESCENT   ")
    print("="*40)
    
    print("Select Game Mode:")
    print("1. Normal Mode (Escape after Floor 5)")
    print("2. Endless Mode (Descend until you die)")
    
    endless_mode = False
    while True:
        choice = input("Choice (1 or 2): ")
        if choice == '1':
            endless_mode = False
            break
        elif choice == '2':
            endless_mode = True
            break
        else:
            print("Invalid choice. Try again.")
            
    floor = 1
    ##
    
    while player["hp"] > 0:
        print(f"\n--- FLOOR {floor} ---")
        
        if endless_mode == False and floor > 5:
            print("\n" + "="*40)
            print(" You defeated the Dungeon Lord and escaped!")
            print("          VICTORY ACHIEVED          ")
            print("="*40)
            break
            
        print(f"HP: {player['hp']}/{player['max_hp']} | Potions: {player['potions']}")
        
        is_boss = False
        if endless_mode == False and floor == 5:
            is_boss = True
        elif endless_mode == True and floor % 5 == 0:
            is_boss = True
            
        enemy = spawn_enemy(floor, is_boss)
        
        if is_boss:
            print(f"\n*** BOSS BATTLE! {enemy['name']} blocks the exit! ***")
        else:
            print(f"\nA wild {enemy['name']} appears!")
            
        enemy_bleeding = False
        enemy_stunned = False
        
        while enemy["hp"] > 0 and player["hp"] > 0:
            
            if enemy_bleeding == True:
                enemy["hp"] -= 3
                print(f"The {enemy['name']} takes 3 Bleed damage! (HP: {enemy['hp']})")
                if enemy["hp"] <= 0:
                    break

            action = input("\nAction: [A]ttack, [H]eal, [R]un? ").lower()
            
            if action == 'a' or action == 'attack':
                dmg_bonus = 0.0
                crit_chance = 0.0
                crit_mult = 1.0
                can_stun = False
                can_bleed = False
                
                for item in player["accessories"]:
                    stats = accessories_data[item]
                    if "dmg_bonus" in stats:
                        dmg_bonus += stats["dmg_bonus"]
                    if "crit_chance" in stats:
                        crit_chance += stats["crit_chance"]
                        if stats["crit_mult"] > crit_mult:
                            crit_mult = stats["crit_mult"]
                    if "stun" in stats:
                        can_stun = True
                    if "bleed" in stats:
                        can_bleed = True
                        
                base_dmg = random.randint(player["base_attack"] - 2, player["base_attack"] + 2)
                final_dmg = int(base_dmg + (base_dmg * dmg_bonus))
                
                if random.random() < crit_chance:
                    final_dmg = int(final_dmg * crit_mult)
                    print(f"CRITICAL HIT! You strike for {final_dmg} damage!")
                else:
                    print(f"You strike the {enemy['name']} for {final_dmg} damage!")
                    
                enemy["hp"] -= final_dmg
                
                if can_stun == True and random.random() < 0.20:
                    enemy_stunned = True
                    print(f"** The {enemy['name']} is STUNNED! **")
                    
                if can_bleed == True and enemy_bleeding == False:
                    enemy_bleeding = True
                    print(f"** The {enemy['name']} is BLEEDING! **")
                    
            elif action == 'h' or action == 'heal':
                if player["potions"] > 0:
                    healed = random.randint(10, 15)
                    player["hp"] += healed
                    if player["hp"] > player["max_hp"]:
                        player["hp"] = player["max_hp"]
                    player["potions"] -= 1
                    print(f"You heal {healed} HP. (Potions left: {player['potions']})")
                else:
                    print("You are out of potions!")
                    continue
                    
            elif action == 'r' or action == 'run':
                if is_boss:
                    print("You cannot run from a Boss!")
                    continue
                elif random.random() < 0.5:
                    print("You desperately sprint to the next room!")
                    break 
                else:
                    print("You tried to run, but the monster blocked you!")
            else:
                print("Invalid action. Try A, H, or R.")
                continue
                
            if enemy["hp"] > 0 and action != 'r' and action != 'run':
                if enemy_stunned == True:
                    print(f"The {enemy['name']} is stunned and skips its turn!")
                    enemy_stunned = False 
                else:
                    enemy_dmg = random.randint(enemy["attack"] - 1, enemy["attack"] + 1)
                    player["hp"] -= enemy_dmg
                    print(f"The {enemy['name']} hits you for {enemy_dmg} damage!")
                
        if player["hp"] > 0:
            print(f"\n*** You defeated the {enemy['name']}! ***")
            drop_loot()
            floor += 1
            time.sleep(1)
            
    if player["hp"] <= 0:
        print("\n" + "="*40)
        print("                 GAME OVER                 ")
        print(f" You fell in battle. Reached Floor {floor}.")
        print("="*40)


if __name__ == "__main__":
    play_game()
