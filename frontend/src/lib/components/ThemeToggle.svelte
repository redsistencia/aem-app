<script lang="ts">
	import { theme } from '$lib/stores/theme';

	$: isDark = $theme === 'dark';

	function toggle() {
		theme.update((t) => (t === 'light' ? 'dark' : 'light'));
	}
</script>

<button
	on:click={toggle}
	aria-label="Cambiar tema"
	title="Cambiar tema"
>
	{#if isDark}
		☀️
	{:else}
		🌙
	{/if}
</button>

<style>
    button {
        background: none;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-sm);
        padding: var(--space-xs) var(--space-sm);
        cursor: pointer;
        color: var(--color-text);
    }

    button:hover {
        background-color: var(--color-bg-muted);
    }
</style>
