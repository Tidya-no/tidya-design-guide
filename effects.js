// Valgfrie effekter for forsider: innkomst ved scroll, 3D-tilt og glød på kort, tellere og magnetiske knapper.
// Atferd styres av data-attributter (se «Effekter» i DESIGN.md). Ingen avhengigheter. Uten JS, eller med
// prefers-reduced-motion: reduce, vises alt som vanlig innhold.
(() => {
	const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
	const root = document.documentElement
	const all = (selector) => document.querySelectorAll(selector)

	// Innkomst ved scroll: det som allerede er synlig ved oppstart vises uten animasjon, resten skjules til det scrolles inn
	const reveals = all('[data-reveal]')
	if (reveals.length && !reduceMotion) {
		const inView = (el) => el.getBoundingClientRect().top < window.innerHeight * 0.9
		reveals.forEach((el) => { if (inView(el)) el.setAttribute('data-in', '') })
		root.setAttribute('data-effects', '')
		const observer = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) return
				entry.target.setAttribute('data-in', '')
				observer.unobserve(entry.target)
			})
		}, { threshold: 0.15 })
		reveals.forEach((el) => { if (!el.hasAttribute('data-in')) observer.observe(el) })
	}

	// Tellere: teksten i elementet er sluttverdien (uten JS og ved redusert bevegelse), og telles opp fra 0 når den scrolles inn
	if (!reduceMotion) {
		const counter = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (!entry.isIntersecting) return
				counter.unobserve(entry.target)
				const el = entry.target
				const target = Number(el.dataset.count)
				const start = performance.now()
				const tick = (now) => {
					const progress = Math.min((now - start) / 1400, 1)
					el.textContent = String(Math.round(target * (1 - Math.pow(1 - progress, 3))))
					if (progress < 1) requestAnimationFrame(tick)
				}
				requestAnimationFrame(tick)
			})
		}, { threshold: 0.6 })
		all('[data-count]').forEach((el) => { el.textContent = '0'; counter.observe(el) })
	}

	// Glød som følger pekeren, og lett 3D-tilt, på kort med data-tilt (legg inn <div class="card-glow"> i kortet)
	all('[data-tilt]').forEach((card) => {
		card.addEventListener('pointermove', (e) => {
			const r = card.getBoundingClientRect()
			const x = e.clientX - r.left
			const y = e.clientY - r.top
			card.style.setProperty('--mx', x + 'px')
			card.style.setProperty('--my', y + 'px')
			if (reduceMotion) return
			card.style.transform = `perspective(900px) rotateX(${(y / r.height - 0.5) * -5}deg) rotateY(${(x / r.width - 0.5) * 5}deg)`
		})
		card.addEventListener('pointerleave', () => { card.style.transform = '' })
	})

	// Magnetiske knapper: følger pekeren litt
	if (!reduceMotion) {
		all('[data-magnetic]').forEach((el) => {
			el.addEventListener('pointermove', (e) => {
				const r = el.getBoundingClientRect()
				el.style.transform = `translate(${(e.clientX - (r.left + r.width / 2)) * 0.18}px, ${(e.clientY - (r.top + r.height / 2)) * 0.28}px)`
			})
			el.addEventListener('pointerleave', () => { el.style.transform = '' })
		})
	}
})()
