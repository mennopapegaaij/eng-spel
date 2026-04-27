"""Eng Spel - een simpel clicker-spel met een eng poppetje."""

import math
import sys

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

    tekst_getal = str(getal)
    begin = tekst_getal[:16]
    mantisse = float(f"{begin[0]}.{begin[1:]}")
    return (len(tekst_getal) - 1) + math.log10(mantisse)


def format_getal(getal):
    """Maak grote getallen kort, zodat ze op het scherm passen."""
    suffixen = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]

    if isinstance(getal, int):
        negatief = getal < 0
        tekst_getal = str(abs(getal))

        if len(tekst_getal) <= 3:
            return f"-{tekst_getal}" if negatief else tekst_getal

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


def bereken_reset_bonus(punten):
    """Geef de resetbonus terug.

    Elke 50 punten geeft +0.1 multiplier.
    Dus:
    - 0 t/m 49 punten = +0.0x
    - 50 t/m 99 punten = +0.1x
    - 100 t/m 149 punten = +0.2x
    """
    return (max(0, int(punten)) // 10) // 50


def teken_poppetje(scherm, rect, teller, klik_animatie, punten):
    """Teken het enge poppetje waar je op moet klikken."""
    x = rect.x
    y = rect.y
    breedte = rect.width
    eng_kracht = bereken_eng_niveau(punten)
    eng_fase = int(eng_kracht)
    basis_niveau = min(eng_kracht, 6)
    extra_niveau = max(0.0, eng_kracht - 6)
    extra_tellen = max(0, int(extra_niveau))

    # Bij een klik wordt het poppetje heel even groter.
    extra = 10 if klik_animatie > 0 else 0
    enge_golf = math.sin(teller * (0.05 + eng_kracht * 0.003)) * min(eng_kracht, 18)
    lijf = pygame.Rect(
        x + 55 - extra // 2,
        int(y + 78 - extra // 2 - min(extra_niveau * 2, 22)),
        110 + extra,
        int(150 + extra + min(extra_niveau * 6, 72)),
    )
    hoofd_midden = (x + breedte // 2, y + 75 + int(enge_golf * 0.4))
    hoofd_straal = int(52 + extra // 3 + min(extra_niveau * 1.5, 20))
    huid_kleur = (
        int(max(0, PANEEL_KLEUR[0] - basis_niveau * 3 - extra_niveau * 2)),
        int(max(0, PANEEL_KLEUR[1] - basis_niveau * 2 - extra_niveau)),
        int(max(0, PANEEL_KLEUR[2] - basis_niveau * 5 - extra_niveau * 4)),
    )
    rand_kleur = (
        int(min(255, PANEEL_RAND[0] + basis_niveau * 12 + extra_niveau * 6)),
        int(max(0, PANEEL_RAND[1] - basis_niveau * 4 - extra_niveau * 2)),
        int(min(255, PANEEL_RAND[2] + basis_niveau * 8 + extra_niveau * 4)),
    )

    # Schaduw.
    pygame.draw.ellipse(scherm, ZWART, (x + 35, y + 220, 160, 35))

    # Hoe enger het niveau, hoe sterker de aura rond het hoofd.
    if eng_kracht >= 2:
        aantal_ringen = 1 + int(math.sqrt(extra_tellen + 1))
        for ring in range(aantal_ringen):
            aura_straal = int(hoofd_straal + 8 + basis_niveau * 3 + ring * (10 + min(extra_niveau, 12)))
            aura_kleur = (
                int(min(255, 70 + extra_niveau * 10 + ring * 18)),
                20,
                int(min(255, 80 + extra_niveau * 12 + ring * 24)),
            )
            pygame.draw.circle(scherm, aura_kleur, hoofd_midden, aura_straal, 3 if ring == 0 else 2)

    # Hoofd en lijf.
    pygame.draw.circle(scherm, huid_kleur, hoofd_midden, hoofd_straal)
    pygame.draw.circle(scherm, rand_kleur, hoofd_midden, hoofd_straal, 4)
    pygame.draw.rect(scherm, huid_kleur, lijf, border_radius=18)
    pygame.draw.rect(scherm, rand_kleur, lijf, 4, border_radius=18)

    # Armen.
    arm_golf = math.sin(teller * 0.08) * (12 + basis_niveau * 2 + extra_niveau * 3)
    pygame.draw.line(scherm, rand_kleur, (x + 60, y + 130), (x + 10, y + 155 + arm_golf), 8)
    pygame.draw.line(scherm, rand_kleur, (x + 160, y + 130), (x + 210, y + 155 - arm_golf), 8)

    # Hoorns bij hogere niveaus.
    if basis_niveau >= 4:
        hoorn_hoogte = int(28 + extra_niveau * 6)
        hoorn_buiten = int(18 + extra_niveau * 2)
        pygame.draw.polygon(
            scherm,
            rand_kleur,
            [(x + 78, y + 10), (x + 96 - hoorn_buiten, y - hoorn_hoogte), (x + 110, y + 18)],
        )
        pygame.draw.polygon(
            scherm,
            rand_kleur,
            [(x + 130, y + 18), (x + 144 + hoorn_buiten, y - hoorn_hoogte), (x + 162, y + 10)],
        )

    # Ogen - rood als het echt eng is.
    oog_kleur = ROZE if klik_animatie > 0 else ROOD
    oog_straal = int(10 + min(basis_niveau, 3) + min(extra_niveau, 8))
    pygame.draw.circle(scherm, oog_kleur, (x + 88, y + 65), oog_straal)
    pygame.draw.circle(scherm, oog_kleur, (x + 132, y + 65), oog_straal)
    pygame.draw.circle(scherm, WIT, (x + 91, y + 62), 3)
    pygame.draw.circle(scherm, WIT, (x + 135, y + 62), 3)

    if basis_niveau >= 2:
        pygame.draw.line(scherm, ZWART, (x + 74, y + 48), (x + 97, y + 58), 3)
        pygame.draw.line(scherm, ZWART, (x + 123, y + 58), (x + 146, y + 48), 3)

    if eng_kracht >= 5:
        pygame.draw.circle(scherm, oog_kleur, (x + 110, y + 34), int(8 + min(extra_niveau, 6)))
        pygame.draw.circle(scherm, WIT, (x + 112, y + 31), 2)

    if eng_kracht >= 8:
        pygame.draw.circle(scherm, oog_kleur, (x + 68, y + 104), int(5 + min(extra_niveau, 5)))
        pygame.draw.circle(scherm, oog_kleur, (x + 152, y + 104), int(5 + min(extra_niveau, 5)))

    if extra_tellen > 0:
        zwevende_ogen = 2 + int(math.sqrt(extra_tellen) * 3)
        for i in range(zwevende_ogen):
            hoek = teller * 0.02 + i * (math.tau / zwevende_ogen)
            oog_afstand = hoofd_straal + 42 + (i % 4) * 12 + extra_niveau * 1.7
            klein_oog_x = hoofd_midden[0] + int(math.cos(hoek) * oog_afstand)
            klein_oog_y = hoofd_midden[1] + int(math.sin(hoek) * oog_afstand * 0.55)
            klein_oog_straal = 3 + min(extra_tellen // 3, 6)
            pygame.draw.circle(scherm, ZWART, (klein_oog_x, klein_oog_y), klein_oog_straal + 2)
            pygame.draw.circle(scherm, oog_kleur, (klein_oog_x, klein_oog_y), klein_oog_straal)
            pygame.draw.circle(scherm, WIT, (klein_oog_x + 1, klein_oog_y - 1), 1)

    # Mond.
    if basis_niveau <= 1 and extra_niveau == 0:
        pygame.draw.arc(scherm, WIT, (x + 78, y + 88, 64, 28), 0, math.pi, 3)
    else:
        mond_breedte = 76 + min(extra_niveau * 6, 42)
        mond_hoogte = 34 + min(extra_niveau * 2, 18)
        mond_x = x + breedte // 2 - mond_breedte // 2
        pygame.draw.arc(scherm, WIT, (mond_x, y + 92, mond_breedte, mond_hoogte), 0, math.pi, 3)
        tanden = int(3 + min(basis_niveau, 4) + min(extra_niveau, 4))
        tand_afstand = mond_breedte / (tanden + 1)
        for tand in range(tanden):
            tand_midden = int(mond_x + tand_afstand * (tand + 1))
            tand_hoogte = 15 + min(extra_niveau * 2, 14)
            pygame.draw.polygon(
                scherm,
                WIT,
                [(tand_midden - 6, y + 103), (tand_midden, y + 103 + tand_hoogte), (tand_midden + 6, y + 103)],
            )

    if eng_kracht >= 6:
        vonken = 6 + extra_tellen * 3
        for i in range(vonken):
            hoek = teller * 0.03 + i * (math.tau / max(vonken, 1))
            afstand = hoofd_straal + 32 + (i % 3) * 10 + min(extra_niveau * 5, 70)
            vonk_x = hoofd_midden[0] + int(math.cos(hoek) * afstand)
            vonk_y = hoofd_midden[1] + int(math.sin(hoek) * afstand * 0.7)
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x - 8, vonk_y - 14), 2)
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x + 8, vonk_y - 12), 2)

    if extra_tellen > 0:
        for i in range(extra_tellen * 2):
            kras_x = x + 72 + (i * 17) % 76
            kras_y = y + 94 + (i * 23) % 112
            kras_lengte = 10 + (i % 3) * 4
            pygame.draw.line(scherm, ROOD, (kras_x, kras_y), (kras_x + kras_lengte, kras_y + 6), 2)
            pygame.draw.line(scherm, ZWART, (kras_x + 4, kras_y - 2), (kras_x - 2, kras_y + 8), 2)

    # Kleine waarschuwingstekst op het poppetje.
    font = pygame.font.SysFont("Arial", 20, bold=True)
    font_klein = pygame.font.SysFont("Arial", 16, bold=True)
    tekst = font.render("KLIK!", True, GEEL)
    scherm.blit(tekst, (x + breedte // 2 - tekst.get_width() // 2, y + 245))
    niveau_tekst = font_klein.render(f"Eng fase {eng_fase}", True, ROZE)
    scherm.blit(niveau_tekst, (x + breedte // 2 - niveau_tekst.get_width() // 2, y + 268))


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
        bonus = int(vorige_bonus * 1.12 + 5000 + nummer * 15)
        kosten = int(vorige_kosten * 1.13 + bonus * 14)
        uitleg = f"+{format_getal(bonus)} klik"
        return {"titel": titel, "uitleg": uitleg, "kosten": kosten, "klik_bonus": bonus, "auto_bonus": 0}

    vorige_bonus = upgrades[-2]["auto_bonus"]
    bonus = int(vorige_bonus * 1.12 + 3500 + nummer * 12)
    kosten = int(vorige_kosten * 1.13 + bonus * 16)
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
    start_y = paneel_rect.y + 245
    breedte = 129
    hoogte = 55
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

    titel_tekst = font_titel.render(upgrade["titel"], True, TEKST_KLEUR)
    uitleg_tekst = font_klein.render(upgrade["uitleg"], True, SUBTEKST_KLEUR)
    kosten_tekst = font_klein.render(f"{format_getal(upgrade['kosten'])} p", True, GEEL)

    scherm.blit(titel_tekst, (rect.x + 8, rect.y + 6))
    scherm.blit(uitleg_tekst, (rect.x + 8, rect.y + 24))
    scherm.blit(kosten_tekst, (rect.x + 8, rect.y + 39))


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
        uitleg = font_klein.render("Spaar 50 punten voor +0.1x", True, SUBTEKST_KLEUR)

    scherm.blit(
        uitleg,
        (rect.x + rect.width // 2 - uitleg.get_width() // 2, rect.y + 42),
    )


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
    paneel_rect = pygame.Rect(620, 30, 300, 480)
    shop_vakken = maak_shop_vakken(paneel_rect)
    vorige_pagina_knop = pygame.Rect(paneel_rect.x + 176, paneel_rect.y + 176, 32, 28)
    volgende_pagina_knop = pygame.Rect(paneel_rect.x + 252, paneel_rect.y + 176, 32, 28)
    reset_knop = pygame.Rect(45, 415, 250, 74)

    # Spelvariabelen.
    punten, klik_kracht, auto_spoken, shop_pagina = reset_speltoestand()
    multiplier = 10
    klik_animatie = 0
    teller = 0
    auto_punten_buffer = 0
    upgrades = maak_upgrades()
    vakken_per_pagina = len(shop_vakken)

    while True:
        delta_ms = klok.tick(FPS)
        teller += 1

        punten_voor_auto = punten
        punten, auto_punten_buffer = verwerk_auto_punten(
            punten, auto_spoken, multiplier, auto_punten_buffer, delta_ms
        )
        if punten > punten_voor_auto:
            shop_pagina = kies_volgende_shop_pagina(punten, shop_pagina, upgrades, vakken_per_pagina)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                # Klik op het poppetje voor punten.
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

        teken_achtergrond(scherm, teller)

        # Titel en uitleg linksboven.
        titel = font_groot.render("Eng Spel", True, TEKST_KLEUR)
        uitleg = font_klein.render("Klik op het enge poppetje en verzamel punten!", True, SUBTEKST_KLEUR)
        scherm.blit(titel, (40, 28))
        scherm.blit(uitleg, (42, 76))

        # Teken het poppetje.
        teken_poppetje(scherm, poppetje_rect, teller, klik_animatie, punten)
        teken_reset_knop(scherm, reset_knop, punten, multiplier, font_klein, font_shop)

        # Teken het informatiepaneel.
        teken_paneel(scherm, paneel_rect)

        punten_tekst = font_groot.render(f"Punten: {format_tienden(punten)}", True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {format_tienden(klik_kracht * multiplier)}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {format_tienden(auto_spoken * multiplier)}", True, ROZE)
        multiplier_tekst = font_klein.render(f"Multiplier: x{format_tienden(multiplier)}", True, GEEL)
        eng_kracht = bereken_eng_niveau(punten)
        eng_tekst = font_klein.render(f"Eng kracht: {format_getal(eng_kracht)}", True, SUBTEKST_KLEUR)
        scherm.blit(punten_tekst, (paneel_rect.x + 20, 55))
        scherm.blit(klik_tekst, (paneel_rect.x + 20, 120))
        scherm.blit(auto_tekst, (paneel_rect.x + 20, 160))
        scherm.blit(multiplier_tekst, (paneel_rect.x + 20, 192))
        scherm.blit(eng_tekst, (paneel_rect.x + 20, 212))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        pagina_tekst = font_klein.render(f"Pagina {shop_pagina + 1}", True, SUBTEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel_rect.x + 20, 220))
        scherm.blit(pagina_tekst, (paneel_rect.x + 210, 224))

        teken_pagina_knop(scherm, vorige_pagina_knop, "<", shop_pagina > 0, font_klein)
        teken_pagina_knop(scherm, volgende_pagina_knop, ">", True, font_klein)

        # Teken alleen de shop-dingen van deze pagina.
        zichtbare_upgrades = pak_shop_upgrades(upgrades, shop_pagina, vakken_per_pagina)
        for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
            teken_shop_knop(scherm, rect, upgrade, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: de shop springt naar de verste betaalbare bladzijde!", True, SUBTEKST_KLEUR)
        scherm.blit(tip, (38, 505))

        pygame.display.flip()


if __name__ == "__main__":
    speel()
