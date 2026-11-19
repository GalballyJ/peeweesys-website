# PeeWeeSys — 986 / 996 instrument cluster assets (v2.1.1)

`pws_cluster.js` is the single source: every SVG and PNG here came out of `renderClusterSvg(state)`. `demo.html` is a live test page.

## What changed in 2.1.1
- **996 end-pod housings:** the volt and oil scales stay exactly where they were, but each housing is now drawn with the same curvature as the main dials (`END_HOUSING_R`, 84) and pulled in behind its neighbour (`END_HOUSING_INSET`, 9), so only a crescent shows and its outer curve matches the dials.

## What changed in 2.1
- **K24 small displays are dot-matrix too.** On `display: 'k24'` the speedo speed and the clock are drawn as dots on a pixel grid, like the centre display. `early` and `k21` keep segment LCDs.
- **Typography:** `numerals: 'italic'` (Boxster S look, default on 3-dial) or `'upright'` (traditional 996 look, default on 5-dial). Applies to every dial.
- **K21 centre display:** odometer and trip are small on the top two lines. The lower field is the OBC and only appears when the OBC is coded; it shows `obcMode`: `'temp'` (default), `'mpg'`, `'range'` or `'limit'`.
- **Early LCD centre display:** digital speed always; outside temperature only when the OBC is coded.
- **Non-OBC cars (all generations):** odometer and trip only, no temperature or computer values.
- **Clock 12/24h:** `clockFormat: '12' | '24'` (default 24). Pass `clock` as 24-hour `HH:MM`; in 12-hour mode a dot top-left means AM, bottom-left PM (lit dot on segment and dot-matrix clocks alike).
- **996 end pods:** now small (r 50) and tucked behind the speedo and fuel/temp pods, like the real car. Their needles pivot out of sight. The housing narrows to fit.
- **Knobs:** single round caps, no stems.

## Display generations (`state.display`)
| value | car | speedo window | centre window (OBC coded) | centre window (not coded) | clock |
|---|---|---|---|---|---|
| `early` | 996.1, early 986 | segment: odometer + trip | segment: speed + outside temp | segment: speed only | segment |
| `k21` | 986 c.2001 | segment: speed | segment: small odo + trip, OBC field below | small odo + trip | segment |
| `k24` | 986.2 / 996.2 | **dots**: speed | **dots**: LIMIT/CHECK/OIL/BC menu + values | **dots**: odo + trip | **dots** |

## State (full list)
| key | default | notes |
|---|---|---|
| `dials` | 3 | 3 = 986 (680×320), 5 = 996 (880×320) |
| `display` | 'k24' | 'early' \| 'k21' \| 'k24' |
| `faceTheme` | 'black' | white faces get chrome bezels, black faces black; override with `bezel` |
| `numerals` | italic on 3-dial, upright on 5-dial | 'italic' \| 'upright' |
| `scaleId` / `scale` | '180_mph' | `160_mph`, `180_mph`, `200_mph`, `250_kmh`, `300_kmh` |
| `speedPred` | from `simMph` | `{indicatedDisplay, trueDisplay}`; needle = indicated, green mark = true |
| `digitalSpeed` | true speed | |
| `rpm`, `redlineRpm` | 4000, 7200 | |
| `coolantPred.indicatedC`, `tempUnit` | 80, 'C' | |
| `fuelPred.indicatedPct` | 75 | |
| `volts`, `oilBar` | 13.8, 3.2 | 996 only |
| `odometer`, `trip`, `ambient` | | |
| `clock`, `clockFormat` | '14:25', '24' | |
| `pm.obc_enabled` | true | drives all three generations as above |
| `obcMode` + `obcMpg`/`obcRange`/`obcLimit` | 'temp' | K21 OBC field |
| `obcMenu`, `obcActive`, `obcLines`, `obcBig` | | K24 OBC |
| `pm.cruise`, `cruiseLamp` | false, 'speedo' | 'strip' moves it to the lamp bar |
| `pm.spoiler` | false | lamp bar |
| `telltales` | | `{cruise, spoiler}` false shows a coded lamp unlit |
| `idPrefix` | auto | unique gradient IDs per cluster on a page |

Only coded features get a lamp.

## Animating
Needles: `<g id="needle-{tach|speedo|coolant|fuel|volt|oil}" data-cx data-cy transform="rotate(a hx hy)">`, each about its own hub:
```js
g.setAttribute('transform', `rotate(${PWSCluster.angleFor('fuel', pct)} ${g.dataset.cx} ${g.dataset.cy})`);
```
`hubFor(dials, gauge)` gives the hub too. Displays: `#obc-display` (`data-display`, `data-obc`), `#speed-display`, `#clock-display` (`data-format`, `data-ampm`); `data-dots="1"` marks dot-matrix windows. Re-render for display text changes; it's cheap.

## Note for the coding agent
The 996 end-pod scale coordinates moved from the original brief (volt 140,166 r50; oil 740,166 r50; the housing is a larger circle derived from these) and their sweeps changed (volt −146° → −48°, oil +146° → +48°, about hubs hidden behind the neighbouring pods). Read them from `LAYOUTS` / `SWEEP` / `angleFor()` rather than hard-coding.

## Worth checking
Built from your photos plus memory, not traced from a cluster: exact OBC wording per market and software, K21 OBC unit labels, and lamp positions in the bar.
