<script lang="ts">
	import { page } from '$app/stores';
	import LinkButton from '$lib/components/ui/Link-button.svelte';
</script>

<div class="container mx-auto px-4 py-16">
	<div class="mx-auto max-w-md text-center space-y-6">
		<h1 class="text-4xl font-semibold tracking-tight">
			{#if $page.status === 404}
				Página no encontrada
			{:else}
				Ocurrió un error
			{/if}
		</h1>

		<p class="text-muted-foreground">
			{#if $page.status === 404}
				El enlace que intentaste visitar no existe o aún no está disponible.
			{:else}
				Algo salió mal. Por favor, intentá nuevamente más tarde.
			{/if}
		</p>

		<div class="flex justify-center gap-3 pt-4">
			<LinkButton href="/">Volver al inicio</LinkButton>
			<LinkButton href="/asociarse" variant="outline">Asociarse</LinkButton>
		</div>
	</div>
</div>
