<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
</script>

<nav class="border-b bg-background">
	<div class="container mx-auto flex h-16 items-center justify-between px-4">
        <a href="/" class="flex items-center gap-3">
            <img
                src="/logo.png"
                alt="Redsistencia"
                class="h-8 w-auto"
            />
            <span class="text-lg font-semibold tracking-tight">
                Redsistencia
            </span>
        </a>
		<div class="flex items-center gap-4">
			<a
				href="/asociarse"
				class="text-sm text-muted-foreground hover:text-foreground transition-colors"
			>
				Asociarse
			</a>

			<a
				href="/login"
				class="text-sm text-muted-foreground hover:text-foreground transition-colors"
			>
				Admin
			</a>

			<ThemeToggle />
		</div>
	</div>
</nav>
