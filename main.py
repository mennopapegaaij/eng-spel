"""Eng Spel - een simpel clicker-spel met een enge smiley."""

import json
import math
import random
import sys
from array import array
from pathlib import Path

import pygame

from instellingen import *


BASIS_UPGRADES = [
    ("Sterke klik", "+1 per klik", 40, 1, 0),
    ("Spookhulp", "+1 per seconde", 100, 0, 1),
    ("Scherpe klik", "+4 per klik", 180, 4, 0),
    ("Kleine geest", "+4 per seconde", 280, 0, 4),
    ("Snelle vingers", "+10 per klik", 420, 10, 0),
    ("Spokenclub", "+9 per seconde", 620, 0, 9),
    ("Mega klik", "+22 per klik", 900, 22, 0),
    ("Mega spook", "+18 per seconde", 1200, 0, 18),
    ("Donderklik", "+45 per klik", 1700, 45, 0),
    ("Geestenstorm", "+35 per seconde", 2300, 0, 35),
    ("Nachtklauw", "+90 per klik", 3400, 90, 0),
    ("Monsterleger", "+70 per seconde", 4600, 0, 70),
    ("Eindklik", "+200 per klik", 7000, 200, 0),
    ("Nachtkoning", "+150 per seconde", 8500, 0, 150),
    ("Schaduwklauw", "+320 per klik", 10500, 320, 0),
    ("Mistwachter", "+240 per seconde", 12500, 0, 240),
    ("Griezelgrijp", "+460 per klik", 15000, 460, 0),
    ("Gloomspook", "+320 per seconde", 18000, 0, 320),
    ("Donkernagel", "+650 per klik", 22000, 650, 0),
    ("Nachtmist", "+430 per seconde", 27000, 0, 430),
    ("Spookraket", "+900 per klik", 33000, 900, 0),
    ("Huilwind", "+580 per seconde", 40000, 0, 580),
    ("Vampierbeet", "+1250 per klik", 49000, 1250, 0),
    ("Grafwolk", "+780 per seconde", 60000, 0, 780),
    ("Paniekpoot", "+1700 per klik", 74000, 1700, 0),
    ("Schaduwkoor", "+1050 per seconde", 90000, 0, 1050),
    ("Monsterhap", "+2300 per klik", 110000, 2300, 0),
    ("Kerkhofmist", "+1400 per seconde", 135000, 0, 1400),
    ("Donderklauw", "+3100 per klik", 165000, 3100, 0),
    ("Spooktrein", "+1900 per seconde", 200000, 0, 1900),
    ("Nachtstorm", "+4200 per klik", 245000, 4200, 0),
    ("Fluistergrot", "+2600 per seconde", 300000, 0, 2600),
    ("Demonensprong", "+5600 per klik", 365000, 5600, 0),
    ("IJsspoor", "+3500 per seconde", 445000, 0, 3500),
    ("Heksenklap", "+7500 per klik", 540000, 7500, 0),
    ("Spookslot", "+4700 per seconde", 655000, 0, 4700),
    ("Ravenvlucht", "+10000 per klik", 790000, 10000, 0),
    ("Maanschaduw", "+6300 per seconde", 950000, 0, 6300),
    ("Bottenbreker", "+13500 per klik", 1150000, 13500, 0),
    ("Mistleger", "+8400 per seconde", 1380000, 0, 8400),
    ("Dondermonster", "+18000 per klik", 1660000, 18000, 0),
    ("Schimfabriek", "+11200 per seconde", 2000000, 0, 11200),
    ("Nachtkraker", "+24000 per klik", 2400000, 24000, 0),
    ("Donkergolf", "+15000 per seconde", 2880000, 0, 15000),
    ("Spookkanon", "+32000 per klik", 3460000, 32000, 0),
    ("Grafstorm", "+20000 per seconde", 4150000, 0, 20000),
    ("Schaduwbeul", "+43000 per klik", 4980000, 43000, 0),
    ("Dondermaan", "+27000 per seconde", 5980000, 0, 27000),
    ("Hellebeet", "+58000 per klik", 7180000, 58000, 0),
    ("Spookplaneet", "+36000 per seconde", 8620000, 0, 36000),
    ("Krakenklauw", "+78000 per klik", 10350000, 78000, 0),
    ("Eeuwige mist", "+48000 per seconde", 12400000, 0, 48000),
    ("Nachtreus", "+105000 per klik", 14900000, 105000, 0),
    ("Schaduwvloot", "+64000 per seconde", 17900000, 0, 64000),
    ("Bottenstorm", "+142000 per klik", 21500000, 142000, 0),
    ("Griezelkern", "+85000 per seconde", 25800000, 0, 85000),
    ("Hellevlam", "+190000 per klik", 31000000, 190000, 0),
    ("Spookster", "+113000 per seconde", 37200000, 0, 113000),
    ("Donderwolf", "+255000 per klik", 44600000, 255000, 0),
    ("Maanleger", "+150000 per seconde", 53500000, 0, 150000),
    ("Schrikbarst", "+340000 per klik", 64200000, 340000, 0),
    ("Duistere zon", "+200000 per seconde", 77000000, 0, 200000),
    ("Eindmonster", "+460000 per klik", 92400000, 460000, 0),
    ("Spookheelal", "+270000 per seconde", 110000000, 0, 270000),
]
SHOP_VOORVOEGSELS = ["Mist", "Spook", "Schim", "Graf", "Nacht", "Donder", "Helle", "Bot", "Maan", "Duister"]
SHOP_ACHTERVOEGSELS = ["Klauw", "Vlam", "Storm", "Tand", "Wolk", "Beet", "Kern", "Poot", "Golf", "Ster"]
OPSLAAN_BESTAND = Path(__file__).with_name("spelopslag.json")
OPSLAAN_VERSIE = 2
AUTO_OPSLAAN_MS = 5000
LUCKSHOP_START_KOSTEN = 10000
LUCKSHOP_START_FACTOR = 100
LUCKSHOP_VOORVOEGSELS = ["Geluk", "Ster", "Maan", "Fortuin", "Goud", "Klaver", "Wens", "Kroon"]
LUCKSHOP_ACHTERVOEGSELS = ["Regen", "Boost", "Stapel", "Storm", "Ruil", "Sprong", "Schat", "Golf"]
WERELD_BASISPRIJS = 10**66
MUZIEK_SAMPLE_RATE = 22050
MUZIEK_VOLUME = 0.32
MUZIEK_BPM = 120
MUZIEK_LUS_SECONDEN = 16
WERELD_THEMAS = [
    {
        "naam": "Schaduw",
        "punten": "Punten",
        "luckcoins": "Luckcoins",
        "reeksen": ["Maan", "Mist", "Spook", "Nacht"],
        "goud_reeksen": ["Goudmaan", "Goudmist", "Goudspook", "Goudnacht"],
        "kleuren": [(78, 42, 98), (118, 34, 72), (92, 28, 122), (60, 80, 130)],
        "goud_kleuren": [(188, 146, 44), (205, 160, 52), (222, 176, 58), (238, 194, 70)],
    },
    {
        "naam": "Kristal",
        "punten": "Kristalpunten",
        "luckcoins": "Kristalluck",
        "reeksen": ["Glans", "Prisma", "Nova", "Scherf"],
        "goud_reeksen": ["Goudglans", "Goudprisma", "Goudnova", "Goudscherf"],
        "kleuren": [(70, 110, 170), (94, 150, 210), (120, 190, 230), (80, 145, 190)],
        "goud_kleuren": [(180, 175, 78), (210, 190, 90), (236, 208, 110), (196, 166, 70)],
    },
    {
        "naam": "Vlam",
        "punten": "Vlampunten",
        "luckcoins": "Vlamluck",
        "reeksen": ["Sintel", "As", "Gloed", "Kool"],
        "goud_reeksen": ["Goudsintel", "Goudas", "Goudgloed", "Goudkool"],
        "kleuren": [(150, 60, 40), (180, 80, 30), (210, 110, 50), (120, 50, 26)],
        "goud_kleuren": [(194, 148, 52), (220, 166, 70), (240, 190, 82), (174, 130, 45)],
    },
    {
        "naam": "Ster",
        "punten": "Sterpunten",
        "luckcoins": "Sterluck",
        "reeksen": ["Puls", "Comet", "Aura", "Orbit"],
        "goud_reeksen": ["Goudpuls", "Goudcomet", "Goudaura", "Goudorbit"],
        "kleuren": [(70, 60, 150), (110, 90, 180), (150, 110, 210), (85, 80, 170)],
        "goud_kleuren": [(182, 152, 60), (215, 182, 84), (238, 198, 104), (198, 164, 72)],
    },
    {
        "naam": "Storm",
        "punten": "Stormpunten",
        "luckcoins": "Stormluck",
        "reeksen": ["Blik", "Dreun", "Wolk", "Regen"],
        "goud_reeksen": ["Goudblik", "Gouddreun", "Goudwolk", "Goudregen"],
        "kleuren": [(52, 92, 140), (68, 120, 170), (90, 142, 188), (60, 102, 154)],
        "goud_kleuren": [(170, 150, 60), (198, 176, 82), (222, 194, 98), (184, 164, 70)],
    },
    {
        "naam": "Droom",
        "punten": "Droempunten",
        "luckcoins": "Droemluck",
        "reeksen": ["Slaap", "Maan", "Wens", "Nevel"],
        "goud_reeksen": ["Goudslaap", "Goudmaan", "Goudwens", "Goudnevel"],
        "kleuren": [(100, 70, 150), (132, 86, 180), (168, 102, 206), (118, 90, 170)],
        "goud_kleuren": [(176, 150, 68), (210, 180, 90), (236, 204, 112), (190, 164, 76)],
    },
]


def maak_wereld_thema(wereld_nummer):
    """Geef het thema van een wereld."""
    index = max(1, int(wereld_nummer)) - 1
    basis = WERELD_THEMAS[index % len(WERELD_THEMAS)]
    ronde = index // len(WERELD_THEMAS) + 1
    naam = basis["naam"] if ronde == 1 else f"{basis['naam']} {ronde}"
    punten = basis["punten"] if ronde == 1 else f"{basis['punten']} {ronde}"
    luckcoins = basis["luckcoins"] if ronde == 1 else f"{basis['luckcoins']} {ronde}"
    reeksen = basis["reeksen"] if ronde == 1 else [f"{reeks}{ronde}" for reeks in basis["reeksen"]]
    goud_reeksen = basis["goud_reeksen"] if ronde == 1 else [f"{reeks}{ronde}" for reeks in basis["goud_reeksen"]]
    return {
        "nummer": index + 1,
        "naam": naam,
        "punten": punten,
        "luckcoins": luckcoins,
        "reeksen": reeksen,
        "goud_reeksen": goud_reeksen,
        "kleuren": basis["kleuren"],
        "goud_kleuren": basis["goud_kleuren"],
    }


def bereken_wereld_kosten(wereld_nummer):
    """Geef hoeveel punten je nodig hebt voor de volgende wereld."""
    if wereld_nummer <= 1:
        return 0
    return WERELD_BASISPRIJS * (1000 ** (wereld_nummer - 2))


def maak_kaarten(goud=False, wereld_nummer=1):
    """Maak een deck met 48 nummerkaarten: 1 t/m 12, vier keer."""
    thema = maak_wereld_thema(wereld_nummer)
    reeksen = thema["goud_reeksen"] if goud else thema["reeksen"]
    kleuren = thema["goud_kleuren"] if goud else thema["kleuren"]
    kaart_kleuren = list(zip(reeksen, kleuren))
    kaarten = []

    for reeks, kleur in kaart_kleuren:
        for nummer in range(1, 13):
            kaarten.append(
                {
                    "titel": f"{'Gouden ' if goud else ''}{thema['naam']} kaart {nummer}",
                    "uitleg": beschrijf_kaart(nummer, goud),
                    "reeks": reeks,
                    "nummer": nummer,
                    "goud": goud,
                    "kleur": kleur,
                }
            )

    return kaarten


def schud_kaarten(kaarten):
    """Maak een geschudde stapel van het kaartdeck."""
    stapel = [kaart.copy() for kaart in kaarten]
    random.shuffle(stapel)
    return stapel


def maak_kaart_sleutel(kaart):
    """Maak een unieke sleutel voor 1 kaart."""
    return (kaart["reeks"], kaart["nummer"])


def beschrijf_kaart(nummer, goud=False):
    """Geef de uitleg van een nummerkaart."""
    alles_factoren = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 5, 8: 4, 11: 20}
    doel = "Luckcoins" if goud else "Alles"
    if nummer in alles_factoren:
        return f"{doel} x{alles_factoren[nummer]}"
    if nummer == 9:
        return "Luckcoins x11" if goud else "Multiplier x11"
    if nummer == 10:
        return "Luckcoins x30" if goud else "Geld x30"
    if nummer == 12:
        return "Alle 4x kaart 12 = luckcoins x100000" if goud else "Alle 4x kaart 12 = alles x100000"
    return "Geen bonus"


def tel_getrokken_kaarten_van_nummer(getrokken_sleutels, nummer):
    """Tel hoeveel kaarten van een bepaald nummer al zijn getrokken."""
    return sum(1 for _, kaart_nummer in getrokken_sleutels if kaart_nummer == nummer)


def maak_kaart_lookup(kaarten, gouden_kaarten):
    """Maak een snelle lijst om kaarten weer terug te vinden."""
    lookup = {}
    for kaart in kaarten + gouden_kaarten:
        sleutel = (bool(kaart.get("goud", False)), kaart["reeks"], int(kaart["nummer"]))
        lookup[sleutel] = kaart
    return lookup


def kaart_naar_bewaar_data(kaart):
    """Bewaar alleen de simpele kaart-info."""
    if kaart is None:
        return None

    return {
        "reeks": kaart["reeks"],
        "nummer": int(kaart["nummer"]),
        "goud": bool(kaart.get("goud", False)),
    }


def kaart_van_bewaar_data(data, kaart_lookup):
    """Zet bewaarde kaart-info weer om naar een echte kaart."""
    if data is None:
        return None

    sleutel = (bool(data["goud"]), str(data["reeks"]), int(data["nummer"]))
    if sleutel not in kaart_lookup:
        raise KeyError(f"Onbekende kaart in opslag: {sleutel}")
    return kaart_lookup[sleutel].copy()


def sleutels_naar_bewaar_data(getrokken_sleutels):
    """Zet een set met kaartsleutels om naar JSON-data."""
    return [[reeks, nummer] for reeks, nummer in sorted(getrokken_sleutels)]


def sleutels_van_bewaar_data(data):
    """Zet JSON-data weer om naar kaartsleutels."""
    return {(str(reeks), int(nummer)) for reeks, nummer in data}


def maak_nieuwe_wereldtoestand(wereld_nummer):
    """Maak een nieuwe, lege wereld."""
    kaarten = maak_kaarten(wereld_nummer=wereld_nummer)
    gouden_kaarten = maak_kaarten(goud=True, wereld_nummer=wereld_nummer)
    return {
        "wereld_nummer": int(wereld_nummer),
        "punten": START_PUNTEN * 10,
        "klik_kracht": START_KLIK_KRACHT,
        "auto_spoken": START_AUTO_SPOKEN,
        "shop_pagina": 0,
        "luckshop_pagina": 0,
        "multiplier": 10,
        "luckcoins": 0,
        "auto_punten_buffer": 0,
        "luckcoin_buffer": 0,
        "kaarten": kaarten,
        "kaarten_stapel": schud_kaarten(kaarten),
        "gouden_kaarten": gouden_kaarten,
        "gouden_kaarten_stapel": schud_kaarten(gouden_kaarten),
        "kaart_trekkingen": 0,
        "laatste_kaart": None,
        "laatste_kaart_resultaat": "",
        "laatste_gouden_kaart": None,
        "laatste_gouden_kaart_resultaat": "",
        "laatste_luckshop_resultaat": f"Open de luckshop en koop punten x{format_getal(LUCKSHOP_START_FACTOR)}",
        "getrokken_kaart_sleutels": set(),
        "getrokken_gouden_kaart_sleutels": set(),
    }


def maak_nieuwe_speltoestand():
    """Maak een nieuwe, lege opslag met wereld 1."""
    return {"actieve_wereld": 1, "werelden": [maak_nieuwe_wereldtoestand(1)]}


def laad_wereldtoestand_uit_data(data, wereld_nummer):
    """Laad 1 wereld uit opslagdata."""
    wereldtoestand = maak_nieuwe_wereldtoestand(wereld_nummer)
    kaart_lookup = maak_kaart_lookup(wereldtoestand["kaarten"], wereldtoestand["gouden_kaarten"])

    wereldtoestand["punten"] = int(data.get("punten", wereldtoestand["punten"]))
    wereldtoestand["klik_kracht"] = int(data.get("klik_kracht", wereldtoestand["klik_kracht"]))
    wereldtoestand["auto_spoken"] = int(data.get("auto_spoken", wereldtoestand["auto_spoken"]))
    wereldtoestand["shop_pagina"] = max(0, int(data.get("shop_pagina", wereldtoestand["shop_pagina"])))
    wereldtoestand["luckshop_pagina"] = max(0, int(data.get("luckshop_pagina", wereldtoestand["luckshop_pagina"])))
    wereldtoestand["multiplier"] = max(1, int(data.get("multiplier", wereldtoestand["multiplier"])))
    wereldtoestand["luckcoins"] = max(0, int(data.get("luckcoins", wereldtoestand["luckcoins"])))
    wereldtoestand["auto_punten_buffer"] = max(0, int(data.get("auto_punten_buffer", 0)))
    wereldtoestand["luckcoin_buffer"] = max(0, int(data.get("luckcoin_buffer", 0)))
    wereldtoestand["kaart_trekkingen"] = max(0, int(data.get("kaart_trekkingen", 0)))
    wereldtoestand["laatste_kaart_resultaat"] = str(data.get("laatste_kaart_resultaat", ""))
    wereldtoestand["laatste_gouden_kaart_resultaat"] = str(data.get("laatste_gouden_kaart_resultaat", ""))
    wereldtoestand["laatste_luckshop_resultaat"] = str(data.get("laatste_luckshop_resultaat", wereldtoestand["laatste_luckshop_resultaat"]))

    if "kaarten_stapel" in data:
        wereldtoestand["kaarten_stapel"] = [kaart_van_bewaar_data(kaart, kaart_lookup) for kaart in data["kaarten_stapel"]]
    if "gouden_kaarten_stapel" in data:
        wereldtoestand["gouden_kaarten_stapel"] = [kaart_van_bewaar_data(kaart, kaart_lookup) for kaart in data["gouden_kaarten_stapel"]]
    if "laatste_kaart" in data:
        wereldtoestand["laatste_kaart"] = kaart_van_bewaar_data(data["laatste_kaart"], kaart_lookup)
    if "laatste_gouden_kaart" in data:
        wereldtoestand["laatste_gouden_kaart"] = kaart_van_bewaar_data(data["laatste_gouden_kaart"], kaart_lookup)
    if "getrokken_kaart_sleutels" in data:
        wereldtoestand["getrokken_kaart_sleutels"] = sleutels_van_bewaar_data(data["getrokken_kaart_sleutels"])
    if "getrokken_gouden_kaart_sleutels" in data:
        wereldtoestand["getrokken_gouden_kaart_sleutels"] = sleutels_van_bewaar_data(data["getrokken_gouden_kaart_sleutels"])

    return wereldtoestand


def wereld_naar_bewaar_data(wereldtoestand):
    """Zet 1 wereld om naar opslagdata."""
    return {
        "wereld_nummer": int(wereldtoestand["wereld_nummer"]),
        "punten": int(wereldtoestand["punten"]),
        "klik_kracht": int(wereldtoestand["klik_kracht"]),
        "auto_spoken": int(wereldtoestand["auto_spoken"]),
        "shop_pagina": int(wereldtoestand["shop_pagina"]),
        "luckshop_pagina": int(wereldtoestand["luckshop_pagina"]),
        "multiplier": int(wereldtoestand["multiplier"]),
        "luckcoins": int(wereldtoestand["luckcoins"]),
        "auto_punten_buffer": int(wereldtoestand["auto_punten_buffer"]),
        "luckcoin_buffer": int(wereldtoestand["luckcoin_buffer"]),
        "kaart_trekkingen": int(wereldtoestand["kaart_trekkingen"]),
        "laatste_kaart": kaart_naar_bewaar_data(wereldtoestand["laatste_kaart"]),
        "laatste_kaart_resultaat": wereldtoestand["laatste_kaart_resultaat"],
        "laatste_gouden_kaart": kaart_naar_bewaar_data(wereldtoestand["laatste_gouden_kaart"]),
        "laatste_gouden_kaart_resultaat": wereldtoestand["laatste_gouden_kaart_resultaat"],
        "laatste_luckshop_resultaat": wereldtoestand["laatste_luckshop_resultaat"],
        "getrokken_kaart_sleutels": sleutels_naar_bewaar_data(wereldtoestand["getrokken_kaart_sleutels"]),
        "getrokken_gouden_kaart_sleutels": sleutels_naar_bewaar_data(wereldtoestand["getrokken_gouden_kaart_sleutels"]),
        "kaarten_stapel": [kaart_naar_bewaar_data(kaart) for kaart in wereldtoestand["kaarten_stapel"]],
        "gouden_kaarten_stapel": [kaart_naar_bewaar_data(kaart) for kaart in wereldtoestand["gouden_kaarten_stapel"]],
    }


def laad_speltoestand():
    """Laad de voortgang uit het opslagbestand."""
    speltoestand = maak_nieuwe_speltoestand()
    if not OPSLAAN_BESTAND.exists():
        return speltoestand

    try:
        with OPSLAAN_BESTAND.open("r", encoding="utf-8") as bestand:
            data = json.load(bestand)

        versie = int(data.get("versie", 0))
        if versie == 1:
            return {"actieve_wereld": 1, "werelden": [laad_wereldtoestand_uit_data(data, 1)]}
        if versie != OPSLAAN_VERSIE:
            print("De oude opslag past niet meer. Het spel start opnieuw.")
            return speltoestand

        werelden_data = data.get("werelden", [])
        if not werelden_data:
            return speltoestand

        werelden = []
        for index, wereld_data in enumerate(werelden_data, start=1):
            wereld_nummer = max(index, int(wereld_data.get("wereld_nummer", index)))
            werelden.append(laad_wereldtoestand_uit_data(wereld_data, wereld_nummer))

        actieve_wereld = int(data.get("actieve_wereld", 1))
        actieve_wereld = min(max(1, actieve_wereld), len(werelden))
        return {"actieve_wereld": actieve_wereld, "werelden": werelden}
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as fout:
        print(f"Opslag laden mislukte: {fout}")
        return maak_nieuwe_speltoestand()


def sla_spel_op(actieve_wereld, werelden):
    """Sla alle werelden veilig op in een JSON-bestand."""
    opslag_data = {
        "versie": OPSLAAN_VERSIE,
        "actieve_wereld": int(actieve_wereld),
        "werelden": [wereld_naar_bewaar_data(wereldtoestand) for wereldtoestand in werelden],
    }

    tijdelijk_bestand = OPSLAAN_BESTAND.with_suffix(".tmp")
    try:
        with tijdelijk_bestand.open("w", encoding="utf-8") as bestand:
            json.dump(opslag_data, bestand, ensure_ascii=False, indent=2)
        tijdelijk_bestand.replace(OPSLAAN_BESTAND)
    except OSError as fout:
        print(f"Opslaan mislukte: {fout}")


def wis_opslagbestand():
    """Wis het opslagbestand voor een echte nieuwe start."""
    try:
        if OPSLAAN_BESTAND.exists():
            OPSLAAN_BESTAND.unlink()
    except OSError as fout:
        print(f"Opslag wissen mislukte: {fout}")


def pak_wereldvariabelen(wereldtoestand):
    """Haal alle spelwaarden uit 1 wereld."""
    return (
        wereldtoestand["wereld_nummer"],
        wereldtoestand["punten"],
        wereldtoestand["klik_kracht"],
        wereldtoestand["auto_spoken"],
        wereldtoestand["shop_pagina"],
        wereldtoestand["luckshop_pagina"],
        wereldtoestand["multiplier"],
        wereldtoestand["luckcoins"],
        wereldtoestand["auto_punten_buffer"],
        wereldtoestand["luckcoin_buffer"],
        wereldtoestand["kaarten"],
        wereldtoestand["kaarten_stapel"],
        wereldtoestand["gouden_kaarten"],
        wereldtoestand["gouden_kaarten_stapel"],
        wereldtoestand["kaart_trekkingen"],
        wereldtoestand["laatste_kaart"],
        wereldtoestand["laatste_kaart_resultaat"],
        wereldtoestand["laatste_gouden_kaart"],
        wereldtoestand["laatste_gouden_kaart_resultaat"],
        wereldtoestand["laatste_luckshop_resultaat"],
        wereldtoestand["getrokken_kaart_sleutels"],
        wereldtoestand["getrokken_gouden_kaart_sleutels"],
    )


def klem_geluid(waarde):
    """Houd een geluidswaarde tussen -1 en 1."""
    return max(-1.0, min(1.0, waarde))


def noot_naar_hz(noot):
    """Zet een nootnummer om naar Hertz."""
    return 440.0 * (2 ** ((noot - 69) / 12))


def mix_klank(spoor_links, spoor_rechts, index, waarde, pan):
    """Zet 1 geluidswaarde op links en rechts."""
    links_pan = (1.0 - pan) * 0.5
    rechts_pan = (1.0 + pan) * 0.5
    spoor_links[index] += waarde * links_pan
    spoor_rechts[index] += waarde * rechts_pan


def voeg_toon_toe(spoor_links, spoor_rechts, start_tijd, noot, duur, volume, pan, klank):
    """Voeg 1 muziekinstrument toe aan het spoor."""
    start_index = int(start_tijd * MUZIEK_SAMPLE_RATE)
    totaal = int(duur * MUZIEK_SAMPLE_RATE)
    frequentie = noot_naar_hz(noot)

    for stap in range(totaal):
        index = start_index + stap
        if index >= len(spoor_links):
            break

        tijd = stap / MUZIEK_SAMPLE_RATE
        verhouding = stap / max(1, totaal - 1)
        fase = 2 * math.pi * frequentie * tijd

        if klank == "piano":
            golf = math.sin(fase) + 0.45 * math.sin(fase * 2) + 0.2 * math.sin(fase * 3)
            envelop = min(1.0, tijd * 20) * math.exp(-tijd * 3.6)
        elif klank == "gitaar":
            golf = 0.65 * math.sin(fase) + 0.35 * math.sin(fase * 2.02) + 0.25 * math.sin(fase * 4)
            golf = math.tanh(golf * 2.8)
            envelop = min(1.0, tijd * 18) * (1.0 - verhouding * 0.7)
        elif klank == "bas":
            golf = 0.8 * math.sin(fase) + 0.2 * math.sin(fase * 0.5)
            envelop = min(1.0, tijd * 10) * math.exp(-tijd * 1.5)
        else:
            detune = math.sin(2 * math.pi * (frequentie * 1.005) * tijd)
            golf = 0.55 * math.sin(fase) + 0.45 * detune
            envelop = min(1.0, tijd * 1.8) * max(0.0, 1.0 - verhouding * 0.55)

        mix_klank(spoor_links, spoor_rechts, index, golf * envelop * volume, pan)


def voeg_kick_toe(spoor_links, spoor_rechts, start_tijd, volume):
    """Voeg een diepe drumkick toe."""
    start_index = int(start_tijd * MUZIEK_SAMPLE_RATE)
    totaal = int(0.34 * MUZIEK_SAMPLE_RATE)

    for stap in range(totaal):
        index = start_index + stap
        if index >= len(spoor_links):
            break

        tijd = stap / MUZIEK_SAMPLE_RATE
        frequentie = 90 - min(52, tijd * 180)
        fase = 2 * math.pi * frequentie * tijd
        golf = math.sin(fase) + 0.35 * math.sin(fase * 0.5)
        envelop = math.exp(-tijd * 8.5)
        mix_klank(spoor_links, spoor_rechts, index, golf * envelop * volume, 0.0)


def voeg_snare_toe(spoor_links, spoor_rechts, start_tijd, volume, toeval):
    """Voeg een felle snare toe."""
    start_index = int(start_tijd * MUZIEK_SAMPLE_RATE)
    totaal = int(0.22 * MUZIEK_SAMPLE_RATE)

    for stap in range(totaal):
        index = start_index + stap
        if index >= len(spoor_links):
            break

        tijd = stap / MUZIEK_SAMPLE_RATE
        ruis = toeval.uniform(-1.0, 1.0)
        toon = math.sin(2 * math.pi * 190 * tijd)
        envelop = math.exp(-tijd * 14)
        waarde = (ruis * 0.75 + toon * 0.25) * envelop * volume
        mix_klank(spoor_links, spoor_rechts, index, waarde, 0.0)


def voeg_hihat_toe(spoor_links, spoor_rechts, start_tijd, volume, toeval, pan):
    """Voeg een scherpe hi-hat toe."""
    start_index = int(start_tijd * MUZIEK_SAMPLE_RATE)
    totaal = int(0.08 * MUZIEK_SAMPLE_RATE)

    for stap in range(totaal):
        index = start_index + stap
        if index >= len(spoor_links):
            break

        tijd = stap / MUZIEK_SAMPLE_RATE
        ruis = toeval.uniform(-1.0, 1.0)
        ring = math.sin(2 * math.pi * 7200 * tijd)
        envelop = math.exp(-tijd * 28)
        waarde = (ruis * 0.8 + ring * 0.2) * envelop * volume
        mix_klank(spoor_links, spoor_rechts, index, waarde, pan)


def maak_muziek_buffer(wereld_nummer):
    """Bouw een eng loopje met drums, gitaar, piano en extra lagen."""
    totaal_samples = MUZIEK_SAMPLE_RATE * MUZIEK_LUS_SECONDEN
    spoor_links = [0.0] * totaal_samples
    spoor_rechts = [0.0] * totaal_samples
    beat = 60.0 / MUZIEK_BPM
    toeval = random.Random(wereld_nummer * 991)
    grondnoten = [40, 40, 43, 38, 45, 43, 41, 36]
    verschuiving = (wereld_nummer - 1) % 6
    grondnoten = [noot + verschuiving for noot in grondnoten]

    for tel in range(MUZIEK_LUS_SECONDEN * 2):
        start = tel * beat
        beat_in_maat = tel % 4
        maat = tel // 4

        if beat_in_maat in (0, 2):
            voeg_kick_toe(spoor_links, spoor_rechts, start, 0.9)
        if beat_in_maat in (1, 3):
            voeg_snare_toe(spoor_links, spoor_rechts, start, 0.55, toeval)
        voeg_hihat_toe(spoor_links, spoor_rechts, start, 0.18, toeval, -0.25 if tel % 2 == 0 else 0.25)
        voeg_hihat_toe(spoor_links, spoor_rechts, start + beat * 0.5, 0.12, toeval, 0.2 if tel % 2 == 0 else -0.2)

        grondnoot = grondnoten[min(maat, len(grondnoten) - 1)]
        voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot - 12, beat * 1.7, 0.38, -0.1, "bas")

        if beat_in_maat in (0, 2):
            voeg_toon_toe(spoor_links, spoor_rechts, start + beat * 0.08, grondnoot, beat * 0.8, 0.22, 0.3, "gitaar")
            voeg_toon_toe(spoor_links, spoor_rechts, start + beat * 0.28, grondnoot + 7, beat * 0.6, 0.16, -0.35, "gitaar")

        if beat_in_maat == 1:
            voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 12, beat * 1.2, 0.18, -0.4, "piano")
            voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 15, beat * 1.0, 0.14, 0.4, "piano")
        if beat_in_maat == 3:
            voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 7, beat * 1.3, 0.17, 0.35, "piano")
            voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 10, beat * 1.0, 0.12, -0.25, "piano")

    for maat in range(0, 8, 2):
        start = maat * 4 * beat
        grondnoot = grondnoten[min(maat, len(grondnoten) - 1)]
        voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 12, beat * 8, 0.11, -0.2, "pad")
        voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 19, beat * 8, 0.09, 0.2, "pad")
        voeg_toon_toe(spoor_links, spoor_rechts, start, grondnoot + 24, beat * 8, 0.07, 0.0, "pad")

    geluid = array("h")
    for links, rechts in zip(spoor_links, spoor_rechts):
        links_sample = int(klem_geluid(links) * 32767)
        rechts_sample = int(klem_geluid(rechts) * 32767)
        geluid.append(links_sample)
        geluid.append(rechts_sample)

    return geluid.tobytes()


def maak_enge_muziek(wereld_nummer):
    """Maak een pygame-geluid voor de achtergrondmuziek."""
    if pygame.mixer.get_init() is None:
        return None
    return pygame.mixer.Sound(buffer=maak_muziek_buffer(wereld_nummer))


def teken_achtergrond(scherm, teller):
    """Teken de donkere lucht, maan en mist."""
    scherm.fill(ACHTERGROND)

    # Teken een grote maan.
    pygame.draw.circle(scherm, MAAN_KLEUR, (770, 110), 55)
    pygame.draw.circle(scherm, ACHTERGROND, (790, 95), 40)

    # Teken simpele vleermuizen die een beetje bewegen.
    vleermuizen = [(120, 80), (210, 130), (340, 95), (680, 170)]
    for index, (vx, vy) in enumerate(vleermuizen):
        golf = math.sin(teller * 0.04 + index) * 8
        x = vx + int(golf)
        pygame.draw.arc(scherm, SUBTEKST_KLEUR, (x, vy, 18, 10), math.pi, 2 * math.pi, 2)
        pygame.draw.arc(scherm, SUBTEKST_KLEUR, (x + 14, vy, 18, 10), math.pi, 2 * math.pi, 2)

    # Mist onderaan het scherm.
    for i in range(6):
        mist_x = (i * 170 + teller * 0.8) % (SCHERM_BREEDTE + 220) - 110
        pygame.draw.ellipse(scherm, MIST_KLEUR, (mist_x, 380 + (i % 2) * 18, 220, 80))


def bereken_eng_niveau(punten):
    """Geef de eng-kracht terug.

    Dit groeit alleen door punten.
    Een resetbonus telt dus niet mee.
    """
    hele_punten = max(0, int(punten) // 10)
    if hele_punten < 1:
        return 0.0
    return bereken_log10_groot_getal(hele_punten + 1) * 2.6


def bereken_log10_groot_getal(getal):
    """Bereken log10 veilig, ook voor supergrote hele getallen."""
    if getal < 1:
        return 0.0
    if getal < 10**15:
        return math.log10(getal)

    verschuiving = max(0, getal.bit_length() - 52)
    begin_stuk = getal >> verschuiving
    return math.log10(begin_stuk) + verschuiving * math.log10(2)


def schat_grote_int(waarde, eerste_cijfers=3):
    """Schat hoeveel cijfers een groot heel getal heeft en hoe het begint."""
    if waarde == 0:
        return 1, "0" * eerste_cijfers

    if waarde < 10**15:
        tekst = str(waarde)
        return len(tekst), tekst[:eerste_cijfers].ljust(eerste_cijfers, "0")

    log10_waarde = bereken_log10_groot_getal(waarde)
    cijfers = int(log10_waarde) + 1
    mantisse = 10 ** (log10_waarde - (cijfers - 1))
    begin_getal = int(mantisse * (10 ** (eerste_cijfers - 1)))

    minimum = 10 ** (eerste_cijfers - 1)
    maximum = (10 ** eerste_cijfers) - 1
    if begin_getal < minimum:
        begin_getal = minimum
    if begin_getal > maximum:
        begin_getal = maximum

    return cijfers, str(begin_getal).zfill(eerste_cijfers)


def maak_letter_suffix(index):
    """Maak extra suffixen zoals aa, ab, ac ... bx."""
    alfabet = "abcdefghijklmnopqrstuvwxyz"
    waarde = index + 26
    letters = ""

    while waarde >= 0:
        letters = alfabet[waarde % 26] + letters
        waarde = waarde // 26 - 1
        if waarde < 0:
            break

    return letters


def pak_getal_suffix(groep):
    """Pak een korte suffix voor een grote getal-groep."""
    standaard = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]
    if groep < len(standaard):
        return standaard[groep]
    return maak_letter_suffix(groep - len(standaard))


def format_grote_waarde(cijfers, begin, negatief):
    """Maak van grote cijfers een korte tekst met suffix."""
    groep = (cijfers - 1) // 3
    suffix = pak_getal_suffix(groep)
    eerste_stuk = cijfers - groep * 3
    hoofd = begin[:eerste_stuk]
    decimaal = begin[eerste_stuk : eerste_stuk + 1]
    tekst = f"{hoofd}.{decimaal}{suffix}" if decimaal and decimaal != "0" else f"{hoofd}{suffix}"
    return f"-{tekst}" if negatief else tekst


def format_macht_van_tien(macht):
    """Maak 10^macht leesbaar zonder e-notatie."""
    if macht <= 0:
        return "1"

    groep = macht // 3
    rest = macht % 3
    hoofd = str(10 ** rest)
    suffix = pak_getal_suffix(groep)
    return f"{hoofd}{suffix}"


def format_getal(getal):
    """Maak grote getallen kort, zodat ze op het scherm passen."""
    if isinstance(getal, int):
        negatief = getal < 0
        waarde = abs(getal)

        if waarde < 1000:
            tekst = str(waarde)
            return f"-{tekst}" if negatief else tekst

        if waarde < 10**15:
            tekst_getal = str(waarde)
            return format_grote_waarde(len(tekst_getal), tekst_getal + "0", negatief)

        cijfers, begin = schat_grote_int(waarde, 4)
        return format_grote_waarde(cijfers, begin, negatief)

    waarde = float(getal)
    if math.isnan(waarde):
        return "te groot"
    if math.isinf(waarde):
        return "oneindig"

    negatief = waarde < 0
    waarde = abs(waarde)

    if waarde < 1000:
        afgerond = round(waarde, 1)
        tekst = str(int(afgerond)) if afgerond == int(afgerond) else f"{afgerond:.1f}"
        return f"-{tekst}" if negatief else tekst

    log10_waarde = math.log10(waarde)
    cijfers = int(log10_waarde) + 1
    mantisse = 10 ** (log10_waarde - (cijfers - 1))
    begin_getal = int(mantisse * 1000)
    begin_getal = max(1000, min(9999, begin_getal))
    begin = str(begin_getal).zfill(4)
    return format_grote_waarde(cijfers, begin, negatief)


def format_tienden(getal_tienden):
    """Maak een getal met 1 decimaal, zonder zwevende komma-fouten."""
    negatief = getal_tienden < 0
    waarde = abs(int(getal_tienden))
    hele = waarde // 10
    decimaal = waarde % 10

    if hele >= 1000:
        tekst = format_getal(hele)
    elif decimaal == 0:
        tekst = str(hele)
    else:
        tekst = f"{hele}.{decimaal}"

    return f"-{tekst}" if negatief else tekst


def maak_passende_tekst(font, tekst, max_breedte):
    """Knip tekst af met ... zodat hij netjes in een vak past."""
    if font.size(tekst)[0] <= max_breedte:
        return tekst

    puntjes = "..."
    if font.size(puntjes)[0] > max_breedte:
        return puntjes

    kort = tekst
    while kort and font.size(kort + puntjes)[0] > max_breedte:
        kort = kort[:-1]

    return kort + puntjes


def bereken_reset_bonus(punten):
    """Geef de resetbonus terug.

    De bonus groeit binnen 1 speelronde steeds langzamer:
    - +0.1x bij 1000 punten
    - +0.2x bij 3000 punten
    - +0.3x bij 6000 punten
    enzovoort.

    Na een reset begin je weer opnieuw bij het begin.
    """
    hele_punten = max(0, int(punten)) // 10
    stap_budget = (hele_punten * 2) // 1000
    return max(0, (math.isqrt(1 + 4 * stap_budget) - 1) // 2)


def bereken_reset_drempel(punten):
    """Geef de volgende puntengrens voor nog eens +0.1x."""
    volgende_stap = bereken_reset_bonus(punten) + 1
    return (1000 * volgende_stap * (volgende_stap + 1)) // 2


def teken_poppetje(scherm, rect, teller, klik_animatie, punten):
    """Teken een originele enge smiley waar je op moet klikken."""
    x = rect.x
    y = rect.y
    breedte = rect.width
    eng_kracht = bereken_eng_niveau(punten)
    eng_fase = int(eng_kracht)
    basis_niveau = min(eng_kracht, 6)
    extra_niveau = max(0.0, eng_kracht - 6)
    extra_tellen = max(0, int(extra_niveau))

    # Bij een klik wordt de smiley heel even groter.
    extra = 12 if klik_animatie > 0 else 0
    golf = math.sin(teller * (0.05 + eng_kracht * 0.003)) * min(eng_kracht, 18)
    gezicht_midden = (x + breedte // 2, y + 115 + int(golf * 0.5))
    gezicht_straal = int(84 + extra // 2 + min(extra_niveau * 2, 24))
    masker_kleur = (
        int(max(120, 248 - basis_niveau * 8 - extra_tellen * 4)),
        int(max(110, 244 - basis_niveau * 9 - extra_tellen * 5)),
        int(max(120, 238 - basis_niveau * 10 - extra_tellen * 6)),
    )
    rand_kleur = (
        int(min(255, 100 + basis_niveau * 16 + extra_tellen * 6)),
        int(max(0, 35 - extra_tellen * 2)),
        int(min(255, 120 + basis_niveau * 14 + extra_tellen * 8)),
    )
    schaduw_kleur = (
        int(min(255, 55 + basis_niveau * 8 + extra_tellen * 6)),
        10,
        int(min(255, 70 + basis_niveau * 10 + extra_tellen * 8)),
    )
    mond_kleur = ROOD if eng_kracht >= 4 else WIT
    oog_kleur = ROZE if klik_animatie > 0 else ROOD

    # Schaduw onder de smiley.
    pygame.draw.ellipse(
        scherm,
        ZWART,
        (gezicht_midden[0] - 78, gezicht_midden[1] + gezicht_straal - 12, 156, 30),
    )

    # Donkere mist rond de smiley.
    if eng_kracht >= 2:
        wolken = 3 + min(extra_tellen, 5)
        for wolk in range(wolken):
            wolk_hoek = teller * 0.015 + wolk * 1.5
            wolk_x = gezicht_midden[0] + int(math.cos(wolk_hoek) * (gezicht_straal + 18)) - 34
            wolk_y = gezicht_midden[1] + int(math.sin(wolk_hoek) * (30 + wolk * 4)) - 20
            pygame.draw.ellipse(scherm, schaduw_kleur, (wolk_x, wolk_y, 68, 40))

    # Aura-ringen maken de smiley nog dreigender.
    if eng_kracht >= 3:
        ringen = 1 + int(math.sqrt(extra_tellen + 1))
        for ring in range(ringen):
            aura_straal = int(gezicht_straal + 8 + ring * (12 + min(extra_niveau, 10)))
            aura_kleur = (
                int(min(255, 85 + ring * 20 + extra_tellen * 4)),
                20,
                int(min(255, 110 + ring * 20 + extra_tellen * 6)),
            )
            pygame.draw.circle(scherm, aura_kleur, gezicht_midden, aura_straal, 3 if ring == 0 else 2)

    # Grote smiley-kop.
    pygame.draw.circle(scherm, masker_kleur, gezicht_midden, gezicht_straal)
    pygame.draw.circle(scherm, rand_kleur, gezicht_midden, gezicht_straal, 5)
    pygame.draw.circle(scherm, ZWART, gezicht_midden, int(gezicht_straal * 0.78), 2)

    # Kapotte masker-lijnen geven hem een enge, originele look.
    if eng_kracht >= 4:
        scheuren = 3 + min(extra_tellen, 5)
        for scheur in range(scheuren):
            scheur_x = gezicht_midden[0] - 46 + (scheur * 19) % 92
            scheur_y = gezicht_midden[1] - 54 + (scheur * 27) % 112
            pygame.draw.line(scherm, ZWART, (scheur_x, scheur_y), (scheur_x - 8, scheur_y + 24), 3)
            pygame.draw.line(scherm, schaduw_kleur, (scheur_x - 4, scheur_y + 12), (scheur_x + 9, scheur_y + 30), 2)

    # Donkere schaduwhanden achter de smiley.
    if eng_kracht >= 7:
        handen = 4 + min(extra_tellen, 6)
        for hand in range(handen):
            hand_hoek = teller * 0.02 + hand * 1.1
            basis_x = gezicht_midden[0] + int(math.cos(hand_hoek) * (gezicht_straal + 16))
            basis_y = gezicht_midden[1] + int(math.sin(hand_hoek) * 60)
            eind_x = basis_x + int(math.sin(hand_hoek * 1.6) * 16)
            eind_y = basis_y - 34
            pygame.draw.line(scherm, schaduw_kleur, (basis_x, basis_y), (eind_x, eind_y), 5)
            for vinger in range(3):
                pygame.draw.line(
                    scherm,
                    ZWART,
                    (eind_x, eind_y),
                    (eind_x + (vinger - 1) * 9, eind_y - 14 - vinger * 2),
                    2,
                )

    # Ogen.
    pupil_schok = int(math.sin(teller * 0.25) * min(2 + extra_niveau, 6))
    linker_oog = pygame.Rect(gezicht_midden[0] - 52, gezicht_midden[1] - 42, 36, 48)
    rechter_oog = pygame.Rect(gezicht_midden[0] + 16, gezicht_midden[1] - 42, 36, 48)
    pygame.draw.ellipse(scherm, ZWART, linker_oog)
    pygame.draw.ellipse(scherm, ZWART, rechter_oog)
    pygame.draw.ellipse(scherm, oog_kleur, (linker_oog.x + 8, linker_oog.y + 8, 20, 28))
    pygame.draw.ellipse(scherm, oog_kleur, (rechter_oog.x + 8, rechter_oog.y + 8, 20, 28))
    pygame.draw.circle(scherm, ZWART, (linker_oog.centerx + pupil_schok, linker_oog.centery + 4), 8)
    pygame.draw.circle(scherm, ZWART, (rechter_oog.centerx - pupil_schok, rechter_oog.centery + 4), 8)
    pygame.draw.circle(scherm, WIT, (linker_oog.centerx + 4 + pupil_schok, linker_oog.centery - 4), 2)
    pygame.draw.circle(scherm, WIT, (rechter_oog.centerx + 4 - pupil_schok, rechter_oog.centery - 4), 2)
    pygame.draw.line(scherm, ZWART, (linker_oog.x - 4, linker_oog.y + 4), (linker_oog.right + 4, linker_oog.y + 18), 4)
    pygame.draw.line(scherm, ZWART, (rechter_oog.x - 4, rechter_oog.y + 18), (rechter_oog.right + 4, rechter_oog.y + 4), 4)

    if eng_kracht >= 5:
        pygame.draw.circle(scherm, oog_kleur, (gezicht_midden[0], gezicht_midden[1] - 68), 9 + min(extra_tellen, 4))
        pygame.draw.circle(scherm, ZWART, (gezicht_midden[0], gezicht_midden[1] - 68), 5 + min(extra_tellen, 2))

    if eng_kracht >= 8:
        pygame.draw.line(scherm, ROOD, (linker_oog.centerx, linker_oog.bottom - 2), (linker_oog.centerx - 8, linker_oog.bottom + 26), 2)
        pygame.draw.line(scherm, ROOD, (rechter_oog.centerx, rechter_oog.bottom - 2), (rechter_oog.centerx + 8, rechter_oog.bottom + 26), 2)

    # Zwevende oogjes rond de smiley.
    if extra_tellen > 0:
        zwevende_ogen = 2 + int(math.sqrt(extra_tellen) * 3)
        for i in range(zwevende_ogen):
            hoek = teller * 0.02 + i * (math.tau / zwevende_ogen)
            oog_afstand = gezicht_straal + 36 + (i % 4) * 10 + extra_niveau * 1.5
            klein_oog_x = gezicht_midden[0] + int(math.cos(hoek) * oog_afstand)
            klein_oog_y = gezicht_midden[1] + int(math.sin(hoek) * oog_afstand * 0.65)
            klein_oog_straal = 3 + min(extra_tellen // 3, 6)
            pygame.draw.circle(scherm, ZWART, (klein_oog_x, klein_oog_y), klein_oog_straal + 2)
            pygame.draw.circle(scherm, oog_kleur, (klein_oog_x, klein_oog_y), klein_oog_straal)
            pygame.draw.circle(scherm, WIT, (klein_oog_x + 1, klein_oog_y - 1), 1)

    # Glimlach die steeds enger wordt.
    mond_breedte = 112 + min(extra_tellen * 8, 58)
    mond_hoogte = 60 + min(extra_tellen * 4, 26)
    mond_rect = pygame.Rect(
        gezicht_midden[0] - mond_breedte // 2,
        gezicht_midden[1] + 6,
        mond_breedte,
        mond_hoogte,
    )
    if eng_kracht < 2:
        pygame.draw.arc(scherm, WIT, mond_rect, 0.2, math.pi - 0.2, 4)
    else:
        pygame.draw.arc(scherm, mond_kleur, mond_rect, 0.12, math.pi - 0.12, 5)
        pygame.draw.arc(scherm, ZWART, (mond_rect.x, mond_rect.y + 8, mond_rect.width, mond_rect.height), 0.18, math.pi - 0.18, 3)
        pygame.draw.line(scherm, schaduw_kleur, (mond_rect.x + 6, mond_rect.y + 32), (mond_rect.x - 18, mond_rect.y + 16), 3)
        pygame.draw.line(
            scherm,
            schaduw_kleur,
            (mond_rect.right - 6, mond_rect.y + 32),
            (mond_rect.right + 18, mond_rect.y + 16),
            3,
        )

        tanden = 4 + min(extra_tellen + int(basis_niveau), 8)
        tand_afstand = mond_breedte / (tanden + 1)
        for tand in range(tanden):
            tand_midden = int(mond_rect.x + tand_afstand * (tand + 1))
            tand_hoogte = 14 + min(extra_tellen * 2, 16)
            pygame.draw.polygon(
                scherm,
                WIT,
                [
                    (tand_midden - 6, mond_rect.y + 18),
                    (tand_midden, mond_rect.y + 18 + tand_hoogte),
                    (tand_midden + 6, mond_rect.y + 18),
                ],
            )

        if eng_kracht >= 6:
            pygame.draw.line(scherm, schaduw_kleur, (gezicht_midden[0], mond_rect.y + 2), (gezicht_midden[0], mond_rect.bottom - 2), 3)
            pygame.draw.arc(
                scherm,
                ROOD,
                (mond_rect.x + 6, mond_rect.y + 18, mond_rect.width - 12, mond_rect.height - 18),
                math.pi,
                math.tau,
                2,
            )

    # Kleine vonken en krassen maken de smiley nog onrustiger.
    if eng_kracht >= 6:
        vonken = 6 + extra_tellen * 3
        for i in range(vonken):
            hoek = teller * 0.03 + i * (math.tau / max(vonken, 1))
            afstand = gezicht_straal + 24 + (i % 3) * 10 + min(extra_niveau * 5, 70)
            vonk_x = gezicht_midden[0] + int(math.cos(hoek) * afstand)
            vonk_y = gezicht_midden[1] + int(math.sin(hoek) * afstand * 0.8)
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x - 8, vonk_y - 14), 2)
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x + 8, vonk_y - 12), 2)

    if extra_tellen > 0:
        for i in range(extra_tellen * 2):
            kras_x = gezicht_midden[0] - 48 + (i * 17) % 96
            kras_y = gezicht_midden[1] - 46 + (i * 23) % 120
            kras_lengte = 10 + (i % 3) * 4
            pygame.draw.line(scherm, ROOD, (kras_x, kras_y), (kras_x + kras_lengte, kras_y + 6), 2)
            pygame.draw.line(scherm, ZWART, (kras_x + 4, kras_y - 2), (kras_x - 2, kras_y + 8), 2)

    # Kleine waarschuwingstekst op de smiley.
    font = pygame.font.SysFont("Arial", 20, bold=True)
    font_klein = pygame.font.SysFont("Arial", 16, bold=True)
    tekst = font.render("KLIK!", True, GEEL)
    scherm.blit(tekst, (x + breedte // 2 - tekst.get_width() // 2, y + 250))
    niveau_tekst = font_klein.render(f"Eng fase {eng_fase}", True, ROZE)
    scherm.blit(niveau_tekst, (x + breedte // 2 - niveau_tekst.get_width() // 2, y + 273))


def maak_upgrades():
    """Maak de beginlijst voor de oneindige shop."""
    return [
        {"titel": titel, "uitleg": uitleg, "kosten": kosten, "klik_bonus": klik_bonus, "auto_bonus": auto_bonus}
        for titel, uitleg, kosten, klik_bonus, auto_bonus in BASIS_UPGRADES
    ]


def maak_volgende_upgrade(upgrades):
    """Maak precies 1 nieuwe upgrade achteraan de shop."""
    index = len(upgrades)
    nummer = index - len(BASIS_UPGRADES) + 1
    voor = SHOP_VOORVOEGSELS[index % len(SHOP_VOORVOEGSELS)]
    achter = SHOP_ACHTERVOEGSELS[(index // len(SHOP_VOORVOEGSELS)) % len(SHOP_ACHTERVOEGSELS)]
    titel = f"{voor}{achter} {format_getal(nummer)}"
    vorige_kosten = upgrades[-1]["kosten"]

    if index % 2 == 0:
        vorige_bonus = upgrades[-2]["klik_bonus"]
        bonus = (vorige_bonus * 112) // 100 + 5000 + nummer * 15
        kosten = (vorige_kosten * 113) // 100 + bonus * 14
        uitleg = f"+{format_getal(bonus)} klik"
        return {"titel": titel, "uitleg": uitleg, "kosten": kosten, "klik_bonus": bonus, "auto_bonus": 0}

    vorige_bonus = upgrades[-2]["auto_bonus"]
    bonus = (vorige_bonus * 112) // 100 + 3500 + nummer * 12
    kosten = (vorige_kosten * 113) // 100 + bonus * 16
    uitleg = f"+{format_getal(bonus)} /s"
    return {"titel": titel, "uitleg": uitleg, "kosten": kosten, "klik_bonus": 0, "auto_bonus": bonus}


def zorg_voor_upgrades(upgrades, tot_index):
    """Maak alleen zoveel shop-dingen als nu nodig zijn."""
    while len(upgrades) <= tot_index:
        upgrades.append(maak_volgende_upgrade(upgrades))


def pak_shop_upgrades(upgrades, shop_pagina, vakken_per_pagina):
    """Pak alleen de upgrades van de huidige shop-bladzijde."""
    start = shop_pagina * vakken_per_pagina
    eind = start + vakken_per_pagina
    zorg_voor_upgrades(upgrades, eind - 1)
    return upgrades[start:eind]


def maak_luckshop_upgrades():
    """Maak de beginlijst voor de oneindige luckshop."""
    return [maak_volgende_luckshop_upgrade([])]


def maak_volgende_luckshop_upgrade(luckshop_upgrades):
    """Maak precies 1 nieuwe luckshop-upgrade."""
    index = len(luckshop_upgrades)
    nummer = index + 1
    voor = LUCKSHOP_VOORVOEGSELS[index % len(LUCKSHOP_VOORVOEGSELS)]
    achter = LUCKSHOP_ACHTERVOEGSELS[(index // len(LUCKSHOP_VOORVOEGSELS)) % len(LUCKSHOP_ACHTERVOEGSELS)]
    titel = f"{voor}{achter} {format_getal(nummer)}"

    if not luckshop_upgrades:
        return {
            "titel": titel,
            "uitleg": f"Punten x{format_getal(LUCKSHOP_START_FACTOR)}",
            "kosten": LUCKSHOP_START_KOSTEN,
            "punten_factor": LUCKSHOP_START_FACTOR,
        }

    vorige_factor = luckshop_upgrades[-1]["punten_factor"]
    vorige_kosten = luckshop_upgrades[-1]["kosten"]
    factor = (vorige_factor * 118) // 100 + 35 + nummer * 4
    kosten = (vorige_kosten * 145) // 100 + factor * 80
    return {
        "titel": titel,
        "uitleg": f"Punten x{format_getal(factor)}",
        "kosten": kosten,
        "punten_factor": factor,
    }


def zorg_voor_luckshop_upgrades(luckshop_upgrades, tot_index):
    """Maak alleen zoveel luckshop-dingen als nu nodig zijn."""
    while len(luckshop_upgrades) <= tot_index:
        luckshop_upgrades.append(maak_volgende_luckshop_upgrade(luckshop_upgrades))


def pak_luckshop_upgrades(luckshop_upgrades, luckshop_pagina, vakken_per_pagina):
    """Pak alleen de luckshop-dingen van de huidige bladzijde."""
    start = luckshop_pagina * vakken_per_pagina
    eind = start + vakken_per_pagina
    zorg_voor_luckshop_upgrades(luckshop_upgrades, eind - 1)
    return luckshop_upgrades[start:eind]


def teken_paneel(scherm, paneel_rect):
    """Teken het rechter paneel voor punten en upgrades."""
    pygame.draw.rect(scherm, PANEEL_KLEUR, paneel_rect, border_radius=20)
    pygame.draw.rect(scherm, PANEEL_RAND, paneel_rect, 4, border_radius=20)


def maak_shop_vakken(paneel_rect):
    """Maak 8 vakken voor de shop (2 kolommen van 4)."""
    vakken = []
    start_x = paneel_rect.x + 16
    start_y = paneel_rect.y + 254
    breedte = 129
    hoogte = 52
    tussenruimte_x = 10
    tussenruimte_y = 8

    for rij in range(4):
        for kolom in range(2):
            vak_x = start_x + kolom * (breedte + tussenruimte_x)
            vak_y = start_y + rij * (hoogte + tussenruimte_y)
            vakken.append(pygame.Rect(vak_x, vak_y, breedte, hoogte))

    return vakken


def maak_luckshop_vakken(overlay_rect):
    """Maak 8 grote vakken voor de luckshop-overlay."""
    vakken = []
    start_x = overlay_rect.x + 18
    start_y = overlay_rect.y + 106
    breedte = 387
    hoogte = 66
    tussenruimte_x = 10
    tussenruimte_y = 10

    for rij in range(4):
        for kolom in range(2):
            vak_x = start_x + kolom * (breedte + tussenruimte_x)
            vak_y = start_y + rij * (hoogte + tussenruimte_y)
            vakken.append(pygame.Rect(vak_x, vak_y, breedte, hoogte))

    return vakken


def teken_shop_knop(scherm, rect, upgrade, punten, font_titel, font_klein):
    """Teken een klein shop-vak."""
    genoeg = punten >= upgrade["kosten"] * 10
    kleur = KNOP_KLEUR if genoeg else KNOP_UIT
    rand = KNOP_RAND if genoeg else PANEEL_RAND

    pygame.draw.rect(scherm, kleur, rect, border_radius=12)
    pygame.draw.rect(scherm, rand, rect, 2, border_radius=12)

    tekst_breedte = rect.width - 16
    titel = maak_passende_tekst(font_titel, upgrade["titel"], tekst_breedte)
    uitleg = maak_passende_tekst(font_klein, upgrade["uitleg"], tekst_breedte)
    kosten = maak_passende_tekst(font_klein, f"{format_getal(upgrade['kosten'])} p", tekst_breedte)
    titel_tekst = font_titel.render(titel, True, TEKST_KLEUR)
    uitleg_tekst = font_klein.render(uitleg, True, SUBTEKST_KLEUR)
    kosten_tekst = font_klein.render(kosten, True, GEEL)

    scherm.blit(titel_tekst, (rect.x + 8, rect.y + 5))
    scherm.blit(uitleg_tekst, (rect.x + 8, rect.y + 22))
    scherm.blit(kosten_tekst, (rect.x + 8, rect.y + 35))


def teken_luckshop_knop(scherm, rect, upgrade, luckcoins, font_titel, font_klein):
    """Teken 1 luckshop-vak."""
    genoeg = luckcoins >= upgrade["kosten"]
    kleur = KNOP_KLEUR if genoeg else KNOP_UIT
    rand = GEEL if genoeg else PANEEL_RAND

    pygame.draw.rect(scherm, kleur, rect, border_radius=14)
    pygame.draw.rect(scherm, rand, rect, 2, border_radius=14)

    tekst_breedte = rect.width - 18
    titel = maak_passende_tekst(font_titel, upgrade["titel"], tekst_breedte)
    uitleg = maak_passende_tekst(font_klein, upgrade["uitleg"], tekst_breedte)
    kosten = maak_passende_tekst(font_klein, f"{format_tienden(upgrade['kosten'])} luckcoins", tekst_breedte)
    titel_tekst = font_titel.render(titel, True, TEKST_KLEUR)
    uitleg_tekst = font_klein.render(uitleg, True, GEEL)
    kosten_tekst = font_klein.render(kosten, True, SUBTEKST_KLEUR)

    scherm.blit(titel_tekst, (rect.x + 10, rect.y + 6))
    scherm.blit(uitleg_tekst, (rect.x + 10, rect.y + 26))
    scherm.blit(kosten_tekst, (rect.x + 10, rect.y + 44))


def kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina):
    """Ga naar de verste pagina waar je nog iets kunt kopen."""
    while upgrades[-1]["kosten"] * 10 <= punten:
        upgrades.append(maak_volgende_upgrade(upgrades))

    laag = 0
    hoog = len(upgrades) - 1
    laatste_betaalbare_index = -1

    while laag <= hoog:
        midden = (laag + hoog) // 2
        if upgrades[midden]["kosten"] * 10 <= punten:
            laatste_betaalbare_index = midden
            laag = midden + 1
        else:
            hoog = midden - 1

    if laatste_betaalbare_index < 0:
        return shop_pagina

    betaalbare_pagina = laatste_betaalbare_index // vakken_per_pagina
    if betaalbare_pagina > shop_pagina:
        return betaalbare_pagina

    return shop_pagina


def kies_volgende_luckshop_pagina(luckcoins, luckshop_pagina, luckshop_upgrades, vakken_per_pagina):
    """Ga naar de verste luckshop-pagina waar je nog iets kunt kopen."""
    while luckshop_upgrades[-1]["kosten"] <= luckcoins:
        luckshop_upgrades.append(maak_volgende_luckshop_upgrade(luckshop_upgrades))

    laag = 0
    hoog = len(luckshop_upgrades) - 1
    laatste_betaalbare_index = -1

    while laag <= hoog:
        midden = (laag + hoog) // 2
        if luckshop_upgrades[midden]["kosten"] <= luckcoins:
            laatste_betaalbare_index = midden
            laag = midden + 1
        else:
            hoog = midden - 1

    if laatste_betaalbare_index < 0:
        return luckshop_pagina

    betaalbare_pagina = laatste_betaalbare_index // vakken_per_pagina
    if betaalbare_pagina > luckshop_pagina:
        return betaalbare_pagina

    return luckshop_pagina


def bereken_beschikbare_kaart_trekkingen(multiplier):
    """Geef hoeveel gratis kaarttrekkingen je hebt vrijgespeeld."""
    hele_multiplier = max(1, int(multiplier) // 10)
    if hele_multiplier < 10:
        return 0
    return int(bereken_log10_groot_getal(hele_multiplier))


def format_kaart_mijlpaal(stap):
    """Maak de volgende multiplier-mijlpaal netjes leesbaar."""
    return f"x{format_macht_van_tien(stap)}"


def trek_kaart(kaarten_stapel):
    """Trek 1 willekeurige kaart uit het deck."""
    if not kaarten_stapel:
        return None
    return kaarten_stapel.pop()


def pas_kaart_toe(kaart, punten, klik_kracht, auto_spoken, multiplier, luckcoins, getrokken_sleutels):
    """Geef de kaartbonus aan je spelwaarden."""
    nummer = kaart["nummer"]
    alles_factoren = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 5, 8: 4, 11: 20}
    is_gouden_kaart = kaart.get("goud", False)

    if is_gouden_kaart:
        if nummer in alles_factoren:
            factor = alles_factoren[nummer]
            return punten, klik_kracht, auto_spoken, multiplier, luckcoins * factor, f"Luckcoins x{factor}!"

        if nummer == 9:
            return punten, klik_kracht, auto_spoken, multiplier, luckcoins * 11, "Luckcoins x11!"

        if nummer == 10:
            return punten, klik_kracht, auto_spoken, multiplier, luckcoins * 30, "Luckcoins x30!"

        if nummer == 12:
            twaalf_getrokken = tel_getrokken_kaarten_van_nummer(getrokken_sleutels, 12)
            if twaalf_getrokken >= 4:
                factor = 100000
                return punten, klik_kracht, auto_spoken, multiplier, luckcoins * factor, "Alle gouden kaart 12 compleet: luckcoins x100000!"
            return punten, klik_kracht, auto_spoken, multiplier, luckcoins, f"Gouden kaart 12: {twaalf_getrokken}/4 verzameld"

        return punten, klik_kracht, auto_spoken, multiplier, luckcoins, "Geen bonus"

    if nummer in alles_factoren:
        factor = alles_factoren[nummer]
        return (
            punten * factor,
            klik_kracht * factor,
            auto_spoken * factor,
            multiplier * factor,
            luckcoins,
            f"Alles x{factor}!",
        )

    if nummer == 9:
        return punten, klik_kracht, auto_spoken, multiplier * 11, luckcoins, "Multiplier x11!"

    if nummer == 10:
        return punten * 30, klik_kracht, auto_spoken, multiplier, luckcoins, "Geld x30!"

    if nummer == 12:
        twaalf_getrokken = tel_getrokken_kaarten_van_nummer(getrokken_sleutels, 12)
        if twaalf_getrokken >= 4:
            factor = 100000
            return (
                punten * factor,
                klik_kracht * factor,
                auto_spoken * factor,
                multiplier * factor,
                luckcoins,
                "Alle kaart 12 compleet: alles x100000!",
            )
        return punten, klik_kracht, auto_spoken, multiplier, luckcoins, f"Kaart 12: {twaalf_getrokken}/4 verzameld"

    return punten, klik_kracht, auto_spoken, multiplier, luckcoins, "Geen bonus"


def koop_luckshop_bonus(punten, luckcoins, upgrade):
    """Ruil luckcoins voor een grote puntenbonus."""
    if luckcoins < upgrade["kosten"]:
        return punten, luckcoins, "Niet genoeg luckcoins"

    basis_punten = max(10, punten)
    factor = upgrade["punten_factor"]
    nieuwe_punten = basis_punten * factor
    nieuwe_luckcoins = luckcoins - upgrade["kosten"]
    return nieuwe_punten, nieuwe_luckcoins, f"Punten x{format_getal(factor)} gekocht!"


def teken_pagina_knop(scherm, rect, tekst, actief, font):
    """Teken een kleine knop om tussen shop-pagina's te gaan."""
    kleur = KNOP_KLEUR if actief else KNOP_UIT
    rand = KNOP_RAND if actief else PANEEL_RAND
    pygame.draw.rect(scherm, kleur, rect, border_radius=10)
    pygame.draw.rect(scherm, rand, rect, 2, border_radius=10)

    tekst_img = font.render(tekst, True, TEKST_KLEUR)
    scherm.blit(
        tekst_img,
        (rect.x + rect.width // 2 - tekst_img.get_width() // 2, rect.y + 4),
    )


def teken_reset_knop(scherm, rect, punten, multiplier, font, font_klein):
    """Teken de resetknop met de bonus die je nu kunt verdienen."""
    reset_bonus = bereken_reset_bonus(punten)
    reset_drempel = bereken_reset_drempel(punten)
    knop_kleur = KNOP_KLEUR if reset_bonus > 0 else KNOP_UIT
    rand_kleur = ROOD if reset_bonus > 0 else PANEEL_RAND

    pygame.draw.rect(scherm, knop_kleur, rect, border_radius=14)
    pygame.draw.rect(scherm, rand_kleur, rect, 3, border_radius=14)

    bonus_tekst = font.render(f"Reset voor +{format_tienden(reset_bonus)}x", True, TEKST_KLEUR)
    scherm.blit(
        bonus_tekst,
        (rect.x + rect.width // 2 - bonus_tekst.get_width() // 2, rect.y + 10),
    )

    if reset_bonus > 0:
        uitleg = font_klein.render(f"Nieuwe multiplier: x{format_tienden(multiplier + reset_bonus)}", True, GEEL)
    else:
        uitleg = font_klein.render(f"Spaar {format_getal(reset_drempel)} punten voor +0.1x", True, SUBTEKST_KLEUR)

    scherm.blit(
        uitleg,
        (rect.x + rect.width // 2 - uitleg.get_width() // 2, rect.y + 42),
    )


def teken_echte_reset_knop(scherm, rect, font):
    """Teken de knop die alles wist."""
    pygame.draw.rect(scherm, ROOD, rect, border_radius=12)
    pygame.draw.rect(scherm, TEKST_KLEUR, rect, 2, border_radius=12)

    tekst = font.render("Echte reset", True, TEKST_KLEUR)
    scherm.blit(
        tekst,
        (rect.x + rect.width // 2 - tekst.get_width() // 2, rect.y + 7),
    )


def teken_echte_reset_waarschuwing(scherm, overlay_rect, ja_rect, nee_rect, font, font_klein):
    """Teken een waarschuwing voordat alles wordt gewist."""
    dim = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 170))
    scherm.blit(dim, (0, 0))

    pygame.draw.rect(scherm, PANEEL_KLEUR, overlay_rect, border_radius=24)
    pygame.draw.rect(scherm, ROOD, overlay_rect, 4, border_radius=24)

    titel = font.render("Weet je het zeker?", True, TEKST_KLEUR)
    regel1 = font_klein.render("Dan begin je echt helemaal opnieuw.", True, GEEL)
    regel2 = font_klein.render("Punten, multiplier, kaarten en luckcoins", True, SUBTEKST_KLEUR)
    regel3 = font_klein.render("worden dan helemaal gewist.", True, SUBTEKST_KLEUR)
    scherm.blit(titel, (overlay_rect.x + 36, overlay_rect.y + 24))
    scherm.blit(regel1, (overlay_rect.x + 36, overlay_rect.y + 74))
    scherm.blit(regel2, (overlay_rect.x + 36, overlay_rect.y + 104))
    scherm.blit(regel3, (overlay_rect.x + 36, overlay_rect.y + 128))

    pygame.draw.rect(scherm, ROOD, ja_rect, border_radius=12)
    pygame.draw.rect(scherm, TEKST_KLEUR, ja_rect, 2, border_radius=12)
    ja_tekst = font_klein.render("Ja, wis alles", True, TEKST_KLEUR)
    scherm.blit(
        ja_tekst,
        (ja_rect.x + ja_rect.width // 2 - ja_tekst.get_width() // 2, ja_rect.y + 11),
    )

    pygame.draw.rect(scherm, KNOP_KLEUR, nee_rect, border_radius=12)
    pygame.draw.rect(scherm, KNOP_RAND, nee_rect, 2, border_radius=12)
    nee_tekst = font_klein.render("Nee", True, TEKST_KLEUR)
    scherm.blit(
        nee_tekst,
        (nee_rect.x + nee_rect.width // 2 - nee_tekst.get_width() // 2, nee_rect.y + 11),
    )


def teken_werelden_knop(scherm, rect, font):
    """Teken de knop om het werelden-scherm te openen."""
    pygame.draw.rect(scherm, KNOP_KLEUR, rect, border_radius=12)
    pygame.draw.rect(scherm, KNOP_RAND, rect, 2, border_radius=12)
    tekst = font.render("Werelden", True, TEKST_KLEUR)
    scherm.blit(
        tekst,
        (rect.x + rect.width // 2 - tekst.get_width() // 2, rect.y + 7),
    )


def maak_wereld_vakken(overlay_rect):
    """Maak vakken voor 4 werelden per pagina."""
    vakken = []
    start_x = overlay_rect.x + 20
    start_y = overlay_rect.y + 100
    breedte = 378
    hoogte = 86
    tussenruimte_x = 12
    tussenruimte_y = 12

    for rij in range(2):
        for kolom in range(2):
            vak_x = start_x + kolom * (breedte + tussenruimte_x)
            vak_y = start_y + rij * (hoogte + tussenruimte_y)
            vakken.append(pygame.Rect(vak_x, vak_y, breedte, hoogte))

    return vakken


def teken_wereld_knop(scherm, rect, wereld_nummer, actief, ontgrendeld, wereld_naam, wereld_punten, font, font_klein):
    """Teken 1 wereldknop in het overzicht."""
    kleur = KNOP_KLEUR if ontgrendeld else KNOP_UIT
    rand = GEEL if actief else KNOP_RAND if ontgrendeld else PANEEL_RAND
    pygame.draw.rect(scherm, kleur, rect, border_radius=16)
    pygame.draw.rect(scherm, rand, rect, 3 if actief else 2, border_radius=16)

    titel = font.render(maak_passende_tekst(font, f"Wereld {format_getal(wereld_nummer)}: {wereld_naam}", rect.width - 20), True, TEKST_KLEUR)
    status_regel = "Actief" if actief else "Ga naar deze wereld" if ontgrendeld else "Nog vergrendeld"
    status = font_klein.render(maak_passende_tekst(font_klein, status_regel, rect.width - 20), True, GEEL if actief else SUBTEKST_KLEUR)
    punten_regel = font_klein.render(maak_passende_tekst(font_klein, f"Punten hier: {format_tienden(wereld_punten)}", rect.width - 20), True, SUBTEKST_KLEUR)
    scherm.blit(titel, (rect.x + 10, rect.y + 8))
    scherm.blit(status, (rect.x + 10, rect.y + 38))
    scherm.blit(punten_regel, (rect.x + 10, rect.y + 58))


def teken_werelden_overzicht(
    scherm,
    overlay_rect,
    sluit_rect,
    vorige_rect,
    volgende_rect,
    koop_rect,
    wereld_vakken,
    werelden,
    actieve_wereld,
    wereld_pagina,
    koop_kosten,
    huidig_wereld_punten,
    font,
    font_klein,
):
    """Teken het overzicht van alle werelden."""
    dim = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 165))
    scherm.blit(dim, (0, 0))

    pygame.draw.rect(scherm, PANEEL_KLEUR, overlay_rect, border_radius=24)
    pygame.draw.rect(scherm, PANEEL_RAND, overlay_rect, 4, border_radius=24)

    titel = font.render("Werelden", True, TEKST_KLEUR)
    uitleg = font_klein.render("Elke wereld heeft eigen punten, kaarten en luckcoins.", True, SUBTEKST_KLEUR)
    scherm.blit(titel, (overlay_rect.x + 20, overlay_rect.y + 16))
    scherm.blit(uitleg, (overlay_rect.x + 22, overlay_rect.y + 52))

    pygame.draw.rect(scherm, KNOP_KLEUR, sluit_rect, border_radius=10)
    pygame.draw.rect(scherm, KNOP_RAND, sluit_rect, 2, border_radius=10)
    sluit_tekst = font_klein.render("Sluiten", True, TEKST_KLEUR)
    scherm.blit(
        sluit_tekst,
        (sluit_rect.x + sluit_rect.width // 2 - sluit_tekst.get_width() // 2, sluit_rect.y + 6),
    )

    teken_pagina_knop(scherm, vorige_rect, "<", wereld_pagina > 0, font_klein)
    teken_pagina_knop(scherm, volgende_rect, ">", (wereld_pagina + 1) * len(wereld_vakken) < len(werelden), font_klein)

    start = wereld_pagina * len(wereld_vakken)
    zichtbare_werelden = werelden[start : start + len(wereld_vakken)]
    for wereldtoestand, rect in zip(zichtbare_werelden, wereld_vakken):
        thema = maak_wereld_thema(wereldtoestand["wereld_nummer"])
        teken_wereld_knop(
            scherm,
            rect,
            wereldtoestand["wereld_nummer"],
            wereldtoestand["wereld_nummer"] == actieve_wereld,
            True,
            thema["naam"],
            wereldtoestand["punten"],
            font_klein,
            font_klein,
        )

    volgende_wereld = len(werelden) + 1
    koop_kleur = KNOP_KLEUR if huidig_wereld_punten >= koop_kosten * 10 else KNOP_UIT
    koop_rand = GEEL if huidig_wereld_punten >= koop_kosten * 10 else PANEEL_RAND
    pygame.draw.rect(scherm, koop_kleur, koop_rect, border_radius=16)
    pygame.draw.rect(scherm, koop_rand, koop_rect, 2, border_radius=16)
    koop_titel = font_klein.render(f"Koop wereld {format_getal(volgende_wereld)}", True, TEKST_KLEUR)
    koop_uitleg = font_klein.render(maak_passende_tekst(font_klein, f"Kost {format_getal(koop_kosten)} punten", koop_rect.width - 20), True, GEEL)
    koop_hint = font_klein.render("Nieuwe punten, nieuwe kaarten en nieuwe luckcoins.", True, SUBTEKST_KLEUR)
    scherm.blit(koop_titel, (koop_rect.x + 14, koop_rect.y + 10))
    scherm.blit(koop_uitleg, (koop_rect.x + 14, koop_rect.y + 36))
    scherm.blit(koop_hint, (koop_rect.x + 14, koop_rect.y + 60))


def teken_luckshop_overzicht(
    scherm,
    overlay_rect,
    sluit_rect,
    vorige_rect,
    volgende_rect,
    luckshop_upgrades,
    luckshop_pagina,
    luckshop_vakken,
    luckcoins,
    luckcoins_naam,
    laatste_luckshop_resultaat,
    font,
    font_klein,
):
    """Teken de oneindige luckshop met pagina's."""
    dim = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 160))
    scherm.blit(dim, (0, 0))

    pygame.draw.rect(scherm, PANEEL_KLEUR, overlay_rect, border_radius=24)
    pygame.draw.rect(scherm, PANEEL_RAND, overlay_rect, 4, border_radius=24)

    titel = font.render("Luckshop", True, TEKST_KLEUR)
    uitleg = font_klein.render("Ruil luckcoins voor heel veel normale punten.", True, SUBTEKST_KLEUR)
    luckcoins_tekst = font_klein.render(maak_passende_tekst(font_klein, f"{luckcoins_naam}: {format_tienden(luckcoins)}", 330), True, GEEL)
    pagina_tekst = font_klein.render(f"Pagina {luckshop_pagina + 1}", True, SUBTEKST_KLEUR)
    resultaat_tekst = font_klein.render(maak_passende_tekst(font_klein, laatste_luckshop_resultaat, overlay_rect.width - 40), True, GEEL)
    scherm.blit(titel, (overlay_rect.x + 20, overlay_rect.y + 16))
    scherm.blit(uitleg, (overlay_rect.x + 22, overlay_rect.y + 52))
    scherm.blit(luckcoins_tekst, (overlay_rect.x + 22, overlay_rect.y + 76))
    scherm.blit(pagina_tekst, (overlay_rect.x + 510, overlay_rect.y + 22))
    scherm.blit(resultaat_tekst, (overlay_rect.x + 22, overlay_rect.bottom - 30))

    pygame.draw.rect(scherm, KNOP_KLEUR, sluit_rect, border_radius=10)
    pygame.draw.rect(scherm, KNOP_RAND, sluit_rect, 2, border_radius=10)
    sluit_tekst = font_klein.render("Sluiten", True, TEKST_KLEUR)
    scherm.blit(
        sluit_tekst,
        (sluit_rect.x + sluit_rect.width // 2 - sluit_tekst.get_width() // 2, sluit_rect.y + 6),
    )

    teken_pagina_knop(scherm, vorige_rect, "<", luckshop_pagina > 0, font_klein)
    teken_pagina_knop(scherm, volgende_rect, ">", True, font_klein)

    zichtbare_upgrades = pak_luckshop_upgrades(luckshop_upgrades, luckshop_pagina, len(luckshop_vakken))
    for upgrade, rect in zip(zichtbare_upgrades, luckshop_vakken):
        teken_luckshop_knop(scherm, rect, upgrade, luckcoins, font, font_klein)


def teken_kaart_paneel(
    scherm,
    paneel_rect,
    knop_rect,
    overzicht_knop_rect,
    luckshop_knop_rect,
    multiplier,
    luckcoins,
    luckcoins_naam,
    luckshop_pagina,
    laatste_kaart,
    laatste_kaart_resultaat,
    laatste_gouden_kaart,
    laatste_gouden_kaart_resultaat,
    laatste_luckshop_resultaat,
    kaart_trekkingen,
    kaarten_stapel,
    gouden_kaarten_stapel,
    getrokken_gouden_sleutels,
    font,
    font_klein,
):
    """Teken het kaart-paneel."""
    kaart_beschikbaar = bereken_beschikbare_kaart_trekkingen(multiplier)
    kaarten_over = min(len(kaarten_stapel), max(0, kaart_beschikbaar - kaart_trekkingen))
    volgende_kaart = format_kaart_mijlpaal(kaart_trekkingen + 1)
    paneel_breedte = paneel_rect.width - 36

    pygame.draw.rect(scherm, PANEEL_KLEUR, paneel_rect, border_radius=20)
    pygame.draw.rect(scherm, PANEEL_RAND, paneel_rect, 4, border_radius=20)

    titel = font.render("Kaarten", True, TEKST_KLEUR)
    if not kaarten_stapel:
        status_tekst = "Deck compleet!"
    elif kaarten_over > 0:
        status_tekst = f"Vrije kaarten: {kaarten_over}"
    else:
        status_tekst = f"Volgende kaart bij {volgende_kaart}"
    status = font_klein.render(maak_passende_tekst(font_klein, status_tekst, paneel_breedte), True, GEEL if kaarten_over > 0 or not kaarten_stapel else SUBTEKST_KLEUR)
    deck_tekst = font_klein.render(maak_passende_tekst(font_klein, f"Normaal deck: {len(kaarten_stapel)}/48", paneel_breedte), True, SUBTEKST_KLEUR)
    goud_tekst = font_klein.render(maak_passende_tekst(font_klein, f"Goud deck: {len(gouden_kaarten_stapel)}/48", paneel_breedte), True, GEEL)
    scherm.blit(titel, (paneel_rect.x + 16, paneel_rect.y + 12))
    scherm.blit(status, (paneel_rect.x + 18, paneel_rect.y + 42))
    scherm.blit(deck_tekst, (paneel_rect.x + 18, paneel_rect.y + 60))
    scherm.blit(goud_tekst, (paneel_rect.x + 18, paneel_rect.y + 78))

    kaart_rect = pygame.Rect(paneel_rect.x + 16, paneel_rect.y + 104, paneel_rect.width - 32, 78)
    kaart_breedte = kaart_rect.width - 20
    if laatste_kaart:
        pygame.draw.rect(scherm, laatste_kaart["kleur"], kaart_rect, border_radius=16)
        pygame.draw.rect(scherm, KNOP_RAND, kaart_rect, 2, border_radius=16)
        kaart_titel = font.render(maak_passende_tekst(font, laatste_kaart["titel"], kaart_breedte), True, TEKST_KLEUR)
        kaart_uitleg = font_klein.render(maak_passende_tekst(font_klein, laatste_kaart["uitleg"], kaart_breedte), True, WIT)
        kaart_resultaat = font_klein.render(maak_passende_tekst(font_klein, laatste_kaart_resultaat, kaart_breedte), True, GEEL)
        kaart_info = font_klein.render(maak_passende_tekst(font_klein, f"Laatste kaart - {laatste_kaart['reeks']}", kaart_breedte), True, GEEL)
        scherm.blit(kaart_info, (kaart_rect.x + 10, kaart_rect.y + 8))
        scherm.blit(kaart_titel, (kaart_rect.x + 10, kaart_rect.y + 24))
        scherm.blit(kaart_uitleg, (kaart_rect.x + 10, kaart_rect.y + 44))
        scherm.blit(kaart_resultaat, (kaart_rect.x + 10, kaart_rect.y + 58))
    else:
        pygame.draw.rect(scherm, KNOP_UIT, kaart_rect, border_radius=16)
        pygame.draw.rect(scherm, PANEEL_RAND, kaart_rect, 2, border_radius=16)
        kaart_info = font.render("Nog geen kaart", True, TEKST_KLEUR)
        kaart_uitleg = font_klein.render(maak_passende_tekst(font_klein, "48 random kaarten: 1 t/m 12, vier keer", kaart_breedte), True, SUBTEKST_KLEUR)
        scherm.blit(kaart_info, (kaart_rect.x + 10, kaart_rect.y + 18))
        scherm.blit(kaart_uitleg, (kaart_rect.x + 10, kaart_rect.y + 46))

    genoeg = kaarten_over > 0
    knop_kleur = KNOP_KLEUR if genoeg else KNOP_UIT
    knop_rand = KNOP_RAND if genoeg else PANEEL_RAND
    pygame.draw.rect(scherm, knop_kleur, knop_rect, border_radius=14)
    pygame.draw.rect(scherm, knop_rand, knop_rect, 2, border_radius=14)

    knop_tekst = font.render("Trek kaart", True, TEKST_KLEUR)
    if not kaarten_stapel:
        kosten_regel = "Alle 48 kaarten zijn getrokken!"
    elif kaarten_over > 0:
        kosten_regel = "Gratis bij deze milestone!"
    else:
        kosten_regel = f"Haal eerst {volgende_kaart}"
    kosten_tekst = font_klein.render(maak_passende_tekst(font_klein, kosten_regel, knop_rect.width - 16), True, GEEL)
    scherm.blit(knop_tekst, (knop_rect.x + knop_rect.width // 2 - knop_tekst.get_width() // 2, knop_rect.y + 6))
    scherm.blit(kosten_tekst, (knop_rect.x + knop_rect.width // 2 - kosten_tekst.get_width() // 2, knop_rect.y + 32))

    pygame.draw.rect(scherm, KNOP_KLEUR, overzicht_knop_rect, border_radius=12)
    pygame.draw.rect(scherm, KNOP_RAND, overzicht_knop_rect, 2, border_radius=12)
    overzicht_tekst = font_klein.render("Bekijk kaarten", True, TEKST_KLEUR)
    scherm.blit(
        overzicht_tekst,
        (
            overzicht_knop_rect.x + overzicht_knop_rect.width // 2 - overzicht_tekst.get_width() // 2,
            overzicht_knop_rect.y + 8,
        ),
    )

    genoeg_luckcoins = luckcoins >= LUCKSHOP_START_KOSTEN
    luckshop_kleur = KNOP_KLEUR
    luckshop_rand = GEEL if genoeg_luckcoins else KNOP_RAND
    pygame.draw.rect(scherm, luckshop_kleur, luckshop_knop_rect, border_radius=12)
    pygame.draw.rect(scherm, luckshop_rand, luckshop_knop_rect, 2, border_radius=12)
    luckshop_titel = font.render(maak_passende_tekst(font, "Open luckshop", luckshop_knop_rect.width - 16), True, TEKST_KLEUR)
    luckshop_kosten = font_klein.render(maak_passende_tekst(font_klein, "Oneindig met bladzijdes", luckshop_knop_rect.width - 16), True, GEEL)
    scherm.blit(
        luckshop_titel,
        (luckshop_knop_rect.x + luckshop_knop_rect.width // 2 - luckshop_titel.get_width() // 2, luckshop_knop_rect.y + 4),
    )
    scherm.blit(
        luckshop_kosten,
        (luckshop_knop_rect.x + luckshop_knop_rect.width // 2 - luckshop_kosten.get_width() // 2, luckshop_knop_rect.y + 27),
    )

    luckcoins_tekst = font_klein.render(maak_passende_tekst(font_klein, f"{luckcoins_naam}: {format_tienden(luckcoins)}", paneel_breedte), True, GEEL)
    luckshop_pagina_tekst = font_klein.render(maak_passende_tekst(font_klein, f"Luckshop pagina: {luckshop_pagina + 1}", paneel_breedte), True, SUBTEKST_KLEUR)
    luckshop_resultaat = font_klein.render(maak_passende_tekst(font_klein, laatste_luckshop_resultaat, paneel_breedte), True, GEEL if genoeg_luckcoins else SUBTEKST_KLEUR)
    scherm.blit(luckcoins_tekst, (paneel_rect.x + 18, paneel_rect.y + 342))
    scherm.blit(luckshop_pagina_tekst, (paneel_rect.x + 18, paneel_rect.y + 362))
    scherm.blit(luckshop_resultaat, (paneel_rect.x + 18, paneel_rect.y + 382))

    if laatste_gouden_kaart:
        goud_resultaat_regel = f"Goud: {laatste_gouden_kaart['titel']}"
        goud_uitleg_regel = laatste_gouden_kaart_resultaat
    else:
        goud_resultaat_regel = "Gouden kaart: nog geen"
        goud_uitleg_regel = "Voltooi een normaal deck voor 1 gouden kaart."
    goud_resultaat = font_klein.render(maak_passende_tekst(font_klein, goud_resultaat_regel, paneel_breedte), True, KNOP_RAND)
    goud_uitleg = font_klein.render(maak_passende_tekst(font_klein, goud_uitleg_regel, paneel_breedte), True, TEKST_KLEUR if laatste_gouden_kaart else SUBTEKST_KLEUR)
    scherm.blit(goud_resultaat, (paneel_rect.x + 18, paneel_rect.y + 392))
    scherm.blit(goud_uitleg, (paneel_rect.x + 18, paneel_rect.y + 410))


def teken_deck_grid(scherm, deck_rect, titel, kaarten, getrokken_sleutels, font, font_klein):
    """Teken 1 kaartdeck als rooster."""
    pygame.draw.rect(scherm, KNOP_UIT, deck_rect, border_radius=18)
    pygame.draw.rect(scherm, PANEEL_RAND, deck_rect, 2, border_radius=18)

    getrokken = len(getrokken_sleutels)
    mist = len(kaarten) - getrokken
    titel_tekst = font.render(titel, True, TEKST_KLEUR)
    status = font_klein.render(f"Getrokken: {getrokken}/48   Nog: {mist}", True, GEEL)
    scherm.blit(titel_tekst, (deck_rect.x + 16, deck_rect.y + 12))
    scherm.blit(status, (deck_rect.x + 16, deck_rect.y + 40))

    start_x = deck_rect.x + 64
    start_y = deck_rect.y + 78
    cel_breedte = 24
    cel_hoogte = 40
    series = [kaart["reeks"] for kaart in kaarten[::12]]

    for rij, reeks in enumerate(series):
        rij_y = start_y + rij * 52
        reeks_kaart = next(kaart for kaart in kaarten if kaart["reeks"] == reeks)
        reeks_tekst = font_klein.render(reeks, True, reeks_kaart["kleur"])
        scherm.blit(reeks_tekst, (deck_rect.x + 12, rij_y + 10))

        for nummer in range(1, 13):
            kaart = next(kaart for kaart in kaarten if kaart["reeks"] == reeks and kaart["nummer"] == nummer)
            kaart_rect = pygame.Rect(start_x + (nummer - 1) * cel_breedte, rij_y, 20, cel_hoogte)
            sleutel = maak_kaart_sleutel(kaart)
            getrokken_kleur = kaart["kleur"] if sleutel in getrokken_sleutels else KNOP_UIT
            rand_kleur = KNOP_RAND if sleutel in getrokken_sleutels else PANEEL_RAND
            pygame.draw.rect(scherm, getrokken_kleur, kaart_rect, border_radius=6)
            pygame.draw.rect(scherm, rand_kleur, kaart_rect, 2, border_radius=6)

            nummer_tekst = font_klein.render(str(nummer), True, TEKST_KLEUR)
            scherm.blit(
                nummer_tekst,
                (kaart_rect.x + kaart_rect.width // 2 - nummer_tekst.get_width() // 2, kaart_rect.y + 4),
            )

            status_tekst = font_klein.render("JA" if sleutel in getrokken_sleutels else ".", True, GEEL if sleutel in getrokken_sleutels else SUBTEKST_KLEUR)
            scherm.blit(
                status_tekst,
                (kaart_rect.x + kaart_rect.width // 2 - status_tekst.get_width() // 2, kaart_rect.y + 20),
            )


def teken_kaart_overzicht(
    scherm,
    overlay_rect,
    sluit_rect,
    kaarten,
    getrokken_sleutels,
    gouden_kaarten,
    getrokken_gouden_sleutels,
    font,
    font_klein,
):
    """Teken een overzicht van normale en gouden kaarten."""
    dim = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 160))
    scherm.blit(dim, (0, 0))

    pygame.draw.rect(scherm, PANEEL_KLEUR, overlay_rect, border_radius=24)
    pygame.draw.rect(scherm, PANEEL_RAND, overlay_rect, 4, border_radius=24)

    titel = font.render("Kaartoverzicht", True, TEKST_KLEUR)
    uitleg = font_klein.render("Links normaal, rechts goud. Licht = getrokken.", True, SUBTEKST_KLEUR)
    scherm.blit(titel, (overlay_rect.x + 20, overlay_rect.y + 16))
    scherm.blit(uitleg, (overlay_rect.x + 22, overlay_rect.y + 52))

    pygame.draw.rect(scherm, KNOP_KLEUR, sluit_rect, border_radius=10)
    pygame.draw.rect(scherm, KNOP_RAND, sluit_rect, 2, border_radius=10)
    sluit_tekst = font_klein.render("Sluiten", True, TEKST_KLEUR)
    scherm.blit(
        sluit_tekst,
        (sluit_rect.x + sluit_rect.width // 2 - sluit_tekst.get_width() // 2, sluit_rect.y + 6),
    )
    normaal_rect = pygame.Rect(overlay_rect.x + 16, overlay_rect.y + 88, 386, 330)
    goud_rect = pygame.Rect(overlay_rect.x + 418, overlay_rect.y + 88, 386, 330)
    teken_deck_grid(scherm, normaal_rect, "Normaal deck", kaarten, getrokken_sleutels, font, font_klein)
    teken_deck_grid(scherm, goud_rect, "Goud deck", gouden_kaarten, getrokken_gouden_sleutels, font, font_klein)


def reset_speltoestand():
    """Zet de spelwaarden terug voor een nieuwe ronde."""
    return START_PUNTEN * 10, START_KLIK_KRACHT, START_AUTO_SPOKEN, 0


def verwerk_auto_punten(punten, auto_spoken, multiplier, buffer_ms, delta_ms):
    """Verdeel automatische punten netjes over de hele seconde."""
    if auto_spoken <= 0 or delta_ms <= 0:
        return punten, buffer_ms

    buffer_ms += auto_spoken * multiplier * delta_ms
    extra_punten = buffer_ms // 1000
    buffer_ms %= 1000
    punten += extra_punten
    return punten, buffer_ms


def verwerk_luckcoins(luckcoins, buffer_ms, delta_ms):
    """Geef elke seconde netjes 0.1 luckcoin erbij."""
    if delta_ms <= 0:
        return luckcoins, buffer_ms

    buffer_ms += delta_ms
    extra_tienden = buffer_ms // 1000
    buffer_ms %= 1000
    luckcoins += extra_tienden
    return luckcoins, buffer_ms


def speel():
    """Start en draai het clicker-spel."""
    pygame.mixer.pre_init(MUZIEK_SAMPLE_RATE, -16, 2, 512)
    pygame.init()
    scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE))
    pygame.display.set_caption(SCHERM_TITEL)
    klok = pygame.time.Clock()

    # Lettertypes.
    font_groot = pygame.font.SysFont("Arial", 40, bold=True)
    font_middel = pygame.font.SysFont("Arial", 28, bold=True)
    font_klein = pygame.font.SysFont("Arial", 20)
    font_shop = pygame.font.SysFont("Arial", 15, bold=True)
    font_shop_klein = pygame.font.SysFont("Arial", 12)

    # Rechthoeken voor het poppetje en de winkel.
    poppetje_rect = pygame.Rect(120, 110, 220, 260)
    kaart_paneel_rect = pygame.Rect(360, 110, 220, 420)
    kaart_knop_rect = pygame.Rect(kaart_paneel_rect.x + 20, kaart_paneel_rect.y + 188, kaart_paneel_rect.width - 40, 58)
    kaart_overzicht_knop_rect = pygame.Rect(kaart_paneel_rect.x + 20, kaart_paneel_rect.y + 252, kaart_paneel_rect.width - 40, 30)
    luckshop_knop_rect = pygame.Rect(kaart_paneel_rect.x + 20, kaart_paneel_rect.y + 288, kaart_paneel_rect.width - 40, 46)
    kaart_overlay_rect = pygame.Rect(70, 36, 820, 468)
    sluit_kaart_overlay_rect = pygame.Rect(kaart_overlay_rect.right - 108, kaart_overlay_rect.y + 16, 88, 30)
    luckshop_overlay_rect = pygame.Rect(70, 36, 820, 468)
    sluit_luckshop_overlay_rect = pygame.Rect(luckshop_overlay_rect.right - 108, luckshop_overlay_rect.y + 16, 88, 30)
    luckshop_vorige_pagina_knop = pygame.Rect(luckshop_overlay_rect.right - 196, luckshop_overlay_rect.y + 16, 36, 30)
    luckshop_volgende_pagina_knop = pygame.Rect(luckshop_overlay_rect.right - 152, luckshop_overlay_rect.y + 16, 36, 30)
    echte_reset_knop = pygame.Rect(18, 18, 122, 34)
    werelden_knop = pygame.Rect(150, 18, 104, 34)
    werelden_overlay_rect = pygame.Rect(70, 36, 820, 468)
    sluit_werelden_overlay_rect = pygame.Rect(werelden_overlay_rect.right - 108, werelden_overlay_rect.y + 16, 88, 30)
    werelden_vorige_pagina_knop = pygame.Rect(werelden_overlay_rect.right - 196, werelden_overlay_rect.y + 16, 36, 30)
    werelden_volgende_pagina_knop = pygame.Rect(werelden_overlay_rect.right - 152, werelden_overlay_rect.y + 16, 36, 30)
    koop_wereld_knop = pygame.Rect(werelden_overlay_rect.x + 20, werelden_overlay_rect.bottom - 96, werelden_overlay_rect.width - 40, 82)
    echte_reset_overlay_rect = pygame.Rect(245, 150, 470, 210)
    echte_reset_ja_rect = pygame.Rect(echte_reset_overlay_rect.x + 42, echte_reset_overlay_rect.bottom - 70, 170, 46)
    echte_reset_nee_rect = pygame.Rect(echte_reset_overlay_rect.right - 212, echte_reset_overlay_rect.bottom - 70, 170, 46)
    paneel_rect = pygame.Rect(620, 30, 300, 480)
    shop_vakken = maak_shop_vakken(paneel_rect)
    vorige_pagina_knop = pygame.Rect(paneel_rect.x + 176, paneel_rect.y + 216, 32, 28)
    volgende_pagina_knop = pygame.Rect(paneel_rect.x + 252, paneel_rect.y + 216, 32, 28)
    reset_knop = pygame.Rect(45, 415, 250, 74)

    # Spelvariabelen.
    speltoestand = laad_speltoestand()
    werelden = speltoestand["werelden"]
    actieve_wereld = min(max(1, speltoestand["actieve_wereld"]), len(werelden))
    wereld_nummer = 1
    punten = START_PUNTEN * 10
    klik_kracht = START_KLIK_KRACHT
    auto_spoken = START_AUTO_SPOKEN
    shop_pagina = 0
    luckshop_pagina = 0
    multiplier = 10
    luckcoins = 0
    auto_punten_buffer = 0
    luckcoin_buffer = 0
    kaarten = []
    kaarten_stapel = []
    gouden_kaarten = []
    gouden_kaarten_stapel = []
    kaart_trekkingen = 0
    laatste_kaart = None
    laatste_kaart_resultaat = ""
    laatste_gouden_kaart = None
    laatste_gouden_kaart_resultaat = ""
    laatste_luckshop_resultaat = ""
    getrokken_kaart_sleutels = set()
    getrokken_gouden_kaart_sleutels = set()
    klik_animatie = 0
    teller = 0
    kaart_overzicht_open = False
    opslaan_timer = 0
    echte_reset_open = False
    luckshop_open = False
    werelden_open = False
    wereld_vakken = maak_wereld_vakken(werelden_overlay_rect)
    wereld_pagina = 0
    upgrades = []
    luckshop_upgrades = []
    vakken_per_pagina = len(shop_vakken)
    luckshop_vakken = maak_luckshop_vakken(luckshop_overlay_rect)
    muziek_geluid = None
    muziek_kanaal = None
    muziek_wereld = None

    def bewaar_actieve_wereld():
        """Bewaar de actieve wereld terug in de wereldenlijst."""
        werelden[actieve_wereld - 1] = {
            "wereld_nummer": wereld_nummer,
            "punten": punten,
            "klik_kracht": klik_kracht,
            "auto_spoken": auto_spoken,
            "shop_pagina": shop_pagina,
            "luckshop_pagina": luckshop_pagina,
            "multiplier": multiplier,
            "luckcoins": luckcoins,
            "auto_punten_buffer": auto_punten_buffer,
            "luckcoin_buffer": luckcoin_buffer,
            "kaarten": kaarten,
            "kaarten_stapel": kaarten_stapel,
            "gouden_kaarten": gouden_kaarten,
            "gouden_kaarten_stapel": gouden_kaarten_stapel,
            "kaart_trekkingen": kaart_trekkingen,
            "laatste_kaart": laatste_kaart,
            "laatste_kaart_resultaat": laatste_kaart_resultaat,
            "laatste_gouden_kaart": laatste_gouden_kaart,
            "laatste_gouden_kaart_resultaat": laatste_gouden_kaart_resultaat,
            "laatste_luckshop_resultaat": laatste_luckshop_resultaat,
            "getrokken_kaart_sleutels": getrokken_kaart_sleutels,
            "getrokken_gouden_kaart_sleutels": getrokken_gouden_kaart_sleutels,
        }

    def laad_actieve_wereld():
        """Laad de actieve wereld in de losse spelvariabelen."""
        nonlocal wereld_nummer, punten, klik_kracht, auto_spoken, shop_pagina, luckshop_pagina
        nonlocal multiplier, luckcoins, auto_punten_buffer, luckcoin_buffer, kaarten, kaarten_stapel
        nonlocal gouden_kaarten, gouden_kaarten_stapel, kaart_trekkingen, laatste_kaart
        nonlocal laatste_kaart_resultaat, laatste_gouden_kaart, laatste_gouden_kaart_resultaat
        nonlocal laatste_luckshop_resultaat, getrokken_kaart_sleutels, getrokken_gouden_kaart_sleutels
        nonlocal upgrades, luckshop_upgrades, klik_animatie

        (
            wereld_nummer,
            punten,
            klik_kracht,
            auto_spoken,
            shop_pagina,
            luckshop_pagina,
            multiplier,
            luckcoins,
            auto_punten_buffer,
            luckcoin_buffer,
            kaarten,
            kaarten_stapel,
            gouden_kaarten,
            gouden_kaarten_stapel,
            kaart_trekkingen,
            laatste_kaart,
            laatste_kaart_resultaat,
            laatste_gouden_kaart,
            laatste_gouden_kaart_resultaat,
            laatste_luckshop_resultaat,
            getrokken_kaart_sleutels,
            getrokken_gouden_kaart_sleutels,
        ) = pak_wereldvariabelen(werelden[actieve_wereld - 1])
        upgrades = maak_upgrades()
        luckshop_upgrades = maak_luckshop_upgrades()
        klik_animatie = 0

    def wissel_naar_wereld(nieuwe_wereld):
        """Ga naar een andere wereld."""
        nonlocal actieve_wereld, wereld_pagina, kaart_overzicht_open, luckshop_open, werelden_open
        bewaar_actieve_wereld()
        actieve_wereld = nieuwe_wereld
        wereld_pagina = (actieve_wereld - 1) // len(wereld_vakken)
        kaart_overzicht_open = False
        luckshop_open = False
        werelden_open = False
        laad_actieve_wereld()
        start_muziek()

    def sla_huidige_voortgang_op():
        """Bewaar alle werelden in het opslagbestand."""
        bewaar_actieve_wereld()
        sla_spel_op(actieve_wereld, werelden)

    def start_muziek():
        """Start of ververs de enge achtergrondmuziek."""
        nonlocal muziek_geluid, muziek_kanaal, muziek_wereld
        if pygame.mixer.get_init() is None:
            return
        if muziek_wereld == wereld_nummer and muziek_kanaal is not None and muziek_kanaal.get_busy():
            return

        if muziek_kanaal is not None:
            muziek_kanaal.stop()

        muziek_geluid = maak_enge_muziek(wereld_nummer)
        if muziek_geluid is None:
            return

        muziek_geluid.set_volume(MUZIEK_VOLUME)
        muziek_kanaal = muziek_geluid.play(loops=-1)
        muziek_wereld = wereld_nummer

    laad_actieve_wereld()
    wereld_pagina = (actieve_wereld - 1) // len(wereld_vakken)
    start_muziek()

    while True:
        delta_ms = klok.tick(FPS)
        teller += 1
        opslaan_timer += delta_ms

        punten_voor_auto = punten
        punten, auto_punten_buffer = verwerk_auto_punten(
            punten, auto_spoken, multiplier, auto_punten_buffer, delta_ms
        )
        luckcoins, luckcoin_buffer = verwerk_luckcoins(luckcoins, luckcoin_buffer, delta_ms)
        if punten > punten_voor_auto:
            shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)
        luckshop_pagina = kies_volgende_luckshop_pagina(luckcoins, luckshop_pagina, luckshop_upgrades, len(luckshop_vakken))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sla_huidige_voortgang_op()
                if muziek_kanaal is not None:
                    muziek_kanaal.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                if echte_reset_open:
                    if echte_reset_ja_rect.collidepoint(muis_pos):
                        wis_opslagbestand()
                        speltoestand = maak_nieuwe_speltoestand()
                        werelden = speltoestand["werelden"]
                        actieve_wereld = 1
                        teller = 0
                        opslaan_timer = 0
                        kaart_overzicht_open = False
                        echte_reset_open = False
                        luckshop_open = False
                        werelden_open = False
                        laad_actieve_wereld()
                        wereld_pagina = 0
                        start_muziek()
                        sla_huidige_voortgang_op()
                    elif echte_reset_nee_rect.collidepoint(muis_pos):
                        echte_reset_open = False
                    continue

                if werelden_open:
                    if sluit_werelden_overlay_rect.collidepoint(muis_pos) or werelden_knop.collidepoint(muis_pos):
                        werelden_open = False
                    elif werelden_vorige_pagina_knop.collidepoint(muis_pos) and wereld_pagina > 0:
                        wereld_pagina -= 1
                    elif werelden_volgende_pagina_knop.collidepoint(muis_pos):
                        max_pagina = max(0, (len(werelden) - 1) // len(wereld_vakken))
                        if wereld_pagina < max_pagina:
                            wereld_pagina += 1
                    elif koop_wereld_knop.collidepoint(muis_pos):
                        volgende_wereld = len(werelden) + 1
                        koop_kosten = bereken_wereld_kosten(volgende_wereld)
                        if punten >= koop_kosten * 10:
                            punten -= koop_kosten * 10
                            bewaar_actieve_wereld()
                            werelden.append(maak_nieuwe_wereldtoestand(volgende_wereld))
                            wissel_naar_wereld(volgende_wereld)
                    else:
                        start = wereld_pagina * len(wereld_vakken)
                        zichtbare_werelden = werelden[start : start + len(wereld_vakken)]
                        for wereldtoestand, rect in zip(zichtbare_werelden, wereld_vakken):
                            if rect.collidepoint(muis_pos) and wereldtoestand["wereld_nummer"] != actieve_wereld:
                                wissel_naar_wereld(wereldtoestand["wereld_nummer"])
                                break
                    continue

                if luckshop_open:
                    if sluit_luckshop_overlay_rect.collidepoint(muis_pos) or luckshop_knop_rect.collidepoint(muis_pos):
                        luckshop_open = False
                    elif luckshop_vorige_pagina_knop.collidepoint(muis_pos) and luckshop_pagina > 0:
                        luckshop_pagina -= 1
                    elif luckshop_volgende_pagina_knop.collidepoint(muis_pos):
                        luckshop_pagina += 1
                    else:
                        zichtbare_luckshop_upgrades = pak_luckshop_upgrades(luckshop_upgrades, luckshop_pagina, len(luckshop_vakken))
                        for upgrade, rect in zip(zichtbare_luckshop_upgrades, luckshop_vakken):
                            if rect.collidepoint(muis_pos):
                                punten, luckcoins, laatste_luckshop_resultaat = koop_luckshop_bonus(punten, luckcoins, upgrade)
                                if laatste_luckshop_resultaat.endswith("gekocht!"):
                                    shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)
                                    luckshop_pagina = kies_volgende_luckshop_pagina(luckcoins, luckshop_pagina, luckshop_upgrades, len(luckshop_vakken))
                                break
                    continue

                if kaart_overzicht_open:
                    if sluit_kaart_overlay_rect.collidepoint(muis_pos) or kaart_overzicht_knop_rect.collidepoint(muis_pos):
                        kaart_overzicht_open = False
                    continue

                if echte_reset_knop.collidepoint(muis_pos):
                    echte_reset_open = True
                    continue

                if werelden_knop.collidepoint(muis_pos):
                    werelden_open = True
                    wereld_pagina = (actieve_wereld - 1) // len(wereld_vakken)
                    continue

                # Klik op de smiley voor punten.
                if poppetje_rect.collidepoint(muis_pos):
                    punten += klik_kracht * multiplier
                    klik_animatie = 10
                    shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)

                # Reset het spel en maak de multiplier groter.
                elif reset_knop.collidepoint(muis_pos):
                    reset_bonus = bereken_reset_bonus(punten)
                    if reset_bonus <= 0:
                        continue

                    multiplier += reset_bonus
                    punten, klik_kracht, auto_spoken, shop_pagina = reset_speltoestand()
                    klik_animatie = 0
                    auto_punten_buffer = 0

                # Trek een kaart voor een grote bonus.
                elif kaart_knop_rect.collidepoint(muis_pos):
                    if not kaarten_stapel:
                        continue

                    kaart_beschikbaar = bereken_beschikbare_kaart_trekkingen(multiplier)
                    if kaart_trekkingen >= kaart_beschikbaar:
                        continue

                    laatste_kaart = trek_kaart(kaarten_stapel)
                    if laatste_kaart is None:
                        continue

                    getrokken_kaart_sleutels.add(maak_kaart_sleutel(laatste_kaart))
                    punten, klik_kracht, auto_spoken, multiplier, luckcoins, laatste_kaart_resultaat = pas_kaart_toe(
                        laatste_kaart,
                        punten,
                        klik_kracht,
                        auto_spoken,
                        multiplier,
                        luckcoins,
                        getrokken_kaart_sleutels,
                    )
                    kaart_trekkingen += 1

                    if not kaarten_stapel:
                        laatste_gouden_kaart = trek_kaart(gouden_kaarten_stapel)
                        if laatste_gouden_kaart is not None:
                            getrokken_gouden_kaart_sleutels.add(maak_kaart_sleutel(laatste_gouden_kaart))
                            punten, klik_kracht, auto_spoken, multiplier, luckcoins, laatste_gouden_kaart_resultaat = pas_kaart_toe(
                                laatste_gouden_kaart,
                                punten,
                                klik_kracht,
                                auto_spoken,
                                multiplier,
                                luckcoins,
                                getrokken_gouden_kaart_sleutels,
                            )
                        else:
                            laatste_gouden_kaart_resultaat = "Alle gouden kaarten zijn al op."

                        kaarten_stapel = schud_kaarten(kaarten)
                        getrokken_kaart_sleutels = set()

                    shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)

                # Open het kaartoverzicht.
                elif kaart_overzicht_knop_rect.collidepoint(muis_pos):
                    kaart_overzicht_open = True

                elif luckshop_knop_rect.collidepoint(muis_pos):
                    luckshop_open = True

                # Ga naar de vorige shop-pagina.
                elif vorige_pagina_knop.collidepoint(muis_pos) and shop_pagina > 0:
                    shop_pagina -= 1

                # Ga naar de volgende shop-pagina.
                elif volgende_pagina_knop.collidepoint(muis_pos):
                    shop_pagina += 1

                # Klik op een shop-ding.
                else:
                    zichtbare_upgrades = pak_shop_upgrades(upgrades, shop_pagina, vakken_per_pagina)

                    for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
                        if rect.collidepoint(muis_pos) and punten >= upgrade["kosten"] * 10:
                            punten -= upgrade["kosten"] * 10
                            klik_kracht += upgrade["klik_bonus"]
                            auto_spoken += upgrade["auto_bonus"]
                            shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)
                            break

        if klik_animatie > 0:
            klik_animatie -= 1

        if opslaan_timer >= AUTO_OPSLAAN_MS:
            sla_huidige_voortgang_op()
            opslaan_timer = 0

        teken_achtergrond(scherm, teller)
        wereld_thema = maak_wereld_thema(wereld_nummer)
        koop_kosten = bereken_wereld_kosten(len(werelden) + 1)
        start_muziek()

        # Titel en uitleg linksboven.
        titel = font_groot.render(maak_passende_tekst(font_groot, f"Eng Spel - Wereld {format_getal(wereld_nummer)}", 320), True, TEKST_KLEUR)
        uitleg = font_klein.render(maak_passende_tekst(font_klein, f"{wereld_thema['naam']} - klik op de enge smiley!", 320), True, SUBTEKST_KLEUR)
        teken_echte_reset_knop(scherm, echte_reset_knop, font_shop)
        teken_werelden_knop(scherm, werelden_knop, font_shop)
        scherm.blit(titel, (276, 18))
        scherm.blit(uitleg, (278, 64))

        # Teken de smiley.
        teken_poppetje(scherm, poppetje_rect, teller, klik_animatie, punten)
        teken_kaart_paneel(
            scherm,
            kaart_paneel_rect,
            kaart_knop_rect,
            kaart_overzicht_knop_rect,
            luckshop_knop_rect,
            multiplier,
            luckcoins,
            wereld_thema["luckcoins"],
            luckshop_pagina,
            laatste_kaart,
            laatste_kaart_resultaat,
            laatste_gouden_kaart,
            laatste_gouden_kaart_resultaat,
            laatste_luckshop_resultaat,
            kaart_trekkingen,
            kaarten_stapel,
            gouden_kaarten_stapel,
            getrokken_gouden_kaart_sleutels,
            font_klein,
            font_shop,
        )
        teken_reset_knop(scherm, reset_knop, punten, multiplier, font_klein, font_shop)

        # Teken het informatiepaneel.
        teken_paneel(scherm, paneel_rect)

        punten_tekst = font_groot.render(maak_passende_tekst(font_groot, f"{wereld_thema['punten']}: {format_tienden(punten)}", 260), True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {format_tienden(klik_kracht * multiplier)}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {format_tienden(auto_spoken * multiplier)}", True, ROZE)
        multiplier_tekst = font_klein.render(f"Multiplier: x{format_tienden(multiplier)}", True, GEEL)
        eng_kracht = bereken_eng_niveau(punten)
        wereld_tekst = font_klein.render(maak_passende_tekst(font_klein, f"Wereldnaam: {wereld_thema['naam']}", 250), True, SUBTEKST_KLEUR)
        eng_tekst = font_klein.render(f"Eng kracht: {format_getal(eng_kracht)}", True, SUBTEKST_KLEUR)
        scherm.blit(punten_tekst, (paneel_rect.x + 20, 48))
        scherm.blit(klik_tekst, (paneel_rect.x + 20, 104))
        scherm.blit(auto_tekst, (paneel_rect.x + 20, 140))
        scherm.blit(multiplier_tekst, (paneel_rect.x + 20, 178))
        scherm.blit(wereld_tekst, (paneel_rect.x + 20, 202))
        scherm.blit(eng_tekst, (paneel_rect.x + 20, 222))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        pagina_tekst = font_klein.render(f"Pagina {shop_pagina + 1}", True, SUBTEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel_rect.x + 20, 244))
        scherm.blit(pagina_tekst, (paneel_rect.x + 210, 250))

        teken_pagina_knop(scherm, vorige_pagina_knop, "<", shop_pagina > 0, font_klein)
        teken_pagina_knop(scherm, volgende_pagina_knop, ">", True, font_klein)

        # Teken alleen de shop-dingen van deze pagina.
        zichtbare_upgrades = pak_shop_upgrades(upgrades, shop_pagina, vakken_per_pagina)
        for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
            teken_shop_knop(scherm, rect, upgrade, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: koop nieuwe werelden voor nieuwe kaarten!", True, SUBTEKST_KLEUR)
        scherm.blit(tip, (38, 505))

        if kaart_overzicht_open:
            teken_kaart_overzicht(
                scherm,
                kaart_overlay_rect,
                sluit_kaart_overlay_rect,
                kaarten,
                getrokken_kaart_sleutels,
                gouden_kaarten,
                getrokken_gouden_kaart_sleutels,
                font_klein,
                font_shop,
            )

        if luckshop_open:
            teken_luckshop_overzicht(
                scherm,
                luckshop_overlay_rect,
                sluit_luckshop_overlay_rect,
                luckshop_vorige_pagina_knop,
                luckshop_volgende_pagina_knop,
                luckshop_upgrades,
                luckshop_pagina,
                luckshop_vakken,
                luckcoins,
                wereld_thema["luckcoins"],
                laatste_luckshop_resultaat,
                font_klein,
                font_shop,
            )

        if werelden_open:
            teken_werelden_overzicht(
                scherm,
                werelden_overlay_rect,
                sluit_werelden_overlay_rect,
                werelden_vorige_pagina_knop,
                werelden_volgende_pagina_knop,
                koop_wereld_knop,
                wereld_vakken,
                werelden,
                actieve_wereld,
                wereld_pagina,
                koop_kosten,
                punten,
                font_klein,
                font_shop,
            )

        if echte_reset_open:
            teken_echte_reset_waarschuwing(
                scherm,
                echte_reset_overlay_rect,
                echte_reset_ja_rect,
                echte_reset_nee_rect,
                font_middel,
                font_klein,
            )

        pygame.display.flip()


if __name__ == "__main__":
    speel()
