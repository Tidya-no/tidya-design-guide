---
name: tidya-rust-app
description: Bygg eller utvid en liten Tidya-app i Rust (axum, Askama, htmx, ingen database) etter mønsteret i tidya-website-rust og tidya-faktura. Bruk ved ny app, ny side, nytt vedlegg i CI/vedlikehold, ny pinnet ekstern fil eller binær, eller når en workflow, deploy eller innlogging skal settes opp.
---

# Tidya Rust-app

Reglene her er begrunnelsene. Koden ligger i de to repoene, som er fasit: les dem, ikke kopier fra hukommelsen.

- `Tidya-no/tidya-website-rust`: enklest. Statiske sider, kontaktskjema med SMTP.
- `Tidya-no/tidya-faktura`: full app. Magic-link-innlogging, multipart, ekstern binær (Typst), pinnet pdf.js.
- Designsystemet er dette repoet: `tokens.css`, `components.css`, `fonts/`, `brand/`, regler i `DESIGN.md`.

Legg begge appene til i sesjonen med `add_repo` før du begynner. Les `AGENTS.md` i den du låner fra. Finn eksempler ved å søke i repoet (`vedlikehold.yml`, `scripts/`, `src/lib.rs`), ikke ved å stole på stier her.

## Prinsipper

- Rust edition 2024, `axum`, `askama` (maler kompileres), `tower-http`, `tracing`. Ingen database, ingen JS-byggesteg, ingen JS-rammeverk. htmx er én kopiert fil.
- Tilstand i minnet er greit når den tåler restart (30 min PDF-lager, engangslenker). Trenger noe å overleve restart, si fra til eieren før du legger til en database.
- Ruter og sider i `src/lib.rs`/`sider.rs`, `app(Config) -> Router` slik at tester starter ekte router med `tower::ServiceExt::oneshot`. Ikke mock. En test må kunne feile.
- htmx-svar: fragment ved `HX-Request`, full side ellers, og alltid `Vary: HX-Request`. Skjemaer virker uten JS. 422 og 429 byttes inn i `htmx-config`, andre 4xx/5xx ikke.
- Alt utenom statiske filer har `Cache-Control: no-store` når siden er brukerspesifikk. Sikkerhetsheadere (`nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`) settes i `app()`.
- Design: kopier `tokens.css`, `components.css`, `fonts/`, `brand/` uendret fra dette repoet inn i `static/design` og `static/brand`. Bare `var(--…)` og komponentklasser, ingen hardkodede farger. Appens egen CSS i en egen fil.
- Språk: kode, kommentarer og identifikatorer på engelsk. Domeneord, loggmeldinger, testnavn og brukertekst på norsk (`æøå` blir `ae oe aa` i identifikatorer). Hard tabs.

## Innlogging (hvis appen trenger det)

Statuløse signerte tokens (`purpose|utløp|e-post` + HMAC), ingen database. Les `src/auth.rs` i faktura og behold disse reglene:
- Formålet (`lenke`/`okt`) hindrer at en lenke fungerer som øktcookie. Lenken er engangs (i minnet) og gyldig 15 min.
- E-postlenken åpner en side med knapp (`GET`), selve innloggingen er `POST`, så en skanner ikke bruker opp lenken.
- Cookie: `HttpOnly; SameSite=Lax`, `Secure` når `SITE_URL` er https. `Lax` er CSRF-beskyttelsen. Ikke løsne.
- Ikke la fanen som ba om lenken logge inn via serveren (polling av en ventende innlogging): da blir den som ba om lenken innlogget når eieren av adressen klikker. Bruk `BroadcastChannel` mellom faner i samme nettleser.
- `POST /logg-inn` svarer likt for kjente og ukjente adresser og sender i bakgrunnen.
- `Mailer` er en enum (`Smtp`, `Logg`, `Minne`), ikke en trait.

## Ekstern binær eller kopiert fil (mønsteret mot råte)

Ting som ikke er en cargo-avhengighet (Typst, pdf.js, htmx) pinnes slik:
1. Versjon og sha256 står ett sted (`scripts/<navn>.env`). Dockerfile og CI bruker samme installer-script, så testene kjører det samme som imaget.
2. Et oppdateringsscript (`scripts/oppdater-<navn>.sh <versjon>`) som henter, verifiserer og skriver filen.
3. En jobb i `vedlikehold.yml` sammenligner mot siste utgave hver mandag og feiler høyt med oppskriften i feilmeldingen.
4. Hent ikke fra en containerregistry: Coolify-serveren kommer ikke til `ghcr.io` (403). Bruk GitHub Releases med sha256.
5. Kjør ekstern binær bare gjennom én funksjon: tomt miljø (aldri `SESSION_SECRET`/`SMTP_PASS`), eget temp-katalog, tidsgrense, `setrlimit`. Ingenting fra brukeren i kildekoden til programmet; send data som JSON-fil.

## CI/CD og vedlikehold

Struktur i `.github/workflows/`:
- `deploy.yml`: `test` (fmt, clippy `-D warnings`, test, `cargo audit`) → `docker` (bygger uten push) → `deploy` (bare `main`: push, månedlig `schedule`, `workflow_dispatch`, med `force=true`) og `deploy-test` (alle andre branches, pusher til branchen `test`, aldri Dependabot). Coolify bygger fra git. Runneren joiner tailnettet (Tailscale OIDC, `tag:ci`) og kaller Coolify `/api/v1/deploy`.
- `vedlikehold.yml`: én fil for alt som kjører etter kalender (mandag): audit, nye versjoner av pinnede filer, Dependabot-PR-er eldre enn 14 dager. Ikke én fil per sjekk.
- Dependabot for cargo og actions. Alle actions pinnes til commit-SHA med tag som kommentar, fordi deploy-jobbene gir dem OIDC-token og `COOLIFY_TOKEN`.

**Varsling er en rød workflow-kjøring** (GitHub sender e-post). En sjekk som finner noe avslutter med ikke-null og feiler igjen neste mandag til årsaken er borte. Ikke lag issues, ikke legg til flere workflows for varsling.

Fallgruver vi har betalt for:
- Planlagte workflows kjører bare fra **standardbranchen**, og Actions-fanen viser filene derfra. Sett den til `main` før du forventer noe.
- `gh` i en jobb uten checkout trenger `GH_REPO`.
- Org-secrets virker ikke for private repoer på GitHub Free. Sett secrets per repo.
- Ressursgrenser (`setrlimit` på adresserom) må måles med samme libc som imaget: musl og glibc gir veldig forskjellige tall. Mål på det som havner i imaget.
- Kald bygging av store crates (for eksempel hele `typst`) tok 20 min og flere GB. Bruk ferdig binær.
- Hemmeligheter (`SMTP_PASS`, `SESSION_SECRET`) skal ikke være «Available at Buildtime» i Coolify.
- Feil i SMTP bare logges i appen. Test innlogging/kontaktskjema etter SMTP-endringer, eller ha en ukentlig ende-til-ende-jobb som sender en ekte testmelding.

## Engangsoppsett for en ny app

Disse kan ikke ligge i repoet. Skriv dem i README under «Vedlikehold og varsling» og minn eieren på dem:
1. Standardbranch `main`.
2. github.com/settings/notifications → Actions: e-post for feilede workflows.
3. Coolify: API-token med bare _Deploy_, slå av automatisk deploy, testappen følger branchen `test`, varsler på, minnegrense på containeren.
4. Tailscale: `tag:ci`, grant til Coolify på `tcp:8000`, federated identity (subject med org-ID: `repo:Tidya-no@<org-id>/*:ref:refs/heads/*`).
5. Secrets: `TS_CLIENT_ID`, `TS_AUDIENCE`, `COOLIFY_URL`, `COOLIFY_TOKEN`, `PROD_APP_ID`, `TEST_APP_ID`.
6. Ekstern oppetidsmonitor på `/health`.

## Når du bygger noe nytt

1. Les `AGENTS.md` og `README.md` i begge appene, og velg den som ligner mest som utgangspunkt.
2. Behold strukturen, ikke abstraher ut et felles bibliotek før en tredje app viser hva som faktisk er felles.
3. Dokumentasjonen skal ikke gli fra koden: README (oppsett, miljøvariabler, vedlikehold), `AGENTS.md` (regler og hvorfor). Etter en runde med endringer, les dem mot koden.
4. Ingen sikkerhetsregel over løsnes for å få noe til å virke. Si fra til eieren i stedet.
