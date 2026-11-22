<script lang="ts">
	import type { PageData } from './$types';
	import LinkButton from '$lib/components/ui/Link-button.svelte';
	export let data: PageData;
</script>

<svelte:head><title>{data.activity.title} · Redsistencia</title></svelte:head>
<div class="container mx-auto px-4 py-24 sm:px-6 lg:px-24">
	<article class="max-w-2xl space-y-6">
		<h1 class="text-2xl font-semibold">{data.activity.title}</h1>
		<p class="text-sm text-muted-foreground">{data.activity.date}</p>
		{#if data.activity.image_url}<img
				src={data.activity.image_url}
				alt={data.activity.title}
				class="w-full rounded-md"
			/>{/if}
		<p class="whitespace-pre-wrap">{data.activity.description}</p>
		<LinkButton href="/actividades" variant="outline">Volver</LinkButton>
	</article>
</div>
