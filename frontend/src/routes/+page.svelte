<script lang="ts">
	import LinkButton from '$lib/components/ui/Link-button.svelte';
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="max-w-2xl space-y-6">
		<h1 class="text-4xl font-semibold tracking-tight">
			Argentinxs en Resistencia en Baleares 🇦🇷
		</h1>

		<p class="text-muted-foreground text-lg">
			Colectivo migrante que busca resistir y sostenerse en medio de la crisis
			que atraviesa la Argentina en la actualidad 🧉💚✊
		</p>

		<div class="flex gap-3 pt-4">
			<LinkButton href="/asociarse">Asociarse</LinkButton>
			<LinkButton href="/actividades" variant="outline">Ver actividades</LinkButton>
		</div>
	</div>
</div>
