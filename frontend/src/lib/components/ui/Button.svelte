<script lang="ts">
	import { cn } from '$lib/utils';
	import { createEventDispatcher } from 'svelte';

	export let variant: 'default' | 'outline' | 'ghost' = 'default';
	export let size: 'sm' | 'md' | 'lg' | 'icon' = 'md';
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let disabled = false;
	export let className = '';

	const dispatch = createEventDispatcher<{ click: MouseEvent }>();

	const variants = {
		default: 'bg-primary text-primary-foreground hover:bg-primary/90',
		outline: 'border border-border bg-background hover:bg-muted',
		ghost: 'hover:bg-muted'
	};

	const sizes = {
		sm: 'h-8 px-3 text-sm',
		md: 'h-10 px-4',
		lg: 'h-12 px-6 text-lg',
		icon: 'h-10 w-10 p-0'
	};

	const base =
		'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50';
</script>

<button
	type={type}
	disabled={disabled}
	class={cn(base, variants[variant], sizes[size], className)}
	on:click={(e) => dispatch('click', e)}
>
	<slot />
</button>
