// Header: skjules/vises ikke, men får tåkete bakgrunn ved scroll, mobilmeny og temabryter.
// Markup og klasser: se «Header» i DESIGN.md. Ingen avhengigheter. Kopier filen inn i appen.
(() => {
	const root = document.documentElement
	const header = document.querySelector('.site-header')
	if (!header) return
	// Uten JS vises menyen som vanlige lenker også på smal skjerm
	header.setAttribute('data-js', '')

	const onScroll = () => header.toggleAttribute('data-scrolled', window.scrollY > 24)
	window.addEventListener('scroll', onScroll, { passive: true })
	onScroll()

	const navToggle = header.querySelector('[data-nav-toggle]')
	const nav = header.querySelector('.site-nav')
	const setOpen = (open) => {
		nav.toggleAttribute('data-open', open)
		navToggle.setAttribute('aria-expanded', String(open))
		navToggle.setAttribute('aria-label', open ? 'Lukk meny' : 'Åpne meny')
	}
	navToggle.addEventListener('click', () => setOpen(!nav.hasAttribute('data-open')))
	nav.addEventListener('click', (e) => { if (e.target.closest('a, button')) setOpen(false) })
	document.addEventListener('click', (e) => { if (!header.contains(e.target)) setOpen(false) })
	document.addEventListener('keydown', (e) => {
		if (e.key === 'Escape' && nav.hasAttribute('data-open')) { setOpen(false); navToggle.focus() }
	})
	window.matchMedia('(min-width: 721px)').addEventListener('change', (e) => { if (e.matches) setOpen(false) })

	// Tema: valget huskes, ellers følger siden OS (mørk når OS ikke har preferanse)
	const themeToggle = header.querySelector('[data-theme-toggle]')
	const storageKey = themeToggle.dataset.themeKey || 'tidya-theme'
	const prefersLight = window.matchMedia('(prefers-color-scheme: light)')
	const isDark = () => {
		const chosen = root.getAttribute('data-theme')
		return chosen ? chosen === 'dark' : !prefersLight.matches
	}
	const sync = () => {
		themeToggle.setAttribute('aria-label', isDark() ? 'Bytt til lys modus' : 'Bytt til mørk modus')
		// theme-color følger valgt modus, ikke bare OS
		const bg = getComputedStyle(root).getPropertyValue('--color-bg').trim()
		document.querySelectorAll('meta[name="theme-color"]').forEach((m) => {
			m.removeAttribute('media')
			m.setAttribute('content', bg)
		})
		window.dispatchEvent(new Event('tidya:themechange'))
	}
	sync()
	prefersLight.addEventListener('change', () => { if (!root.hasAttribute('data-theme')) sync() })
	themeToggle.addEventListener('click', () => {
		const next = isDark() ? 'light' : 'dark'
		root.setAttribute('data-theme', next)
		try { localStorage.setItem(storageKey, next) } catch { /* ignorer */ }
		sync()
	})
})()
