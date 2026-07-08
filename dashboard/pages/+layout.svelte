<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { onMount, afterUpdate } from 'svelte';
	import { browser } from '$app/environment';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;

	function normalizePath(pathname) {
		const normalized = decodeURIComponent(pathname).replace(/\/+$/, '');
		return normalized === '' ? '/' : normalized;
	}

	function syncSidebarCurrent() {
		if (!browser) return;

		const currentPath = normalizePath(window.location.pathname);
		const sidebarLinks = document.querySelectorAll('aside a[href], #mobileScrollable a[href]');

		sidebarLinks.forEach((link) => {
			const href = normalizePath(new URL(link.href, window.location.origin).pathname);
			const isCurrent = href === currentPath;
			link.toggleAttribute('data-sidebar-current', isCurrent);
			if (isCurrent) {
				link.setAttribute('aria-current', 'page');
			} else {
				link.removeAttribute('aria-current');
			}

			const wrapper = link.parentElement;
			if (wrapper?.classList.contains('relative')) {
				wrapper.toggleAttribute('data-sidebar-current-wrapper', isCurrent);
			}
		});
	}

	onMount(() => {
		if (!browser) return;

		const observer = new MutationObserver(() => syncSidebarCurrent());
		observer.observe(document.body, { childList: true, subtree: true });
		requestAnimationFrame(syncSidebarCurrent);

		return () => observer.disconnect();
	});

	afterUpdate(() => {
		if (browser) requestAnimationFrame(syncSidebarCurrent);
	});
</script>

<EvidenceDefaultLayout {data}>
	<div slot="content" class="dashboard-shell">
		<slot />
	</div>
</EvidenceDefaultLayout>

<style>
	:global(.dashboard-shell) {
		padding-bottom: 2rem;
	}

	:global(.dashboard-shell > :first-child) {
		margin-top: 0.35rem;
	}

	:global(.dashboard-shell h1) {
		margin: 0 0 0.8rem;
		font-size: clamp(2.4rem, 4.6vw, 3.5rem);
		line-height: 0.98;
		letter-spacing: -0.03em;
		font-weight: 780;
		color: #f4f6ff;
	}

	:global(.dashboard-shell h2) {
		margin-top: 2.75rem;
		margin-bottom: 0.7rem;
		padding-top: 0.95rem;
		border-top: 1px solid rgba(138, 173, 244, 0.16);
		font-size: 1.08rem;
		line-height: 1.2;
		letter-spacing: 0.01em;
		font-weight: 700;
		color: #edf1ff;
	}

	:global(.dashboard-shell p) {
		line-height: 1.65;
		color: #b8c0e0;
	}

	:global(.dashboard-shell .page-lead) {
		max-width: 62rem;
		margin: 0 0 1.15rem;
		font-size: 1.07rem;
		line-height: 1.75;
		color: #cdd5ee;
	}

	:global(.dashboard-shell .section-lead) {
		max-width: 60rem;
		margin: 0 0 1.05rem;
		font-size: 0.95rem;
		color: #aeb8d6;
	}

	:global(.dashboard-shell .page-header) {
		margin: 0 0 2rem;
		padding: 0 0 1.35rem;
		border-bottom: 1px solid rgba(138, 173, 244, 0.14);
	}

	:global(.dashboard-shell .page-kicker) {
		margin-bottom: 0.85rem;
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: #8aadf4;
	}

	:global(.dashboard-shell .page-meta-row) {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
		gap: 0.9rem;
		margin-top: 1.4rem;
	}

	:global(.dashboard-shell .page-meta-card) {
		padding: 0.9rem 0.95rem;
		border: 1px solid rgba(138, 173, 244, 0.14);
		border-radius: 5px;
		background: linear-gradient(180deg, rgba(54, 58, 79, 0.46), rgba(30, 32, 48, 0.68));
		box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
	}

	:global(.dashboard-shell .page-meta-label) {
		margin-bottom: 0.35rem;
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #91d7e3;
	}

	:global(.dashboard-shell .page-meta-copy) {
		font-size: 0.9rem;
		line-height: 1.5;
		color: #d7def7;
	}

	:global(.dashboard-shell blockquote) {
		margin: 1rem 0 1.45rem;
		padding: 0.1rem 0 0.1rem 0.95rem;
		border-left: 2px solid rgba(138, 173, 244, 0.3);
		color: #aeb8d6;
	}

	:global(.dashboard-shell blockquote p) {
		color: #aeb8d6;
	}

	:global(.dashboard-shell strong) {
		color: #e8ecff;
	}

	:global(.dashboard-shell code) {
		color: #f5bde6;
	}

	:global(.dashboard-shell .hero-strip) {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
		gap: 0.9rem;
		margin: 1.4rem 0 2rem;
	}

	:global(.dashboard-shell .hero-strip-card) {
		padding: 0.95rem 1rem;
		border: 1px solid rgba(138, 173, 244, 0.14);
		border-radius: 5px;
		background: linear-gradient(180deg, rgba(54, 58, 79, 0.42), rgba(36, 39, 58, 0.22));
	}

	:global(.dashboard-shell .hero-strip-label) {
		margin-bottom: 0.35rem;
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #8aadf4;
	}

	:global(.dashboard-shell .hero-strip-copy) {
		font-size: 0.9rem;
		line-height: 1.45;
		color: #cad3f5;
	}

	:global(.dashboard-shell .hero-feature) {
		display: grid;
		grid-template-columns: minmax(0, 1.6fr) minmax(260px, 0.9fr);
		gap: 1.2rem;
		margin: 1.6rem 0 2rem;
	}

	:global(.dashboard-shell .homepage-hero) {
		position: relative;
		overflow: hidden;
		padding: 1.35rem 1.4rem 1.45rem;
		border: 1px solid rgba(189, 147, 249, 0.16);
		border-radius: 5px;
		background:
			radial-gradient(circle at top right, rgba(189, 147, 249, 0.16), transparent 32%),
			radial-gradient(circle at bottom left, rgba(139, 233, 253, 0.12), transparent 28%),
			linear-gradient(180deg, rgba(54, 58, 82, 0.9), rgba(36, 39, 58, 0.96));
		box-shadow:
			0 18px 50px rgba(0, 0, 0, 0.22),
			inset 0 1px 0 rgba(255, 255, 255, 0.04);
	}

	:global(.dashboard-shell .homepage-hero-grid) {
		display: grid;
		grid-template-columns: minmax(0, 1.7fr) minmax(260px, 0.95fr);
		gap: 1.2rem;
		align-items: stretch;
	}

	:global(.dashboard-shell .homepage-hero-copy) {
		position: relative;
		z-index: 1;
	}

	:global(.dashboard-shell .homepage-hero-copy h1) {
		max-width: 12ch;
		margin-bottom: 0.9rem;
	}

	:global(.dashboard-shell .homepage-hero-copy .page-lead) {
		max-width: 58rem;
		margin-bottom: 0.85rem;
	}

	:global(.dashboard-shell .homepage-hero-copy .section-lead) {
		max-width: 52rem;
		color: #b4bdd9;
	}

	:global(.dashboard-shell .homepage-side-stack) {
		display: grid;
		gap: 0.9rem;
	}

	:global(.dashboard-shell .homepage-side-card) {
		padding: 0.95rem 1rem;
		border: 1px solid rgba(145, 215, 227, 0.14);
		border-radius: 5px;
		background: rgba(24, 26, 40, 0.46);
		backdrop-filter: blur(8px);
	}

	:global(.dashboard-shell .homepage-side-card:nth-child(2)) {
		border-color: rgba(245, 169, 127, 0.14);
	}

	:global(.dashboard-shell .homepage-side-card strong) {
		display: block;
		margin-bottom: 0.25rem;
		font-size: 0.74rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #91d7e3;
	}

	:global(.dashboard-shell .homepage-side-card p) {
		margin: 0;
		font-size: 0.92rem;
		line-height: 1.5;
		color: #d0d7f0;
	}

	:global(.dashboard-shell .stats-grid) {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 0.95rem;
	}

	:global(.dashboard-shell .stat-card) {
		position: relative;
		overflow: hidden;
		padding: 1rem 1rem 1.05rem;
		border: 1px solid rgba(138, 173, 244, 0.14);
		border-radius: 5px;
		background:
			radial-gradient(circle at top right, rgba(189, 147, 249, 0.08), transparent 34%),
			linear-gradient(180deg, rgba(54, 58, 79, 0.52), rgba(30, 32, 48, 0.74));
		box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
	}

	:global(.dashboard-shell .stat-card:nth-child(2)) {
		border-color: rgba(145, 215, 227, 0.14);
	}

	:global(.dashboard-shell .stat-card:nth-child(3)) {
		border-color: rgba(166, 218, 149, 0.14);
	}

	:global(.dashboard-shell .stat-card:nth-child(4)) {
		border-color: rgba(245, 169, 127, 0.14);
	}

	:global(.dashboard-shell .hero-feature-main),
	:global(.dashboard-shell .hero-feature-side) {
		padding: 1.15rem 1.2rem 1.25rem;
		border: 1px solid rgba(138, 173, 244, 0.14);
		border-radius: 5px;
		background: linear-gradient(180deg, rgba(54, 58, 79, 0.5), rgba(30, 32, 48, 0.72));
	}

	:global(.dashboard-shell .hero-feature-side) {
		border-color: rgba(198, 160, 246, 0.14);
	}

	:global(.dashboard-shell .hero-feature-label) {
		margin-bottom: 0.5rem;
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #8aadf4;
	}

	:global(.dashboard-shell .hero-feature-main h2),
	:global(.dashboard-shell .hero-feature-side h2) {
		margin: 0 0 0.5rem;
		padding-top: 0;
		border-top: 0;
		font-size: 1.25rem;
		letter-spacing: -0.02em;
	}

	:global(.dashboard-shell .hero-feature-main p),
	:global(.dashboard-shell .hero-feature-side p) {
		margin: 0;
		color: #c9d1eb;
	}

	:global(.dashboard-shell .hero-side-list) {
		margin: 0.85rem 0 0;
		padding: 0;
		list-style: none;
	}

	:global(.dashboard-shell .hero-side-list li) {
		padding: 0.6rem 0;
		border-top: 1px solid rgba(138, 173, 244, 0.1);
		font-size: 0.9rem;
		line-height: 1.45;
		color: #c9d1eb;
	}

	:global(.dashboard-shell .hero-side-list li:first-child) {
		border-top: 0;
		padding-top: 0;
	}

	:global(.dashboard-shell .hero-side-list strong) {
		display: block;
		margin-bottom: 0.18rem;
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: #91d7e3;
	}

	:global(.dashboard-shell .panel) {
		margin: 1.25rem 0 2rem;
		padding: 1.15rem 1.2rem 1.25rem;
		border-radius: 5px;
		border: 1px solid rgba(138, 173, 244, 0.12);
		background: linear-gradient(180deg, rgba(46, 50, 72, 0.46), rgba(31, 34, 51, 0.65));
		box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025);
	}

	:global(.dashboard-shell .panel-grid) {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: 1.5rem;
	}

	:global(.dashboard-shell .panel-cool) {
		border-color: rgba(145, 215, 227, 0.14);
	}

	:global(.dashboard-shell .panel-warm) {
		border-color: rgba(245, 169, 127, 0.14);
	}

	:global(.dashboard-shell .panel-accent) {
		border-color: rgba(198, 160, 246, 0.14);
	}

	:global(.dashboard-shell .panel-soft) {
		background: linear-gradient(180deg, rgba(42, 45, 64, 0.4), rgba(31, 34, 51, 0.56));
	}

	:global(.dashboard-shell .section-kicker) {
		margin-bottom: 0.45rem;
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #8aadf4;
	}

	:global(.dashboard-shell .section-stack) {
		margin-top: 1rem;
	}

	@media (max-width: 900px) {
		:global(.dashboard-shell .hero-feature) {
			grid-template-columns: 1fr;
		}

		:global(.dashboard-shell .homepage-hero-grid) {
			grid-template-columns: 1fr;
		}
	}

	:global(aside a[data-sidebar-current='true']),
	:global(#mobileScrollable a[data-sidebar-current='true']) {
		color: hsl(var(--twc-primary)) !important;
		font-weight: 700;
		text-decoration: underline;
		text-underline-offset: 0.18em;
		background: rgba(138, 173, 244, 0.1);
		border-radius: 5px;
		padding-left: 0.45rem;
		padding-right: 0.45rem;
	}

	:global(aside [data-sidebar-current-wrapper='true']),
	:global(#mobileScrollable [data-sidebar-current-wrapper='true']) {
		border-color: hsl(var(--twc-primary)) !important;
	}
</style>
