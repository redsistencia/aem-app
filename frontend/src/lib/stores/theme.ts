import { writable } from 'svelte/store';

export type Theme = 'light' | 'dark';

export const theme = writable<Theme>('light');

if (typeof window !== 'undefined') {
	const current = document.documentElement.getAttribute('data-theme') as Theme | null;
	if (current) {
		theme.set(current);
	}

	theme.subscribe((value) => {
		document.documentElement.setAttribute('data-theme', value);
		localStorage.setItem('theme', value);
	});
}

export function toggleTheme() {
	theme.update((t) => (t === 'dark' ? 'light' : 'dark'));
}
