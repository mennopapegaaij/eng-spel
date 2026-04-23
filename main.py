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


def teken_poppetje(scherm, rect, teller, klik_animatie):
    """Teken het enge poppetje waar je op moet klikken."""
    x = rect.x
    y = rect.y
    breedte = rect.width

    # Bij een klik wordt het poppetje heel even groter.
    extra = 10 if klik_animatie > 0 else 0
    lijf = pygame.Rect(x + 55 - extra // 2, y + 78 - extra // 2, 110 + extra, 150 + extra)
    hoofd_midden = (x + breedte // 2, y + 75)
    hoofd_straal = 52 + extra // 3

    # Schaduw.
    pygame.draw.ellipse(scherm, ZWART, (x + 35, y + 220, 160, 35))

    # Hoofd en lijf.
    pygame.draw.circle(scherm, PANEEL_KLEUR, hoofd_midden, hoofd_straal)
    pygame.draw.circle(scherm, PANEEL_RAND, hoofd_midden, hoofd_straal, 4)
    pygame.draw.rect(scherm, PANEEL_KLEUR, lijf, border_radius=18)
    pygame.draw.rect(scherm, PANEEL_RAND, lijf, 4, border_radius=18)

    # Armen.
    arm_golf = math.sin(teller * 0.08) * 12
    pygame.draw.line(scherm, PANEEL_RAND, (x + 60, y + 130), (x + 10, y + 155 + arm_golf), 8)
    pygame.draw.line(scherm, PANEEL_RAND, (x + 160, y + 130), (x + 210, y + 155 - arm_golf), 8)

    # Ogen - rood als het echt eng is.
    oog_kleur = ROZE if klik_animatie > 0 else ROOD
    pygame.draw.circle(scherm, oog_kleur, (x + 88, y + 65), 10)
    pygame.draw.circle(scherm, oog_kleur, (x + 132, y + 65), 10)
    pygame.draw.circle(scherm, WIT, (x + 91, y + 62), 3)
    pygame.draw.circle(scherm, WIT, (x + 135, y + 62), 3)

    # Mond.
    pygame.draw.arc(scherm, WIT, (x + 78, y + 88, 64, 28), 0, math.pi, 3)

    # Kleine waarschuwingstekst op het poppetje.
    font = pygame.font.SysFont("Arial", 20, bold=True)
    tekst = font.render("KLIK!", True, GEEL)
    scherm.blit(tekst, (x + breedte // 2 - tekst.get_width() // 2, y + 245))


def maak_upgrades():
    """Maak alle shop-dingen.

    Elke upgrade heeft:
    - een naam
    - uitleg
    - vaste prijs
    - bonus voor klikken of per seconde
    """
    return [
        {"titel": "Sterke klik", "uitleg": "+1 per klik", "kosten": 25, "klik_bonus": 1, "auto_bonus": 0},
        {"titel": "Spookhulp", "uitleg": "+1 per seconde", "kosten": 60, "klik_bonus": 0, "auto_bonus": 1},
        {"titel": "Scherpe klik", "uitleg": "+2 per klik", "kosten": 90, "klik_bonus": 2, "auto_bonus": 0},
        {"titel": "Kleine geest", "uitleg": "+2 per seconde", "kosten": 140, "klik_bonus": 0, "auto_bonus": 2},
        {"titel": "Snelle vingers", "uitleg": "+3 per klik", "kosten": 200, "klik_bonus": 3, "auto_bonus": 0},
        {"titel": "Spokenclub", "uitleg": "+3 per seconde", "kosten": 280, "klik_bonus": 0, "auto_bonus": 3},
        {"titel": "Mega klik", "uitleg": "+5 per klik", "kosten": 380, "klik_bonus": 5, "auto_bonus": 0},
        {"titel": "Mega spook", "uitleg": "+5 per seconde", "kosten": 520, "klik_bonus": 0, "auto_bonus": 5},
        {"titel": "Donderklik", "uitleg": "+10 per klik", "kosten": 700, "klik_bonus": 10, "auto_bonus": 0},
        {"titel": "Geestenstorm", "uitleg": "+10 per seconde", "kosten": 950, "klik_bonus": 0, "auto_bonus": 10},
        {"titel": "Nachtklauw", "uitleg": "+20 per klik", "kosten": 1300, "klik_bonus": 20, "auto_bonus": 0},
        {"titel": "Monsterleger", "uitleg": "+20 per seconde", "kosten": 1800, "klik_bonus": 0, "auto_bonus": 20},
        {"titel": "Eindklik", "uitleg": "+50 per klik", "kosten": 2600, "klik_bonus": 50, "auto_bonus": 0},
        {"titel": "Nachtkoning", "uitleg": "+50 per seconde", "kosten": 3200, "klik_bonus": 0, "auto_bonus": 50},
    ]


def teken_paneel(scherm, paneel_rect):
    """Teken het rechter paneel voor punten en upgrades."""
    pygame.draw.rect(scherm, PANEEL_KLEUR, paneel_rect, border_radius=20)
    pygame.draw.rect(scherm, PANEEL_RAND, paneel_rect, 4, border_radius=20)


def maak_shop_vakken(paneel_rect):
    """Maak 8 vakken voor de shop (2 kolommen van 4)."""
    vakken = []
    start_x = paneel_rect.x + 16
    start_y = paneel_rect.y + 215
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

    # Spelvariabelen.
    punten = START_PUNTEN
    klik_kracht = START_KLIK_KRACHT
    auto_spoken = START_AUTO_SPOKEN
    klik_animatie = 0
    teller = 0
    upgrades = maak_upgrades()
    shop_pagina = 0
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
                punten += auto_spoken

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                # Klik op het poppetje voor punten.
                if poppetje_rect.collidepoint(muis_pos):
                    punten += klik_kracht
                    klik_animatie = 10

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
        teken_poppetje(scherm, poppetje_rect, teller, klik_animatie)

        # Teken het informatiepaneel.
        teken_paneel(scherm, paneel_rect)

        punten_tekst = font_groot.render(f"Punten: {punten}", True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {klik_kracht}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {auto_spoken}", True, ROZE)
        scherm.blit(punten_tekst, (paneel_rect.x + 20, 55))
        scherm.blit(klik_tekst, (paneel_rect.x + 20, 120))
        scherm.blit(auto_tekst, (paneel_rect.x + 20, 160))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        pagina_tekst = font_klein.render(f"Pagina {shop_pagina + 1}/{max_pagina + 1}", True, SUBTEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel_rect.x + 20, 190))
        scherm.blit(pagina_tekst, (paneel_rect.x + 210, 194))

        teken_pagina_knop(scherm, vorige_pagina_knop, "<", shop_pagina > 0, font_klein)
        teken_pagina_knop(scherm, volgende_pagina_knop, ">", shop_pagina < max_pagina, font_klein)

        # Teken alleen de shop-dingen van deze pagina.
        start = shop_pagina * vakken_per_pagina
        zichtbare_upgrades = upgrades[start : start + vakken_per_pagina]
        for upgrade, rect in zip(zichtbare_upgrades, shop_vakken):
            teken_shop_knop(scherm, rect, upgrade, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: gebruik < en > voor meer shop-dingen!", True, SUBTEKST_KLEUR)
        scherm.blit(tip, (38, 495))

        pygame.display.flip()
        klok.tick(FPS)


if __name__ == "__main__":
    speel()
