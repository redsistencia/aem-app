<script lang="ts">
	import { resolve } from '$app/paths';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/Button.svelte';
	import { api, errorMessage, setToken } from '$lib/api/client';

	let error = '';
	let pending = false;
	async function submit(event: SubmitEvent) {
		if (pending) return;
		const data = new FormData(event.currentTarget as HTMLFormElement);
		error = '';
		pending = true;
		try {
			const result = await api<{ access_token: string }>('/admin/users/login', {
				method: 'POST',
				body: JSON.stringify(Object.fromEntries(data))
			});
			setToken(result.access_token);
			await goto(resolve('/admin/actividades'));
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			pending = false;
		}
	}
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="mx-auto max-w-xl space-y-8">
		<header class="space-y-2">
			<h1 class="text-3xl font-semibold tracking-tight">Login</h1>
		</header>

		{#if error}<p role="alert">{error}</p>{/if}

		<form on:submit|preventDefault={submit} class="space-y-6">
			<div class="space-y-4">
				<div class="space-y-1">
					<label for="email" class="text-sm font-medium"> Email </label>
					<input
						id="email"
						name="email"
						type="email"
						required
						autocomplete="email"
						placeholder="admin@email.com"
						class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
					/>
				</div>

				<div class="space-y-1">
					<label for="password" class="text-sm font-medium"> Password </label>
					<input
						id="password"
						name="password"
						type="password"
						required
						autocomplete="current-password"
						placeholder="••••••••"
						class="w-full rounded-md border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
					/>
				</div>
			</div>

			<div class="flex gap-3">
				<Button type="submit" disabled={pending}>Ingresar</Button>

				<a href={resolve('/')} class="inline-flex items-center px-4">Cancelar</a>
			</div>
		</form>
	</div>
</div>
