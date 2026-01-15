<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	export let form; 
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="mx-auto max-w-xl space-y-8">
		<header class="space-y-2">
			<h1 class="text-3xl font-semibold tracking-tight">
				Asociate
			</h1>
		</header>
        
        {#if form?.success}
            <div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-800">
                ¡Gracias por asociarte! Te vamos a escribir pronto 💌
            </div>
        {/if}

        {#if form?.error}
            <div class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                {form.error}
            </div>
        {/if}

        <form method="POST" class="space-y-6">
            <div class="space-y-4">
                <!-- Nombre -->
                <div class="space-y-1">
                    <label for="name" class="text-sm font-medium">
                        Nombre o alias
                    </label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        required
                        maxlength="150"
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Apellido -->
                <div class="space-y-1">
                    <label for="lastname" class="text-sm font-medium">
                        Apellido/s
                    </label>
                    <input
                        id="lastname"
                        name="lastname"
                        type="text"
                        required
                        maxlength="150"
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Email -->
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
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Dirección -->
                <div class="space-y-1">
                    <label for="address" class="text-sm font-medium">
                        Dirección
                    </label>
                    <input
                        id="address"
                        name="address"
                        type="text"
                        required
                        maxlength="250"
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Nacionalidad -->
                <div class="space-y-1">
                    <label for="nationality" class="text-sm font-medium">
                        Nacionalidad
                    </label>
                    <input
                        id="nationality"
                        name="nationality"
                        type="text"
                        required
                        maxlength="250"
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Documento -->
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

                <!-- Teléfono -->
                <div class="space-y-1">
                    <label for="phone" class="text-sm font-medium">
                        Teléfono
                    </label>
                    <input
                        id="phone"
                        name="phone"
                        type="tel"
                        required
                        class="w-full rounded-md border px-3 py-2 text-sm"
                    />
                </div>

                <!-- Checkboxes legales -->
                <div class="space-y-3 pt-2">
                    <div class="flex items-start gap-2">
                        <input
                            id="privacy_policy"
                            name="privacy_policy"
                            type="checkbox"
                            required
                            class="mt-1"
                        />
                        <label for="privacy_policy" class="text-sm">
                            Acepto la política de privacidad
                        </label>
                    </div>

                    <div class="flex items-start gap-2">
                        <input
                            id="newsletter"
                            name="newsletter"
                            type="checkbox"
                            class="mt-1"
                        />
                        <label for="newsletter" class="text-sm">
                            Consiento recibir newsletters y comunicaciones
                        </label>
                    </div>
                </div>
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
