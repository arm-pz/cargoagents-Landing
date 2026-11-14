# Cargo Agents

Landing page for **cargoagents.si**, sea freight handled by an agent on every container.
The `.si` stands for "superintelligence", not for a country.

## What is here

- `index.html`: the finished page. Deploy it together with `assets/`.
- `assets/`: the photographs the page uses.
- `src/page.src.html`: the page template (CSS, markup, script).
- `src/build.py`: fills in the globe's land mask and writes `index.html`. Run `python3 src/build.py`.
- `design/`: the earlier illustrated design boards. The page no longer uses them.

## Photographs

All from Pexels under the Pexels licence (free to use, no attribution required). Replace them with your own when you have them.

| File | Used for | Source |
| --- | --- | --- |
| `hero.jpg` | Hero | https://www.pexels.com/photo/an-aerial-shot-of-a-cargo-ship-11820859/ |
| `open-sea.jpg` | Band under the opening statement | https://www.pexels.com/photo/directly-above-a-fully-loaded-cargo-ship-on-a-sea-12530458/ |
| `full-container.jpg` | Full container tab | https://www.pexels.com/photo/photo-of-multicolored-shipping-containers-14400831/ |
| `part-load.jpg` | Part load tab | https://www.pexels.com/photo/boxes-on-shelves-inside-a-warehouse-5156696/ |
| `terminal.jpg` | Refrigerated tab (a general terminal shot, not reefer units) | https://www.pexels.com/photo/cargo-containers-in-harbor-14020705/ |
| `quay.jpg` | Footer | https://www.pexels.com/photo/port-with-cranes-2326876/ |

## Notes

- Fonts load from Google Fonts: Archivo, Inter Tight, IBM Plex Mono.
- Motion uses GSAP 3.12.5 and ScrollTrigger from cdnjs. Without them the page falls back to a static layout. With reduced motion on, nothing scrolls or pins.
- Scope is sea freight only: full containers, part loads and refrigerated, with customs handled.
- Page order: photo hero with a quote and track bar, the idea, the shipment workspace (an example the visitor can act on), the route story, container types, questions, quote form.
- The workspace, its prices and dates, and the container number `CAGU 482615 0` are example data and are labelled as such on the page. The track bar checks the ISO 6346 check digit but looks nothing up.
- The quote form only drafts text for the visitor to copy. Nothing is sent anywhere yet, and what the call to action should do is still open (quote, booking or container lookup).
- Legal and address lines in the footer are placeholders in square brackets.
