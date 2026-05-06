# Eng Spel

Een simpel clicker-spel in Python met `pygame`.

## Wat doe je in het spel?

- Klik op de enge smiley om punten te krijgen
- Koop `Sterke klik` voor meer punten per klik
- Koop `Spookhulp` voor automatische punten per seconde
- Koop `Mega klik` voor nog veel meer punten per klik
- Koop `Mega spook` voor nog meer automatische punten per seconde
- Er zijn nu oneindig veel shop-dingen verdeeld over oneindig veel pagina's
- Er zijn nu ook oneindig veel `werelden`
- Voor `wereld 2` heb je `1000000000000000000000000000000000000000000000000000000000000000000` punten nodig
- Elke wereld heeft zijn eigen punten, kaarten, luckcoins en shop-pagina's
- Elke nieuwe wereld heeft een ander thema dan de vorige wereld
- Trek gratis kaarten bij multiplier-milestones zoals `x10`, `x100`, `x1000` en verder
- Het deck heeft nu 48 random kaarten: nummers `1` t/m `12`, en elke kaart zit er `4` keer in
- Met `Bekijk kaarten` kun je zien welke kaarten je al hebt en welke nog missen
- Kaarten hebben nu vaste nummer-bonussen, bijvoorbeeld kaart `1 = alles x10`, kaart `9 = multiplier x11`, kaart `10 = geld x30`
- Als je alle vier de kaarten met nummer `12` hebt, krijg je `alles x100000`
- Als je een normaal deck van 48 kaarten compleet maakt, krijg je 1 gouden kaart en begint het normale deck opnieuw
- Gouden kaarten geven dezelfde soort nummer-bonussen, maar dan voor je `luckcoins`
- `Luckcoins` beginnen bij `0`
- Je krijgt vanzelf elke seconde `0.1` luckcoin erbij
- De `Luckshop` is nu oneindig groot met bladzijdes
- De eerste luckshop-koop is nu `1000.0` luckcoins en daarna wordt alles steeds duurder
- In de `Luckshop` kun je luckcoins ruilen voor heel veel normale punten
- Je voortgang wordt automatisch opgeslagen in `spelopslag.json`

## Starten

```bash
pip install -r requirements.txt
python main.py
```

## Besturing

- Linkermuisknop op de smiley = punten krijgen
- Linkermuisknop op een upgrade = upgrade kopen
- Linkermuisknop op `Trek kaart` = een gratis bonuskaart pakken als je een nieuwe multiplier-milestone hebt gehaald
- Linkermuisknop op `Bekijk kaarten` = je hele kaartoverzicht openen
- Linkermuisknop op `Luckshop` = de oneindige luckshop openen en luckcoins uitgeven
- De shop springt vanzelf naar de verste bladzijde waar je iets kunt betalen
- Linkermuisknop op `Reset` = opnieuw beginnen; binnen 1 ronde wordt de bonus steeds duurder, maar na reset begint dat weer opnieuw
- Linkermuisknop op `Echte reset` linksboven = alles wissen en weer echt vanaf 0 beginnen
- Linkermuisknop op `Werelden` = werelden bekijken, kopen en wisselen
- Als het normale deck leeg is, krijg je eerst 1 gouden kaart en daarna begint het normale deck opnieuw
