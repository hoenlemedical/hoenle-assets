# JM² – Logo & Hintergründe

Neues Branding für **JM²** (a eurocept homecare company), im Stil des Hoenle-Medical-Logos, aber in Schwarz, Chrom und dunklem Silber.

- `JM2_Uebersicht.png`: alle Logo-Varianten auf einen Blick
- `JM2_Hintergruende_Uebersicht.png`: alle Hintergründe auf einen Blick
- `svg/`: Vektordateien, Schrift in Pfade umgewandelt
- `png/`: 3000 px breit, transparenter Hintergrund (App-Icon 1024 px)
- `wallpaper_png/`: Mac-Lockscreens (5120 × 2880) und Teams-Hintergründe (1920 × 1080)
- `wallpaper_svg/`: dieselben Hintergründe als Vektordateien

| Datei | Verwendung |
|---|---|
| `JM2_payoff_left_rgb` | Hauptlogo quer, mit Unterzeile |
| `JM2_left_notagline_rgb` | quer, ohne Unterzeile |
| `JM2_payoff_center_rgb` / `JM2_center_rgb` | hochkant, mit und ohne Unterzeile |
| `JM2_pearl_rgb` | nur die Perle |
| `*_dark_rgb` | für dunkle Hintergründe |
| `JM2_icon_1024` | App-/Profil-Icon auf Schwarz |

## Hintergründe

Gleiche Aufteilung wie beim Hoenle-Set:

| Datei | Motiv |
|---|---|
| `JM2_Mac_A_Dunkel_Perle_zentral` | dunkel, Perle mittig |
| `JM2_Mac_B_Dunkel_Perle_rechts` | dunkel, Perle rechts |
| `JM2_Mac_C_Hell_Perle_zentral` | hell, Perle mittig mit Schatten |
| `JM2_Mac_D_Hell_Logo_klein` | hell, kleines Logo oben |
| `JM2_Mac_E_Hell_Logo_unten` | hell, Logo unten |
| `JM2_Teams_T1_Hell_Logo_links` | hell, Logo unten links |
| `JM2_Teams_T2_Hell_Perle_Logo` | hell, Perle rechts, Logo links |
| `JM2_Teams_T3_Hell_Logo_rechts` | hell, Logo unten rechts |
| `JM2_Teams_T4_Dunkel_Perle` | dunkel, Perle rechts |
| `JM2_Teams_T5_Dunkel_Logo_Chip` | dunkel, Logo auf heller Plakette |

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
node _build/render.js 3000  # Logo-PNGs (benötigt Playwright)
python3 _build/wallpapers.py                               # Hintergrund-SVGs
node _build/render.js 0 ../wallpaper_svg ../wallpaper_png  # Hintergrund-PNGs
```
