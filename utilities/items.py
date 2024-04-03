async def replace_aliases(alias: str):
    """Replaces aliases with a format that works for RealmEye"""
    replacements = {
        "t1 dagger": "dirk",
        "t1 bow": "reinforced-bow",
        "t1 staff": "firebrand-staff",
        "t1 wand": "force-wand",
        "t1 sword": "broad-sword",
        "t1 katana": "kendo-stick",
        "t2 dagger": "blue-steel-dagger",
        "t2 bow": "hardwood-bow",
        "t2 staff": "comet-staff",
        "t2 wand": "power-wand",
        "t2 sword": "saber",
        "t2 katana": "plain-katana",
        "t3 dagger": "dusky-rose-dagger",
        "t3 bow": "greywood-bow",
        "t3 staff": "serpentine-staff",
        "t3 wand": "missile-wand",
        "t3 sword": "long-sword",
        "t3 katana": "thunder-katana",
        "t4 dagger": "silver-dagger",
        "t4 bow": "ironwood-bow",
        "t4 staff": "meteor-staff",
        "t4 wand": "eldritch-wand",
        "t4 sword": "falchion",
        "t4 katana": "line-kutter-katana",
        "t5 dagger": "golden-dagger",
        "t5 bow": "fire-bow",
        "t5 staff": "slayer-staff",
        "t5 wand": "hell-s-fire-wand",
        "t5 sword": "fire-sword",
        "t5 katana": "night-edge",
        "t6 dagger": "obsidian-dagger",
        "t6 bow": "sharpshooter-bow",
        "t6 staff": "avenger-staff",
        "t6 wand": "wand-of-dark-magic",
        "t6 sword": "glass-sword",
        "t6 katana": "sky-edge",
        "t7 dagger": "mithril-dagger",
        "t7 bow": "redwood-bow",
        "t7 staff": "staff-of-destruction",
        "t7 wand": "wand-of-arcane-flame",
        "t7 sword": "golden-sword",
        "t7 katana": "buster-katana",
        "t7 blades": "royal-blades",
        "t7 longbow": "hunter-s-longbow",
        "t7 spellblade": "spellblade-of-decimation",
        "t7 morning star": "morning-star-of-mystic-light",
        "t7 flail": "gilded-flail",
        "t7 tachi": "cloudstrike-tachi",
        "t8 dagger": "fire-dagger",
        "t8 bow": "golden-bow",
        "t8 staff": "staff-of-horror",
        "t8 wand": "wand-of-death",
        "t8 sword": "ravenheart-sword",
        "t8 katana": "demon-edge",
        "t8 blades": "blazing-blades",
        "t8 longbow": "gilded-longbow",
        "t8 spellblade": "spellblade-of-nightmares",
        "t8 morning star": "morning-star-of-silent-mourning",
        "t8 flail": "champion-s-flail",
        "t8 tachi": "devilbane-tachi",
        "t9 dagger": "ragetalon-dagger",
        "t9 bow": "verdant-bow",
        "t9 staff": "staff-of-necrotic-arcana",
        "t9 wand": "wand-of-deep-sorcery",
        "t9 sword": "dragonsoul-sword",
        "t9 katana": "jewel-eye-katana",
        "t9 blades": "garnet-blades",
        "t9 longbow": "emerald-longbow",
        "t9 spellblade": "spellblade-of-arcane-magic",
        "t9 morning star": "morning-star-of-hidden-secrets",
        "t9 flail": "drakerider-s-flail",
        "t9 tachi": "darksteel-tachi",
        "t10 dagger": "emeraldshard-dagger",
        "t10 bow": "bow-of-fey-magic",
        "t10 staff": "staff-of-diabolic-secrets",
        "t10 wand": "wand-of-shadow",
        "t10 sword": "archon-sword",
        "t10 katana": "ichimonji",
        "t10 blades": "verdant-blades",
        "t10 longbow": "mystic-longbow",
        "t10 spellblade": "spellblade-of-corrupt-premonitions",
        "t10 morning star": "morning-star-of-the-night",
        "t10 flail": "infernal-flail",
        "t10 tachi": "dragonbone-tachi",
        "t11 dagger": "agateclaw-dagger",
        "t11 bow": "bow-of-innocent-blood",
        "t11 staff": "staff-of-astral-knowledge",
        "t11 wand": "wand-of-ancient-warning",
        "t11 sword": "skysplitter-sword",
        "t11 katana": "muramasa",
        "t11 blades": "occult-blades",
        "t11 longbow": "crimson-longbow",
        "t11 spellblade": "spellblade-of-starry-insight",
        "t11 morning star": "morning-star-of-harrowing-memories",
        "t11 flail": "mithril-flail",
        "t11 tachi": "accursed-tachi",
        "t12 dagger": "dagger-of-foul-malevolence",
        "t12 bow": "bow-of-covert-havens",
        "t12 staff": "staff-of-the-cosmic-whole",
        "t12 wand": "wand-of-recompense",
        "t12 sword": "sword-of-acclaim",
        "t12 katana": "masamune",
        "t12 blades": "bloodshed-blades",
        "t12 longbow": "longbow-of-the-endless-sky",
        "t12 spellblade": "spellblade-of-the-sun",
        "t12 morning star": "morning-star-of-repentance",
        "t12 flail": "celebrant-flail",
        "t12 tachi": "skyslash-tachi",
    }
    
    for aliases, item in replacements.items():
        if aliases in alias:
            alias = alias.replace(aliases, item)
    
    return alias