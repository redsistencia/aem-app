<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { activities } from '$lib/mocks/activities';
	import Button from '$lib/components/ui/Button.svelte';

	$: slug = $page.params.slug;
	$: activity = activities.find((a) => a.slug === slug);

	onMount(() => {
		// Si existe el embed de Instagram, forzamos el render
		if (window.instgrm) {
			window.instgrm.Embeds.process();
		}
	});
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	{#if activity}
		<div class="flex flex-col gap-6 max-w-2xl">
			<h1 class="text-2xl font-semibold">{activity.title}</h1>

			<p class="text-sm text-muted-foreground">
				{new Date(activity.date).toLocaleDateString()}
			</p>
            
			{#if activity.instagramUrl}
				<!-- Instagram Embed -->
				<blockquote
					class="instagram-media"
					data-instgrm-permalink={activity.instagramUrl}
					data-instgrm-version="14"
					style="width:100%; margin:0 auto;"
				></blockquote>
			{/if}

			<p>{activity.description}</p>

			<div class="flex gap-3">
				<Button variant="outline">
					<a href="/admin/actividades">
						Volver
					</a>
				</Button>
			</div>
		</div>
	{:else}
		<p class="text-muted-foreground">Actividad no encontrada</p>
	{/if}
</div>

<svelte:head>
	<script async src="https://www.instagram.com/embed.js"></script>
</svelte:head>
