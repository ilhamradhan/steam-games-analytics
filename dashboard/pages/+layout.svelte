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
	<slot slot="content" />
</EvidenceDefaultLayout>

<style>
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
