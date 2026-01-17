<script lang="ts">
	import { activities } from '$lib/mocks/activities';

	const sortedActivities = [...activities].sort(
		(a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
	);
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<header class="max-w-2xl space-y-2 mb-12">
		<h1 class="text-3xl font-semibold tracking-tight">
			Actividades
		</h1>
		<p class="text-muted-foreground">
			Novedades, encuentros y acciones de Redsistencia
		</p>
	</header>

	<div class="grid gap-8 max-w-3xl">
		{#each sortedActivities as activity}
			<article class="space-y-4 border-b pb-8">
                {#if activity.instagramUrl}
                    <!-- Instagram Embed -->
                    <blockquote
                        class="instagram-media"
                        data-instgrm-permalink={activity.instagramUrl}
                        data-instgrm-version="14"
                        style="width:100%; margin:0 auto;"
                    ></blockquote>
                {/if}

				<div class="space-y-1">
					<h2 class="text-xl font-semibold">
						<a
							href={`/actividades/${activity.slug}`}
							class="hover:underline"
						>
							{activity.title}
						</a>
					</h2>

					<p class="text-sm text-muted-foreground">
						{new Date(activity.date).toLocaleDateString()}
					</p>
				</div>

				<p class="text-sm text-muted-foreground">
					{activity.description.slice(0, 180)}…
				</p>

				<a
					href={`/actividades/${activity.slug}`}
					class="text-sm font-medium hover:underline"
				>
					Leer más →
				</a>
			</article>
		{/each}
	</div>
</div>
