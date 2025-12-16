<script lang="ts">
    import favicon from '$lib/assets/favicon.svg';
    import '$lib/styles/theme.css';
    import '$lib/styles/base.css';
	import { theme } from '$lib/stores/theme';

    import Nav from '$lib/components/Nav.svelte';
    import Footer from '$lib/components/Footer.svelte';
</script>

<svelte:head>
    <link rel="icon" href={favicon} />
</svelte:head>

<div class="app-layout">
	<Nav />

	<main class="main">
		<slot />
	</main>

	<Footer />
</div>

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
