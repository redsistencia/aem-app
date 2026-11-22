<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import { api, errorMessage } from '$lib/api/client';
	import type { Activity } from '$lib/types/activity';

	let activities: Activity[] = [];
	let loading = true;
	let error = '';
	onMount(async () => {
		try {
			activities = await api<Activity[]>('/activities/');
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			loading = false;
		}
	});
</script>

<div class="container mx-auto px-4 py-24 sm:px-6 lg:px-24">
	<header class="mb-12 max-w-2xl space-y-2">
		<h1 class="text-3xl font-semibold">Actividades</h1>
		<p>Novedades, encuentros y acciones de Redsistencia</p>
	</header>
	{#if error}<p role="alert">{error}</p>
	{:else if loading}<p>Cargando actividades…</p>
	{:else if activities.length === 0}<p>Todavía no hay actividades publicadas.</p>
	{:else}
		<div class="grid max-w-3xl gap-8">
			{#each activities as activity (activity.id)}
				<article class="space-y-4 border-b pb-8">
					<h2 class="text-xl font-semibold">
						<a href={resolve('/actividades/[slug]', { slug: activity.slug })}>{activity.title}</a>
					</h2>
					<p class="text-sm text-muted-foreground">{activity.date}</p>
					<p>{activity.description.slice(0, 180)}{activity.description.length > 180 ? '…' : ''}</p>
					<a
						href={resolve('/actividades/[slug]', { slug: activity.slug })}
						class="text-sm font-medium hover:underline">Leer más →</a
					>
				</article>
			{/each}
		</div>
	{/if}
</div>
