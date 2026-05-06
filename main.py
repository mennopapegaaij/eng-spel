"""Eng Spel - een simpel clicker-spel met een enge smiley."""

import json
import math
import random
import sys
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
OPSLAAN_VERSIE = 1
AUTO_OPSLAAN_MS = 5000


def maak_kaarten(goud=False):
    """Maak een deck met 48 nummerkaarten: 1 t/m 12, vier keer."""
    if goud:
        kaart_kleuren = [
            ("Goudmaan", (188, 146, 44)),
            ("Goudmist", (205, 160, 52)),
            ("Goudspook", (222, 176, 58)),
            ("Goudnacht", (238, 194, 70)),
        ]
    else:
        kaart_kleuren = [
            ("Maan", (78, 42, 98)),
            ("Mist", (118, 34, 72)),
            ("Spook", (92, 28, 122)),
            ("Nacht", (60, 80, 130)),
        ]
    kaarten = []

    for reeks, kleur in kaart_kleuren:
        for nummer in range(1, 13):
            kaarten.append(
                {
                    "titel": f"{'Gouden ' if goud else ''}kaart {nummer}",
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


def maak_nieuwe_speltoestand():
    """Maak een nieuwe, lege speltoestand."""
    kaarten = maak_kaarten()
    gouden_kaarten = maak_kaarten(goud=True)
    return {
        "punten": START_PUNTEN * 10,
        "klik_kracht": START_KLIK_KRACHT,
        "auto_spoken": START_AUTO_SPOKEN,
        "shop_pagina": 0,
        "multiplier": 10,
        "luckcoins": 0,
        "klik_animatie": 0,
        "teller": 0,
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
        "getrokken_kaart_sleutels": set(),
        "getrokken_gouden_kaart_sleutels": set(),
        "kaart_overzicht_open": False,
        "opslaan_timer": 0,
    }


def laad_speltoestand():
    """Laad de voortgang uit het opslagbestand."""
    speltoestand = maak_nieuwe_speltoestand()
    if not OPSLAAN_BESTAND.exists():
        return speltoestand

    kaart_lookup = maak_kaart_lookup(speltoestand["kaarten"], speltoestand["gouden_kaarten"])

    try:
        with OPSLAAN_BESTAND.open("r", encoding="utf-8") as bestand:
            data = json.load(bestand)

        if int(data.get("versie", 0)) != OPSLAAN_VERSIE:
            print("De oude opslag past niet meer. Het spel start opnieuw.")
            return speltoestand

        speltoestand["punten"] = int(data.get("punten", speltoestand["punten"]))
        speltoestand["klik_kracht"] = int(data.get("klik_kracht", speltoestand["klik_kracht"]))
        speltoestand["auto_spoken"] = int(data.get("auto_spoken", speltoestand["auto_spoken"]))
        speltoestand["shop_pagina"] = max(0, int(data.get("shop_pagina", speltoestand["shop_pagina"])))
        speltoestand["multiplier"] = max(1, int(data.get("multiplier", speltoestand["multiplier"])))
        speltoestand["luckcoins"] = max(0, int(data.get("luckcoins", speltoestand["luckcoins"])))
        speltoestand["auto_punten_buffer"] = max(0, int(data.get("auto_punten_buffer", 0)))
        speltoestand["luckcoin_buffer"] = max(0, int(data.get("luckcoin_buffer", 0)))
        speltoestand["kaart_trekkingen"] = max(0, int(data.get("kaart_trekkingen", 0)))
        speltoestand["laatste_kaart_resultaat"] = str(data.get("laatste_kaart_resultaat", ""))
        speltoestand["laatste_gouden_kaart_resultaat"] = str(data.get("laatste_gouden_kaart_resultaat", ""))

        if "kaarten_stapel" in data:
            speltoestand["kaarten_stapel"] = [kaart_van_bewaar_data(kaart, kaart_lookup) for kaart in data["kaarten_stapel"]]
        if "gouden_kaarten_stapel" in data:
            speltoestand["gouden_kaarten_stapel"] = [kaart_van_bewaar_data(kaart, kaart_lookup) for kaart in data["gouden_kaarten_stapel"]]
        if "laatste_kaart" in data:
            speltoestand["laatste_kaart"] = kaart_van_bewaar_data(data["laatste_kaart"], kaart_lookup)
        if "laatste_gouden_kaart" in data:
            speltoestand["laatste_gouden_kaart"] = kaart_van_bewaar_data(data["laatste_gouden_kaart"], kaart_lookup)
        if "getrokken_kaart_sleutels" in data:
            speltoestand["getrokken_kaart_sleutels"] = sleutels_van_bewaar_data(data["getrokken_kaart_sleutels"])
        if "getrokken_gouden_kaart_sleutels" in data:
            speltoestand["getrokken_gouden_kaart_sleutels"] = sleutels_van_bewaar_data(data["getrokken_gouden_kaart_sleutels"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as fout:
        print(f"Opslag laden mislukte: {fout}")
        return maak_nieuwe_speltoestand()

    return speltoestand


def sla_spel_op(
    punten,
    klik_kracht,
    auto_spoken,
    shop_pagina,
    multiplier,
    luckcoins,
    auto_punten_buffer,
    luckcoin_buffer,
    kaart_trekkingen,
    laatste_kaart,
    laatste_kaart_resultaat,
    laatste_gouden_kaart,
    laatste_gouden_kaart_resultaat,
    getrokken_kaart_sleutels,
    getrokken_gouden_kaart_sleutels,
    kaarten_stapel,
    gouden_kaarten_stapel,
):
    """Sla de voortgang veilig op in een JSON-bestand."""
    opslag_data = {
        "versie": OPSLAAN_VERSIE,
        "punten": int(punten),
        "klik_kracht": int(klik_kracht),
        "auto_spoken": int(auto_spoken),
        "shop_pagina": int(shop_pagina),
        "multiplier": int(multiplier),
        "luckcoins": int(luckcoins),
        "auto_punten_buffer": int(auto_punten_buffer),
        "luckcoin_buffer": int(luckcoin_buffer),
        "kaart_trekkingen": int(kaart_trekkingen),
        "laatste_kaart": kaart_naar_bewaar_data(laatste_kaart),
        "laatste_kaart_resultaat": laatste_kaart_resultaat,
        "laatste_gouden_kaart": kaart_naar_bewaar_data(laatste_gouden_kaart),
        "laatste_gouden_kaart_resultaat": laatste_gouden_kaart_resultaat,
        "getrokken_kaart_sleutels": sleutels_naar_bewaar_data(getrokken_kaart_sleutels),
        "getrokken_gouden_kaart_sleutels": sleutels_naar_bewaar_data(getrokken_gouden_kaart_sleutels),
        "kaarten_stapel": [kaart_naar_bewaar_data(kaart) for kaart in kaarten_stapel],
        "gouden_kaarten_stapel": [kaart_naar_bewaar_data(kaart) for kaart in gouden_kaarten_stapel],
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


def pak_spelvariabelen(speltoestand):
    """Haal alle spelwaarden uit 1 speltoestand."""
    return (
        speltoestand["punten"],
        speltoestand["klik_kracht"],
        speltoestand["auto_spoken"],
        speltoestand["shop_pagina"],
        speltoestand["multiplier"],
        speltoestand["luckcoins"],
        speltoestand["klik_animatie"],
        speltoestand["teller"],
        speltoestand["auto_punten_buffer"],
        speltoestand["luckcoin_buffer"],
        speltoestand["kaarten"],
        speltoestand["kaarten_stapel"],
        speltoestand["gouden_kaarten"],
        speltoestand["gouden_kaarten_stapel"],
        speltoestand["kaart_trekkingen"],
        speltoestand["laatste_kaart"],
        speltoestand["laatste_kaart_resultaat"],
        speltoestand["laatste_gouden_kaart"],
        speltoestand["laatste_gouden_kaart_resultaat"],
        speltoestand["getrokken_kaart_sleutels"],
        speltoestand["getrokken_gouden_kaart_sleutels"],
        speltoestand["kaart_overzicht_open"],
        speltoestand["opslaan_timer"],
    )


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


def format_getal(getal):
    """Maak grote getallen kort, zodat ze op het scherm passen."""
    suffixen = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]

    if isinstance(getal, int):
        negatief = getal < 0
        waarde = abs(getal)

        if waarde < 1000:
            tekst = str(waarde)
            return f"-{tekst}" if negatief else tekst

        if waarde < 10**15:
            tekst_getal = str(waarde)
            groep = (len(tekst_getal) - 1) // 3
            if groep < len(suffixen):
                eerste_stuk = len(tekst_getal) - groep * 3
                hoofd = tekst_getal[:eerste_stuk]
                decimaal = tekst_getal[eerste_stuk : eerste_stuk + 1]
                tekst = f"{hoofd}.{decimaal}{suffixen[groep]}" if decimaal and decimaal != "0" else f"{hoofd}{suffixen[groep]}"
                return f"-{tekst}" if negatief else tekst

            macht = len(tekst_getal) - 1
            tekst = f"{tekst_getal[0]}.{tekst_getal[1:3]}e{macht}"
            return f"-{tekst}" if negatief else tekst

        cijfers, begin = schat_grote_int(waarde, 3)
        groep = (cijfers - 1) // 3
        if groep < len(suffixen):
            eerste_stuk = cijfers - groep * 3
            hoofd = begin[:eerste_stuk]
            decimaal = begin[eerste_stuk : eerste_stuk + 1]
            tekst = f"{hoofd}.{decimaal}{suffixen[groep]}" if decimaal and decimaal != "0" else f"{hoofd}{suffixen[groep]}"
            return f"-{tekst}" if negatief else tekst

        tekst = f"{begin[0]}.{begin[1:3]}e{cijfers - 1}"
        return f"-{tekst}" if negatief else tekst

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

    groep = min(int(math.log10(waarde) // 3), len(suffixen) - 1)
    klein = waarde / (1000 ** groep)
    tekst = f"{klein:.1f}{suffixen[groep]}"
    if tekst.endswith(".0" + suffixen[groep]):
        tekst = f"{int(klein)}{suffixen[groep]}"
    return f"-{tekst}" if negatief else tekst


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


def teken_paneel(scherm, paneel_rect):
    """Teken het rechter paneel voor punten en upgrades."""
    pygame.draw.rect(scherm, PANEEL_KLEUR, paneel_rect, border_radius=20)
    pygame.draw.rect(scherm, PANEEL_RAND, paneel_rect, 4, border_radius=20)


def maak_shop_vakken(paneel_rect):
    """Maak 8 vakken voor de shop (2 kolommen van 4)."""
    vakken = []
    start_x = paneel_rect.x + 16
    start_y = paneel_rect.y + 236
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


def bereken_beschikbare_kaart_trekkingen(multiplier):
    """Geef hoeveel gratis kaarttrekkingen je hebt vrijgespeeld."""
    hele_multiplier = max(1, int(multiplier) // 10)
    if hele_multiplier < 10:
        return 0
    return int(bereken_log10_groot_getal(hele_multiplier))


def format_kaart_mijlpaal(stap):
    """Maak de volgende multiplier-mijlpaal netjes leesbaar."""
    if stap <= 3:
        return f"x{10 ** stap}"
    return f"x1e{stap}"


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


def teken_kaart_paneel(
    scherm,
    paneel_rect,
    knop_rect,
    overzicht_knop_rect,
    multiplier,
    luckcoins,
    laatste_kaart,
    laatste_kaart_resultaat,
    laatste_gouden_kaart,
    laatste_gouden_kaart_resultaat,
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

    luckcoins_tekst = font_klein.render(maak_passende_tekst(font_klein, f"Luckcoins: {format_tienden(luckcoins)}", paneel_breedte), True, GEEL)
    scherm.blit(luckcoins_tekst, (paneel_rect.x + 18, paneel_rect.y + 284))

    if laatste_gouden_kaart:
        goud_resultaat_regel = f"Goud: {laatste_gouden_kaart['titel']}"
        goud_uitleg_regel = laatste_gouden_kaart_resultaat
    else:
        goud_resultaat_regel = "Gouden kaart: nog geen"
        goud_uitleg_regel = "Voltooi een normaal deck voor 1 gouden kaart."
    goud_resultaat = font_klein.render(maak_passende_tekst(font_klein, goud_resultaat_regel, paneel_breedte), True, KNOP_RAND)
    goud_uitleg = font_klein.render(maak_passende_tekst(font_klein, goud_uitleg_regel, paneel_breedte), True, TEKST_KLEUR if laatste_gouden_kaart else SUBTEKST_KLEUR)
    scherm.blit(goud_resultaat, (paneel_rect.x + 18, paneel_rect.y + 304))
    scherm.blit(goud_uitleg, (paneel_rect.x + 18, paneel_rect.y + 322))


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
    kaart_paneel_rect = pygame.Rect(360, 110, 220, 342)
    kaart_knop_rect = pygame.Rect(kaart_paneel_rect.x + 20, kaart_paneel_rect.y + 188, kaart_paneel_rect.width - 40, 58)
    kaart_overzicht_knop_rect = pygame.Rect(kaart_paneel_rect.x + 20, kaart_paneel_rect.y + 252, kaart_paneel_rect.width - 40, 30)
    kaart_overlay_rect = pygame.Rect(70, 36, 820, 468)
    sluit_kaart_overlay_rect = pygame.Rect(kaart_overlay_rect.right - 108, kaart_overlay_rect.y + 16, 88, 30)
    echte_reset_knop = pygame.Rect(18, 18, 122, 34)
    echte_reset_overlay_rect = pygame.Rect(245, 150, 470, 210)
    echte_reset_ja_rect = pygame.Rect(echte_reset_overlay_rect.x + 42, echte_reset_overlay_rect.bottom - 70, 170, 46)
    echte_reset_nee_rect = pygame.Rect(echte_reset_overlay_rect.right - 212, echte_reset_overlay_rect.bottom - 70, 170, 46)
    paneel_rect = pygame.Rect(620, 30, 300, 480)
    shop_vakken = maak_shop_vakken(paneel_rect)
    vorige_pagina_knop = pygame.Rect(paneel_rect.x + 176, paneel_rect.y + 198, 32, 28)
    volgende_pagina_knop = pygame.Rect(paneel_rect.x + 252, paneel_rect.y + 198, 32, 28)
    reset_knop = pygame.Rect(45, 415, 250, 74)

    # Spelvariabelen.
    speltoestand = laad_speltoestand()
    (
        punten,
        klik_kracht,
        auto_spoken,
        shop_pagina,
        multiplier,
        luckcoins,
        klik_animatie,
        teller,
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
        getrokken_kaart_sleutels,
        getrokken_gouden_kaart_sleutels,
        kaart_overzicht_open,
        opslaan_timer,
    ) = pak_spelvariabelen(speltoestand)
    echte_reset_open = False
    upgrades = maak_upgrades()
    vakken_per_pagina = len(shop_vakken)

    def sla_huidige_voortgang_op():
        """Bewaar de huidige voortgang van het spel."""
        sla_spel_op(
            punten,
            klik_kracht,
            auto_spoken,
            shop_pagina,
            multiplier,
            luckcoins,
            auto_punten_buffer,
            luckcoin_buffer,
            kaart_trekkingen,
            laatste_kaart,
            laatste_kaart_resultaat,
            laatste_gouden_kaart,
            laatste_gouden_kaart_resultaat,
            getrokken_kaart_sleutels,
            getrokken_gouden_kaart_sleutels,
            kaarten_stapel,
            gouden_kaarten_stapel,
        )

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sla_huidige_voortgang_op()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                if echte_reset_open:
                    if echte_reset_ja_rect.collidepoint(muis_pos):
                        wis_opslagbestand()
                        speltoestand = maak_nieuwe_speltoestand()
                        (
                            punten,
                            klik_kracht,
                            auto_spoken,
                            shop_pagina,
                            multiplier,
                            luckcoins,
                            klik_animatie,
                            teller,
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
                            getrokken_kaart_sleutels,
                            getrokken_gouden_kaart_sleutels,
                            kaart_overzicht_open,
                            opslaan_timer,
                        ) = pak_spelvariabelen(speltoestand)
                        upgrades = maak_upgrades()
                        echte_reset_open = False
                        sla_huidige_voortgang_op()
                    elif echte_reset_nee_rect.collidepoint(muis_pos):
                        echte_reset_open = False
                    continue

                if kaart_overzicht_open:
                    if sluit_kaart_overlay_rect.collidepoint(muis_pos) or kaart_overzicht_knop_rect.collidepoint(muis_pos):
                        kaart_overzicht_open = False
                    continue

                if echte_reset_knop.collidepoint(muis_pos):
                    echte_reset_open = True
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

        # Titel en uitleg linksboven.
        titel = font_groot.render("Eng Spel", True, TEKST_KLEUR)
        uitleg = font_klein.render("Klik op de enge smiley en verzamel punten!", True, SUBTEKST_KLEUR)
        teken_echte_reset_knop(scherm, echte_reset_knop, font_shop)
        scherm.blit(titel, (160, 20))
        scherm.blit(uitleg, (162, 68))

        # Teken de smiley.
        teken_poppetje(scherm, poppetje_rect, teller, klik_animatie, punten)
        teken_kaart_paneel(
            scherm,
            kaart_paneel_rect,
            kaart_knop_rect,
            kaart_overzicht_knop_rect,
            multiplier,
            luckcoins,
            laatste_kaart,
            laatste_kaart_resultaat,
            laatste_gouden_kaart,
            laatste_gouden_kaart_resultaat,
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

        punten_tekst = font_groot.render(f"Punten: {format_tienden(punten)}", True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {format_tienden(klik_kracht * multiplier)}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {format_tienden(auto_spoken * multiplier)}", True, ROZE)
        multiplier_tekst = font_klein.render(f"Multiplier: x{format_tienden(multiplier)}", True, GEEL)
        eng_kracht = bereken_eng_niveau(punten)
        eng_tekst = font_klein.render(f"Eng kracht: {format_getal(eng_kracht)}", True, SUBTEKST_KLEUR)
        scherm.blit(punten_tekst, (paneel_rect.x + 20, 48))
        scherm.blit(klik_tekst, (paneel_rect.x + 20, 104))
        scherm.blit(auto_tekst, (paneel_rect.x + 20, 140))
        scherm.blit(multiplier_tekst, (paneel_rect.x + 20, 178))
        scherm.blit(eng_tekst, (paneel_rect.x + 20, 202))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        pagina_tekst = font_klein.render(f"Pagina {shop_pagina + 1}", True, SUBTEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel_rect.x + 20, 226))
        scherm.blit(pagina_tekst, (paneel_rect.x + 210, 232))

        teken_pagina_knop(scherm, vorige_pagina_knop, "<", shop_pagina > 0, font_klein)
        teken_pagina_knop(scherm, volgende_pagina_knop, ">", True, font_klein)

        # Teken alleen de shop-dingen van deze pagina.
        zichtbare_upgrades = pak_shop_upgrades(upgrades, shop_pagina, vakken_per_pagina)
        for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
            teken_shop_knop(scherm, rect, upgrade, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: trek kaarten voor zotte multiplier-bonussen!", True, SUBTEKST_KLEUR)
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
