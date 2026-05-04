# Eng Spel

Een simpel clicker-spel in Python met `pygame`.

## Wat doe je in het spel?

- Klik op de enge smiley om punten te krijgen
- Koop `Sterke klik` voor meer punten per klik
- Koop `Spookhulp` voor automatische punten per seconde
- Koop `Mega klik` voor nog veel meer punten per klik
- Koop `Mega spook` voor nog meer automatische punten per seconde
- Er zijn nu oneindig veel shop-dingen verdeeld over oneindig veel pagina's
- Trek gratis kaarten bij multiplier-milestones zoals `x10`, `x100`, `x1000` en verder
- Het deck heeft nu 48 random kaarten: nummers `1` t/m `12`, en elke kaart zit er `4` keer in
- Met `Bekijk kaarten` kun je zien welke kaarten je al hebt en welke nog missen

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
- De shop springt vanzelf naar de verste bladzijde waar je iets kunt betalen
- Linkermuisknop op `Reset` = opnieuw beginnen; binnen 1 ronde wordt de bonus steeds duurder, maar na reset begint dat weer opnieuw
- Als alle 48 kaarten op zijn, kun je geen nieuwe kaarten meer trekken
