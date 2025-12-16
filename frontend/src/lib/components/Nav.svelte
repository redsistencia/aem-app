<script lang="ts">
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
</script>

<nav class="nav">
	<div class="container">
		<a href="/" class="logo">Argentinxs en Mallorca</a>

		<div class="right">
			<ul class="links">
				<li><a href="/asociarse">Asociarse</a></li>
				<li><a href="/login">Admin</a></li>
			</ul>

			<ThemeToggle />
		</div>
	</div>
</nav>

<style>
	.nav {
		background-color: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
	}

	.container {
		max-width: 1024px;
		margin: 0 auto;
		padding: var(--space-md);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.logo {
		font-weight: 600;
		color: var(--color-text);
	}

	.links {
		list-style: none;
		display: flex;
		gap: var(--space-md);
		margin: 0;
		padding: 0;
	}

	.links a {
		color: var(--color-text-muted);
	}

	.links a:hover {
		color: var(--color-primary);
	}

    .right {
        display: flex;
        align-items: center;
        gap: var(--space-md);
    }
</style>
