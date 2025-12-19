<script lang="ts">
	import { Moon, Sun } from 'lucide-svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { theme, toggleTheme } from '$lib/stores/theme';
</script>

<Button
	variant="ghost"
	size="icon"
	aria-label="Cambiar tema"
	on:click={toggleTheme}
>
	{#if $theme === 'dark'}
		<Sun class="h-5 w-5" />
	{:else}
		<Moon class="h-5 w-5" />
	{/if}
</Button>
