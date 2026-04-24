"""Eng Spel - een simpel clicker-spel met een eng poppetje."""

import math
import sys

import pygame

from instellingen import *


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
    """Geef het eng-niveau terug.

    0 punten = niveau 0
    1 t/m 9 = niveau 1
    10 t/m 99 = niveau 2
    100 t/m 999 = niveau 3
    enzovoort.
    """
    if punten < 1:
        return 0
    return int(math.log10(punten)) + 1


def format_getal(getal):
    """Maak hele getallen netjes kort en decimalen met 1 cijfer."""
    afgerond = round(getal, 1)
    if afgerond == int(afgerond):
        return str(int(afgerond))
    return f"{afgerond:.1f}"


def bereken_reset_bonus(punten):
    """Geef de resetbonus terug.

    Elke 50 punten geeft +0.1 multiplier.
    Dus:
    - 0 t/m 49 punten = +0.0x
    - 50 t/m 99 punten = +0.1x
    - 100 t/m 149 punten = +0.2x
    """
    return (int(punten) // 50) / 10


def teken_poppetje(scherm, rect, teller, klik_animatie, punten):
    """Teken het enge poppetje waar je op moet klikken."""
    x = rect.x
    y = rect.y
    breedte = rect.width
    eng_niveau = bereken_eng_niveau(punten)
    visueel_niveau = min(eng_niveau, 6)

    # Bij een klik wordt het poppetje heel even groter.
    extra = 10 if klik_animatie > 0 else 0
    lijf = pygame.Rect(x + 55 - extra // 2, y + 78 - extra // 2, 110 + extra, 150 + extra)
    hoofd_midden = (x + breedte // 2, y + 75)
    hoofd_straal = 52 + extra // 3
    huid_kleur = (
        max(0, PANEEL_KLEUR[0] - visueel_niveau * 3),
        max(0, PANEEL_KLEUR[1] - visueel_niveau * 2),
        max(0, PANEEL_KLEUR[2] - visueel_niveau * 5),
    )
    rand_kleur = (
        min(255, PANEEL_RAND[0] + visueel_niveau * 12),
        max(0, PANEEL_RAND[1] - visueel_niveau * 4),
        min(255, PANEEL_RAND[2] + visueel_niveau * 8),
    )

    # Schaduw.
    pygame.draw.ellipse(scherm, ZWART, (x + 35, y + 220, 160, 35))

    # Hoe enger het niveau, hoe sterker de aura rond het hoofd.
    if visueel_niveau >= 2:
        aura_straal = hoofd_straal + 8 + visueel_niveau * 3
        pygame.draw.circle(scherm, (70, 20, 80), hoofd_midden, aura_straal, 3)

    # Hoofd en lijf.
    pygame.draw.circle(scherm, huid_kleur, hoofd_midden, hoofd_straal)
    pygame.draw.circle(scherm, rand_kleur, hoofd_midden, hoofd_straal, 4)
    pygame.draw.rect(scherm, huid_kleur, lijf, border_radius=18)
    pygame.draw.rect(scherm, rand_kleur, lijf, 4, border_radius=18)

    # Armen.
    arm_golf = math.sin(teller * 0.08) * (12 + visueel_niveau * 2)
    pygame.draw.line(scherm, rand_kleur, (x + 60, y + 130), (x + 10, y + 155 + arm_golf), 8)
    pygame.draw.line(scherm, rand_kleur, (x + 160, y + 130), (x + 210, y + 155 - arm_golf), 8)

    # Hoorns bij hogere niveaus.
    if visueel_niveau >= 4:
        pygame.draw.polygon(scherm, rand_kleur, [(x + 78, y + 10), (x + 96, y - 28), (x + 110, y + 18)])
        pygame.draw.polygon(scherm, rand_kleur, [(x + 130, y + 18), (x + 144, y - 28), (x + 162, y + 10)])

    # Ogen - rood als het echt eng is.
    oog_kleur = ROZE if klik_animatie > 0 else ROOD
    oog_straal = 10 + min(visueel_niveau, 3)
    pygame.draw.circle(scherm, oog_kleur, (x + 88, y + 65), oog_straal)
    pygame.draw.circle(scherm, oog_kleur, (x + 132, y + 65), oog_straal)
    pygame.draw.circle(scherm, WIT, (x + 91, y + 62), 3)
    pygame.draw.circle(scherm, WIT, (x + 135, y + 62), 3)

    if visueel_niveau >= 2:
        pygame.draw.line(scherm, ZWART, (x + 74, y + 48), (x + 97, y + 58), 3)
        pygame.draw.line(scherm, ZWART, (x + 123, y + 58), (x + 146, y + 48), 3)

    if visueel_niveau >= 5:
        pygame.draw.circle(scherm, oog_kleur, (x + 110, y + 34), 8)
        pygame.draw.circle(scherm, WIT, (x + 112, y + 31), 2)

    # Mond.
    if visueel_niveau <= 1:
        pygame.draw.arc(scherm, WIT, (x + 78, y + 88, 64, 28), 0, math.pi, 3)
    else:
        pygame.draw.arc(scherm, WIT, (x + 72, y + 92, 76, 34), 0, math.pi, 3)
        tanden = 3 + min(visueel_niveau, 4)
        for tand in range(tanden):
            tand_x = x + 78 + tand * 12
            pygame.draw.polygon(scherm, WIT, [(tand_x, y + 103), (tand_x + 6, y + 118), (tand_x + 12, y + 103)])

    if visueel_niveau >= 6:
        for i in range(6):
            vonk_x = x + 44 + i * 24
            vonk_y = y + 18 + (i % 2) * 12
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x - 8, vonk_y - 14), 2)
            pygame.draw.line(scherm, ROOD, (vonk_x, vonk_y), (vonk_x + 8, vonk_y - 12), 2)

    # Kleine waarschuwingstekst op het poppetje.
    font = pygame.font.SysFont("Arial", 20, bold=True)
    font_klein = pygame.font.SysFont("Arial", 16, bold=True)
    tekst = font.render("KLIK!", True, GEEL)
    scherm.blit(tekst, (x + breedte // 2 - tekst.get_width() // 2, y + 245))
    niveau_tekst = font_klein.render(f"Eng niveau {eng_niveau}", True, ROZE)
    scherm.blit(niveau_tekst, (x + breedte // 2 - niveau_tekst.get_width() // 2, y + 268))


def maak_upgrades():
    """Maak alle shop-dingen.

    Elke upgrade heeft:
    - een naam
    - uitleg
    - vaste prijs
    - bonus voor klikken of per seconde
    """
    return [
        {"titel": "Sterke klik", "uitleg": "+1 per klik", "kosten": 40, "klik_bonus": 1, "auto_bonus": 0},
        {"titel": "Spookhulp", "uitleg": "+1 per seconde", "kosten": 100, "klik_bonus": 0, "auto_bonus": 1},
        {"titel": "Scherpe klik", "uitleg": "+4 per klik", "kosten": 180, "klik_bonus": 4, "auto_bonus": 0},
        {"titel": "Kleine geest", "uitleg": "+4 per seconde", "kosten": 280, "klik_bonus": 0, "auto_bonus": 4},
        {"titel": "Snelle vingers", "uitleg": "+10 per klik", "kosten": 420, "klik_bonus": 10, "auto_bonus": 0},
        {"titel": "Spokenclub", "uitleg": "+9 per seconde", "kosten": 620, "klik_bonus": 0, "auto_bonus": 9},
        {"titel": "Mega klik", "uitleg": "+22 per klik", "kosten": 900, "klik_bonus": 22, "auto_bonus": 0},
        {"titel": "Mega spook", "uitleg": "+18 per seconde", "kosten": 1200, "klik_bonus": 0, "auto_bonus": 18},
        {"titel": "Donderklik", "uitleg": "+45 per klik", "kosten": 1700, "klik_bonus": 45, "auto_bonus": 0},
        {"titel": "Geestenstorm", "uitleg": "+35 per seconde", "kosten": 2300, "klik_bonus": 0, "auto_bonus": 35},
        {"titel": "Nachtklauw", "uitleg": "+90 per klik", "kosten": 3400, "klik_bonus": 90, "auto_bonus": 0},
        {"titel": "Monsterleger", "uitleg": "+70 per seconde", "kosten": 4600, "klik_bonus": 0, "auto_bonus": 70},
        {"titel": "Eindklik", "uitleg": "+200 per klik", "kosten": 7000, "klik_bonus": 200, "auto_bonus": 0},
        {"titel": "Nachtkoning", "uitleg": "+150 per seconde", "kosten": 8500, "klik_bonus": 0, "auto_bonus": 150},
    ]


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
    genoeg = punten >= upgrade["kosten"]
    kleur = KNOP_KLEUR if genoeg else KNOP_UIT
    rand = KNOP_RAND if genoeg else PANEEL_RAND

    pygame.draw.rect(scherm, kleur, rect, border_radius=12)
    pygame.draw.rect(scherm, rand, rect, 2, border_radius=12)

    titel_tekst = font_titel.render(upgrade["titel"], True, TEKST_KLEUR)
    uitleg_tekst = font_klein.render(upgrade["uitleg"], True, SUBTEKST_KLEUR)
    kosten_tekst = font_klein.render(f"{upgrade['kosten']} p", True, GEEL)

    scherm.blit(titel_tekst, (rect.x + 8, rect.y + 6))
    scherm.blit(uitleg_tekst, (rect.x + 8, rect.y + 24))
    scherm.blit(kosten_tekst, (rect.x + 8, rect.y + 39))


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

    bonus_tekst = font.render(f"Reset voor +{format_getal(reset_bonus)}x", True, TEKST_KLEUR)
    scherm.blit(
        bonus_tekst,
        (rect.x + rect.width // 2 - bonus_tekst.get_width() // 2, rect.y + 10),
    )

    if reset_bonus > 0:
        uitleg = font_klein.render(f"Nieuwe multiplier: x{format_getal(multiplier + reset_bonus)}", True, GEEL)
    else:
        uitleg = font_klein.render("Spaar 50 punten voor +0.1x", True, SUBTEKST_KLEUR)

    scherm.blit(
        uitleg,
        (rect.x + rect.width // 2 - uitleg.get_width() // 2, rect.y + 42),
    )


def reset_speltoestand():
    """Zet de spelwaarden terug voor een nieuwe ronde."""
    return START_PUNTEN, START_KLIK_KRACHT, START_AUTO_SPOKEN, 0


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
    multiplier = 1.0
    klik_animatie = 0
    teller = 0
    upgrades = maak_upgrades()
    vakken_per_pagina = len(shop_vakken)
    max_pagina = (len(upgrades) - 1) // vakken_per_pagina

    # Dit event geeft elke seconde automatische punten.
    auto_punt_event = pygame.USEREVENT + 1
    pygame.time.set_timer(auto_punt_event, AUTO_EVENT_MS)

    while True:
        teller += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Elke seconde krijg je punten van je spookhelpers.
            if event.type == auto_punt_event and auto_spoken > 0:
                punten += auto_spoken * multiplier

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                # Klik op het poppetje voor punten.
                if poppetje_rect.collidepoint(muis_pos):
                    punten += klik_kracht * multiplier
                    klik_animatie = 10

                # Reset het spel en maak de multiplier groter.
                elif reset_knop.collidepoint(muis_pos):
                    reset_bonus = bereken_reset_bonus(punten)
                    if reset_bonus <= 0:
                        continue

                    multiplier += reset_bonus
                    punten, klik_kracht, auto_spoken, shop_pagina = reset_speltoestand()
                    klik_animatie = 0

                # Ga naar de vorige shop-pagina.
                elif vorige_pagina_knop.collidepoint(muis_pos) and shop_pagina > 0:
                    shop_pagina -= 1

                # Ga naar de volgende shop-pagina.
                elif volgende_pagina_knop.collidepoint(muis_pos) and shop_pagina < max_pagina:
                    shop_pagina += 1

                # Klik op een shop-ding.
                else:
                    start = shop_pagina * vakken_per_pagina
                    zichtbare_upgrades = upgrades[start : start + vakken_per_pagina]

                    for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
                        if rect.collidepoint(muis_pos) and punten >= upgrade["kosten"]:
                            punten -= upgrade["kosten"]
                            klik_kracht += upgrade["klik_bonus"]
                            auto_spoken += upgrade["auto_bonus"]
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

        punten_tekst = font_groot.render(f"Punten: {format_getal(punten)}", True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {format_getal(klik_kracht * multiplier)}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {format_getal(auto_spoken * multiplier)}", True, ROZE)
        multiplier_tekst = font_klein.render(f"Multiplier: x{format_getal(multiplier)}", True, GEEL)
        eng_niveau = bereken_eng_niveau(punten)
        volgende_grens = 1 if punten < 1 else 10 ** eng_niveau
        eng_tekst = font_klein.render(f"Volgende enge vorm bij: {volgende_grens}", True, SUBTEKST_KLEUR)
        scherm.blit(punten_tekst, (paneel_rect.x + 20, 55))
        scherm.blit(klik_tekst, (paneel_rect.x + 20, 120))
        scherm.blit(auto_tekst, (paneel_rect.x + 20, 160))
        scherm.blit(multiplier_tekst, (paneel_rect.x + 20, 192))
        scherm.blit(eng_tekst, (paneel_rect.x + 20, 212))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        pagina_tekst = font_klein.render(f"Pagina {shop_pagina + 1}/{max_pagina + 1}", True, SUBTEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel_rect.x + 20, 220))
        scherm.blit(pagina_tekst, (paneel_rect.x + 210, 224))

        teken_pagina_knop(scherm, vorige_pagina_knop, "<", shop_pagina > 0, font_klein)
        teken_pagina_knop(scherm, volgende_pagina_knop, ">", shop_pagina < max_pagina, font_klein)

        # Teken alleen de shop-dingen van deze pagina.
        start = shop_pagina * vakken_per_pagina
        zichtbare_upgrades = upgrades[start : start + vakken_per_pagina]
        for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
            teken_shop_knop(scherm, rect, upgrade, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: gebruik < en > voor meer shop-dingen!", True, SUBTEKST_KLEUR)
        scherm.blit(tip, (38, 505))

        pygame.display.flip()
        klok.tick(FPS)


if __name__ == "__main__":
    speel()
