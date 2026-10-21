// Henter html-blokken under «Eksempler» i DESIGN.md, setter den inn i en minimal side
// og kjører html-validate og axe (mørk/lys, alle dialoger åpnet én for én).
// Slik driver ikke eksemplene fra de ekte komponentene.
const { chromium } = require('playwright')
const { HtmlValidate } = require('html-validate')
const fs = require('fs')
const path = require('path')
const os = require('os')

const md = fs.readFileSync('DESIGN.md', 'utf8')
const section = md.split(/^### Eksempler/m)[1]
const block = section && section.match(/```html\n([\s\S]*?)```/)
if (!block) { console.log('FEIL fant ikke html-blokken under «Eksempler» i DESIGN.md'); process.exit(1) }

const root = process.cwd()
const html = `<!DOCTYPE html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eksempler</title>
<link rel="stylesheet" href="file://${root}/tokens.css">
<link rel="stylesheet" href="file://${root}/components.css">
</head>
<body>
<main style="padding-top: 5rem">
<h1 class="h1">Eksempler</h1>
${block[1]}
</main>
</body>
</html>
`
const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'eksempler-')), 'eksempler.html')
fs.writeFileSync(file, html)

const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8')
const tags = ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']

;(async () => {
	let failures = 0

	const config = JSON.parse(fs.readFileSync('.github/qa/htmlvalidate.json', 'utf8'))
	const report = await new HtmlValidate(config).validateString(html)
	if (report.valid) console.log('ok   html-validate')
	for (const r of report.results) for (const m of r.messages) {
		failures++
		console.log(`FEIL html-validate: ${m.ruleId} linje ${m.line}: ${m.message}`)
	}

	const browser = await chromium.launch(
		process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: 'chrome' }
	)
	for (const colorScheme of ['dark', 'light']) {
		const context = await browser.newContext({ colorScheme, viewport: { width: 375, height: 900 } })
		const page = await context.newPage()
		await page.goto('file://' + file)
		const dialogs = await page.$$eval('dialog', (d) => d.map((x) => x.id))
		for (const state of [null, ...dialogs]) {
			if (state) await page.evaluate((id) => document.getElementById(id).showModal(), state)
			await page.evaluate(axeSource)
			const result = await page.evaluate((t) => axe.run(document, { runOnly: { type: 'tag', values: t } }), tags)
			const label = `${colorScheme}, ${state ? 'dialog #' + state : 'ingen dialog'}`
			if (result.violations.length === 0) console.log(`ok   axe ${label}`)
			for (const v of result.violations) {
				failures++
				console.log(`FEIL axe ${label}: ${v.id} (${v.nodes.length}) ${v.help}`)
				v.nodes.slice(0, 3).forEach((n) => console.log(`       ${n.target.join(' ')}`))
			}
			if (state) await page.evaluate((id) => document.getElementById(id).close(), state)
		}
		await context.close()
	}
	await browser.close()
	if (failures) { console.log(`\n${failures} feil`); process.exit(1) }
	console.log('\nEksemplene i DESIGN.md er bestått')
})()
