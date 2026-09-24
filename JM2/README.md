# JM² – Logo-Set (Entwurf)

Neues Branding für **JM²** (a eurocept homecare company), im Stil des Hoenle-Medical-Logos, aber in Schwarz, Chrom und dunklem Silber.

- `JM2_Uebersicht.png`: alle Varianten auf einen Blick
- `svg/`: Vektordateien, Schrift in Pfade umgewandelt
- `png/`: 3000 px breit, transparenter Hintergrund (App-Icon 1024 px)

| Datei | Verwendung |
|---|---|
| `JM2_payoff_left_rgb` | Hauptlogo quer, mit Unterzeile |
| `JM2_left_notagline_rgb` | quer, ohne Unterzeile |
| `JM2_payoff_center_rgb` / `JM2_center_rgb` | hochkant, mit und ohne Unterzeile |
| `JM2_pearl_rgb` | nur die Perle |
| `*_dark_rgb` | für dunkle Hintergründe |
| `JM2_icon_1024` | App-/Profil-Icon auf Schwarz |

## Farben

| Rolle | Hex |
|---|---|
| Schwarz (Text, Perle) | `#0b0b0d` |
| Dunkelsilber (²) | `#5f646c` |
| Silber | `#9aa0a8` |
| Chrom (Lichtkante) | `#e4e7eb` |
| Unterzeile grau | `#8a8e94` |

## Schriften

- Wortmarke: **Unbounded** Bold, dieselbe Familie wie „hoenle medical“
- Unterzeile: **Newsreader** Light

Beide Schriften stehen unter der SIL Open Font License.

## Neu erzeugen

```sh
pip install fonttools
python3 _build/build.py     # SVGs
node _build/render.js 3000  # PNGs (benötigt Playwright)
```
