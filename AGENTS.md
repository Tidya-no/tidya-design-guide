# AGENTS.md

Instruksjoner for AI-agenter og utviklere som endrer dette repoet. Regler for *bruk* av designsystemet står i `DESIGN.md`. Denne filen handler om *endring* av det.

## Filer og hva som må holdes i takt

`tokens.css` er eneste kilde til verdier. Alt annet skal følge etter.

| Når du endrer | Må du også oppdatere / sjekke |
|---|---|
| Et token i `tokens.css` | Fargetabellen og kontrasttallene i `index.html`. Tokentabellen og tall i `DESIGN.md`. Tall i `DESIGN-shadcn.md` (f.eks. kontrast for tekst på `--destructive`). `README.md` hvis noe nevnes der |
| Lys modus i `tokens.css` | Lys modus er definert **to steder** (`@media (prefers-color-scheme: light)` og `:root[data-theme="light"]`). De må være identiske |
| Nytt eller fjernet token | Tabellen i `index.html` og `DESIGN.md`. Ingen ubrukte og ingen udokumenterte tokens |
| En klasse i `components.css` | Demo i `index.html` og omtale i `DESIGN.md`. Klasser som brukes i `index.html` må finnes i CSS, og motsatt |
| Guide-spesifikk stil i `styles.css` | Bare for selve guiden. Gjenbrukbare komponenter hører hjemme i `components.css` |
| En fil som skal publiseres | `pages.yml` (kopieringen til `_site`) og cache-busting-steget for CSS/JS |
| Et htmx-mønster | `DESIGN.md` (htmx-mønstre) og demo i `index.html` |
| Noe som påvirker shadcn-mappingen | `DESIGN-shadcn.md` |

## Kontrastkrav

- Tekst: minst **4,5:1** (WCAG AA). UI-elementer og fokus: minst **3:1**.
- Kontrast regnes mot `--color-bg`, og mot `--color-surface` for innhold i kort.
- Amber (`--color-accent-fill`) kan aldri være tekst på lys bakgrunn (1,5:1). Bruk `--color-accent` til tekst og `--color-accent-fill` til flater.
- Tonet bakgrunn og hover: `--color-accent-bg-subtle` legges oppå bg/surface, og all tekstfarge må fortsatt ha 4,5:1 oppå den (verste tilfelle var feilfarge på surface).
- Regn ut kontrast etter ethvert fargebytte. Ikke anta.

## QA før du åpner PR

CI (`.github/workflows/kvalitet.yml`) kjører html-validate og axe (mørk/lys, 320/1100 px, med og uten åpen dialog). Det er minimum, ikke hele sjekken. Kjør i tillegg lokalt:

1. **html-validate:** `html-validate -c .github/qa/htmlvalidate.json index.html` (0 feil).
2. **axe:** `node .github/qa/axe.cjs` (0 brudd). Test gjerne også 375 og 768 px.
3. **Krysssjekk** (manuelt, se tabellen over):
   - alle tokens finnes i `index.html` og `DESIGN.md`, og verdiene stemmer
   - kontrasttallene i tabellen stemmer med utregnet kontrast
   - begge lysblokkene i `tokens.css` er identiske
   - alle filer som nevnes i `README.md` og `DESIGN.md` finnes
4. **Tastatur:** tab gjennom guiden i begge moduser. Alle fokuserbare elementer skal ha synlig fokus (`:focus-visible`), også inne i dialogen.
5. **Visuelt:** ta skjermbilde i mørk, lys og 375 px. Se på det, ikke bare kjør verktøyene. Axe fanger ikke at noe ser blasst eller trangt ut.
6. **Smal skjerm:** ingen horisontal sidescroll (320 px). Tabeller og kodeblokker som scroller skal ha `tabindex="0"`, `role="region"` og `aria-label`.

Ved htmx-endringer: test mot en kjørende server, ikke bare statisk HTML (fokus etter swap, `aria-live`, validering, `aria-sort`).

## Regler for endringer

- Ingen nye avhengigheter, byggesteg eller `package.json`. Repoet er statisk. QA-verktøy installeres utenfor repoet (se `kvalitet.yml`).
- Hold det kort. Mer tekst og flere komponenter er ikke bedre. Fjern heller enn å legge til.
- Ikke commit midlertidige filer (skjermbilder, scratch-filer). `git status` før commit.
- Tabeller og tall i dokumentene skal være utregnet fra `tokens.css`, ikke skrevet fra hukommelsen.
- UI-tekst er norsk bokmål med ordentlige æ, ø og å.
- Små endringer i én PR, med en kort beskrivelse av hva som er verifisert og hva som **ikke** er det (live-siden, Safari/Firefox, skjermleser).
- Merge først når CI er grønn og eieren ber om det.

## Kjente hull

- Krysssjekken i punkt 3 er ikke automatisert i repoet. Et lite script som sjekker token-dekning, klasser, filreferanser og kontrast mot `tokens.css` ville fange det meste av driften som ellers må sjekkes for hånd.
- Ikke testet: Safari, Firefox, skjermleser, live github.io, shadcn-komponenter utover `Button`/`Input`/`Card`.
