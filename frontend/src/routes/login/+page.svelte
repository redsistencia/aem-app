<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="mx-auto max-w-xl space-y-8">
		<header class="space-y-2">
			<h1 class="text-3xl font-semibold tracking-tight">
				Login 
			</h1>
		</header>

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
                        autocomplete="email"
                        placeholder="admin@email.com"
                        class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                </div>

                <div class="space-y-1">
                    <label for="password" class="text-sm font-medium">
                        Password
                    </label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        autocomplete="current-password"
                        placeholder="••••••••"
                        class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                </div>
            </div>

            <div class="flex gap-3">
                <Button type="submit">
                    Ingresar
                </Button>

                <Button type="button" variant="outline">
                    Cancelar
                </Button>
            </div>
        </form>
	</div>
</div>
