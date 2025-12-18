<script lang="ts">
	import { page } from '$app/stores';
	import { activities } from '$lib/mocks/activities';
	import Button from '$lib/components/ui/Button.svelte';

	$: slug = $page.params.slug;
	$: activity = activities.find((a) => a.slug === slug);
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
{#if activity}
		<div class="flex flex-col gap-6 max-w-2xl">
			<h1 class="text-2xl font-semibold">{activity.title}</h1>

			<p class="text-sm text-muted-foreground">
				{new Date(activity.date).toLocaleDateString()}
			</p>

			{#if activity.imageUrl}
				<img
					src={activity.imageUrl}
					alt={activity.title}
					class="rounded-lg border max-h-[400px] object-cover"
				/>
			{/if}

			<p>{activity.description}</p>

			<div class="flex gap-3">
				<Button
					asChild
				>
					<a
						href={activity.activityUrl}
						target="_blank"
						rel="noopener noreferrer"
					>
						Abrir actividad
					</a>
				</Button>

				<Button
					variant="outline"
					asChild
				>
					<a href="/actividades">
						Volver
					</a>
				</Button>
			</div>
		</div>
	{:else}
		<p class="text-muted-foreground">Actividad no encontrada</p>
	{/if}
</div>
