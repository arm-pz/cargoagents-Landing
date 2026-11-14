# Cargo Agents

Landing page for **cargoagents.si**, sea freight handled by an agent on every container.
The `.si` stands for "superintelligence", not for a country.

## What is here

- `index.html`: the finished page. One self-contained file, deploy it as is.
- `src/page.src.html`: the page template (CSS, markup, GSAP motion). It holds placeholders for the artwork.
- `src/build.py`: fills the placeholders from the design boards and writes `index.html`. Run `python3 src/build.py` from anywhere in the repo.
- `design/`: the design-canvas boards the artwork came from (`HeroCelestial.dc.html` for the hero and `Main.dc.html` for the footer scene).

## Notes

- Fonts load from Google Fonts: Instrument Serif, Inter Tight, IBM Plex Mono.
- Motion uses GSAP 3.12.5 and ScrollTrigger from cdnjs. Without them the page falls back to a static layout. With reduced motion on, nothing scrolls or pins.
- Scope is sea freight only: full containers, part loads and refrigerated, with customs handled.
- Page order: hero with a quote and track bar, the idea, the shipment workspace (an example the visitor can act on), the route story, container types, questions, quote form.
- The workspace, its prices and dates, and the container number `CAGU 482615 0` are example data and are labelled as such on the page. The track bar checks the ISO 6346 check digit but looks nothing up.
- The quote form only drafts text for the visitor to copy. Nothing is sent anywhere yet, and what the call to action should do is still open (quote, booking or container lookup).
- Legal and address lines in the footer are placeholders in square brackets.
