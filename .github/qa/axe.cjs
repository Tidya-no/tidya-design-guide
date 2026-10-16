// Kjører axe-core mot index.html i mørk og lys modus, på smal og bred skjerm,
// også med dialogen åpen. Feiler (exit 1) ved brudd eller JS-feil.
const { chromium } = require('playwright')
const fs = require('fs')
const path = require('path')

const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8')
const url = 'file://' + path.resolve('index.html')
const tags = ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']

;(async () => {
	// Runneren har Chrome ferdig installert. Lokalt kan CHROME_PATH peke på en annen.
	const browser = await chromium.launch(
		process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: 'chrome' }
	)
	let failures = 0
	for (const width of [320, 1100]) {
		for (const colorScheme of ['dark', 'light']) {
			const context = await browser.newContext({ colorScheme, viewport: { width, height: 900 } })
			const page = await context.newPage()
			const errors = []
			page.on('pageerror', (e) => errors.push(e.message))
			await page.goto(url)
			await page.waitForLoadState('networkidle')
			for (const state of ['lukket dialog', 'åpen dialog']) {
				if (state === 'åpen dialog') await page.click('text=Åpne dialog')
				await page.evaluate(axeSource)
				const result = await page.evaluate((t) => axe.run(document, { runOnly: { type: 'tag', values: t } }), tags)
				const label = `${width}px ${colorScheme}, ${state}`
				if (result.violations.length === 0) console.log(`ok   ${label}`)
				for (const v of result.violations) {
					failures++
					console.log(`FEIL ${label}: ${v.id} (${v.nodes.length}) ${v.help}`)
					v.nodes.slice(0, 3).forEach((n) => console.log(`       ${n.target.join(' ')}`))
				}
			}
			for (const e of errors) { failures++; console.log(`FEIL JS-feil: ${e}`) }
			await context.close()
		}
	}
	await browser.close()
	if (failures) { console.log(`\n${failures} feil`); process.exit(1) }
	console.log('\nAlle axe-sjekker bestått')
})()
