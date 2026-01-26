<script lang="ts">
	import { cn } from '$lib/utils';

	export let href: string;
	export let variant: 'default' | 'outline' | 'ghost' = 'default';
	export let size: 'sm' | 'md' | 'lg' | 'icon' = 'md';
	export let className = '';
	export let target: string | undefined = undefined;
	export let rel: string | undefined = undefined;

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
		'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';
</script>

<a
	href={href}
	target={target}
	rel={rel}
	class={cn(base, variants[variant], sizes[size], className)}
>
	<slot />
</a>
