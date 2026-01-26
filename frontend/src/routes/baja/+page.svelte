<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	export let form;
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="mx-auto max-w-xl space-y-8">
		<header class="space-y-2">
			<h1 class="text-3xl font-semibold tracking-tight">
				Baja voluntaria
			</h1>
			<p class="text-muted-foreground text-sm">
				Podés solicitar la baja de la asociación ingresando tu email. 
				Esto también implica dejar de recibir comunicaciones y newsletters.
			</p>
		</header>

		{#if form?.success}
			<div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-800">
				Ya te diste de baja. Gracias por haber sido parte 💚
			</div>
		{/if}

		{#if form?.error}
			<div class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
				{form.error}
			</div>
		{/if}

		<form method="POST" class="space-y-6">
			<div class="space-y-4">
				<div class="space-y-1">
					<label for="email" class="text-sm font-medium">
						Email
					</label>
					<input
						id="email"
						name="email"
						type="email"
						required
						maxlength="150"
						autocomplete="email"
						placeholder="tu@email.com"
						class="w-full rounded-md border px-3 py-2 text-sm"
					/>
				</div>

                <div class="space-y-1">
                    <label for="document_id" class="text-sm font-medium">
                        DNI / NIE / Pasaporte
                    </label>
                    <input
                        id="document_id"
                        name="document_id"
                        type="text"
                        required
                        pattern="[A-Za-z0-9]+"
                        title="Solo letras y números"
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>
			</div>

			<div class="flex gap-3">
				<Button type="submit">
					Darse de baja
				</Button>

				<a href="/" class="inline-flex">
					<Button type="button" variant="outline">
						Cancelar
					</Button>
				</a>
			</div>
		</form>
	</div>
</div>
