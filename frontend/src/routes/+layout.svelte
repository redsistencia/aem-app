<script lang="ts">
	import { QueryClientProvider } from '@tanstack/svelte-query';
	import { queryClient } from '$lib/query/client';
	import { theme } from '$lib/stores/theme';

    import favicon from '$lib/assets/favicon.ico';

    import '$lib/styles/theme.css';
    import '$lib/styles/tailwind.css';

    import Nav from '$lib/components/Nav.svelte';
    import Footer from '$lib/components/Footer.svelte';
</script>

<svelte:head>
	<title>Redsistencia</title>
    <link rel="icon" href={favicon} />
</svelte:head>

<QueryClientProvider client={queryClient}>
	<div class="app-layout">
		<Nav />
		<main class="main">
			<slot />
		</main>
		<Footer />
	</div>
</QueryClientProvider>

<style>
	.app-layout {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.main {
		flex: 1;
	}
</style>
