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
    hoogte = rect.height

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


def teken_paneel(scherm):
    """Teken het rechter paneel voor punten en upgrades."""
    paneel = pygame.Rect(620, 30, 300, 480)
    pygame.draw.rect(scherm, PANEEL_KLEUR, paneel, border_radius=20)
    pygame.draw.rect(scherm, PANEEL_RAND, paneel, 4, border_radius=20)
    return paneel


def teken_knop(scherm, rect, titel, uitleg, kosten, punten, font_titel, font_klein):
    """Teken een upgrade-knop."""
    genoeg = punten >= kosten
    kleur = KNOP_KLEUR if genoeg else KNOP_UIT
    rand = KNOP_RAND if genoeg else PANEEL_RAND

    pygame.draw.rect(scherm, kleur, rect, border_radius=16)
    pygame.draw.rect(scherm, rand, rect, 3, border_radius=16)

    titel_tekst = font_titel.render(titel, True, TEKST_KLEUR)
    uitleg_tekst = font_klein.render(uitleg, True, SUBTEKST_KLEUR)
    kosten_tekst = font_klein.render(f"Kosten: {kosten}", True, GEEL)

    scherm.blit(titel_tekst, (rect.x + 14, rect.y + 8))
    scherm.blit(uitleg_tekst, (rect.x + 14, rect.y + 30))
    scherm.blit(kosten_tekst, (rect.x + 14, rect.y + 46))


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
    font_shop = pygame.font.SysFont("Arial", 22, bold=True)
    font_shop_klein = pygame.font.SysFont("Arial", 16)

    # Rechthoeken voor het poppetje en de winkel.
    poppetje_rect = pygame.Rect(120, 110, 220, 260)
    klik_knop = pygame.Rect(650, 210, 240, 64)
    spook_knop = pygame.Rect(650, 285, 240, 64)
    mega_klik_knop = pygame.Rect(650, 360, 240, 64)
    mega_spook_knop = pygame.Rect(650, 435, 240, 64)

    # Spelvariabelen.
    punten = START_PUNTEN
    klik_kracht = START_KLIK_KRACHT
    auto_spoken = START_AUTO_SPOKEN
    kosten_klik = START_KOSTEN_KLIK
    kosten_spook = START_KOSTEN_SPOOK
    kosten_mega_klik = START_KOSTEN_MEGA_KLIK
    kosten_mega_spook = START_KOSTEN_MEGA_SPOOK
    klik_animatie = 0
    teller = 0

    # Dit event geeft elke seconde automatische punten.
    AUTO_PUNT_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(AUTO_PUNT_EVENT, AUTO_EVENT_MS)

    while True:
        teller += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Elke seconde krijg je punten van je spookhelpers.
            if event.type == AUTO_PUNT_EVENT and auto_spoken > 0:
                punten += auto_spoken

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muis_pos = event.pos

                # Klik op het poppetje voor punten.
                if poppetje_rect.collidepoint(muis_pos):
                    punten += klik_kracht
                    klik_animatie = 10

                # Koop een sterkere klik.
                elif klik_knop.collidepoint(muis_pos) and punten >= kosten_klik:
                    punten -= kosten_klik
                    klik_kracht += 1

                # Koop een spookhelper voor automatische punten.
                elif spook_knop.collidepoint(muis_pos) and punten >= kosten_spook:
                    punten -= kosten_spook
                    auto_spoken += 1

                # Koop een grote klik-upgrade.
                elif mega_klik_knop.collidepoint(muis_pos) and punten >= kosten_mega_klik:
                    punten -= kosten_mega_klik
                    klik_kracht += 5

                # Koop een grote spook-upgrade.
                elif mega_spook_knop.collidepoint(muis_pos) and punten >= kosten_mega_spook:
                    punten -= kosten_mega_spook
                    auto_spoken += 5

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
        paneel = teken_paneel(scherm)

        punten_tekst = font_groot.render(f"Punten: {punten}", True, TEKST_KLEUR)
        klik_tekst = font_middel.render(f"Per klik: {klik_kracht}", True, GEEL)
        auto_tekst = font_middel.render(f"Per seconde: {auto_spoken}", True, ROZE)
        scherm.blit(punten_tekst, (paneel.x + 20, 55))
        scherm.blit(klik_tekst, (paneel.x + 20, 120))
        scherm.blit(auto_tekst, (paneel.x + 20, 160))

        winkel_tekst = font_middel.render("Shop", True, TEKST_KLEUR)
        scherm.blit(winkel_tekst, (paneel.x + 20, 190))

        # Teken de shop-knoppen.
        teken_knop(scherm, klik_knop, "Sterkere klik", "+1 punt per klik", kosten_klik, punten, font_shop, font_shop_klein)
        teken_knop(scherm, spook_knop, "Spookhulp", "+1 punt per seconde", kosten_spook, punten, font_shop, font_shop_klein)
        teken_knop(scherm, mega_klik_knop, "Mega klik", "+5 punten per klik", kosten_mega_klik, punten, font_shop, font_shop_klein)
        teken_knop(scherm, mega_spook_knop, "Mega spook", "+5 punten per seconde", kosten_mega_spook, punten, font_shop, font_shop_klein)

        # Kleine tip onderaan.
        tip = font_klein.render("Tip: koop eerst wat sterkere klikken!", True, SUBTEKST_KLEUR)
        scherm.blit(tip, (38, 495))

        pygame.display.flip()
        klok.tick(FPS)


if __name__ == "__main__":
    speel()
