(() => {
	const root = document.documentElement
	const icon = document.getElementById('themeIcon')
	const label = document.getElementById('themeLabel')
	const storageKey = 'tidya-guide-theme'
	const prefersLight = window.matchMedia('(prefers-color-scheme: light)')

	const readSaved = () => {
		try { return localStorage.getItem(storageKey) } catch { return null }
	}

	const currentTheme = () => root.getAttribute('data-theme') ?? (prefersLight.matches ? 'light' : 'dark')

	const render = () => {
		const isDark = currentTheme() === 'dark'
		icon.textContent = isDark ? '☀️' : '🌙'
		label.textContent = isDark ? 'Lys modus' : 'Mørk modus'
	}

	const saved = readSaved()
	if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved)
	prefersLight.addEventListener('change', render)
	render()

	window.toggleTheme = () => {
		const next = currentTheme() === 'dark' ? 'light' : 'dark'
		root.setAttribute('data-theme', next)
		try { localStorage.setItem(storageKey, next) } catch { /* ignorer */ }
		render()
	}
})()
