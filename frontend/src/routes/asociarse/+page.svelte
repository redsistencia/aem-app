<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="mx-auto max-w-xl space-y-8">
		<header class="space-y-2">
			<h1 class="text-3xl font-semibold tracking-tight">
				Asociate
			</h1>

			<p class="text-muted-foreground">
				Sumate a Argentinxs en Mallorca y ayudanos a sostener este espacio
				colectivo de acompañamiento y resistencia.
			</p>
		</header>

		<form class="space-y-6">
			<!-- Placeholder de campos (próximo paso) -->
			<div class="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground">
				Formulario en construcción
			</div>

			<div class="flex gap-3">
				<Button type="submit">
					Asociarse
				</Button>

				<Button type="button" variant="outline">
					Cancelar
				</Button>
			</div>
		</form>
	</div>
</div>
