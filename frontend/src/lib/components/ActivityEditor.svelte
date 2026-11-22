<script lang="ts">
	import { resolve } from '$app/paths';
	import { goto } from '$app/navigation';
	import { api, errorMessage } from '$lib/api/client';
	import Button from '$lib/components/ui/Button.svelte';
	import LinkButton from '$lib/components/ui/Link-button.svelte';
	import type { Activity } from '$lib/types/activity';

	export let activity: Activity | null = null;
	let title = activity?.title ?? '';
	let description = activity?.description ?? '';
	let date = activity?.date ?? '';
	let slug = activity?.slug ?? '';
	let imageUrl = activity?.image_url ?? '';
	let error = '';
	let pending = false;

	async function save() {
		if (pending) return;
		error = '';
		pending = true;
		const data = { title, description, date, slug, image_url: imageUrl || null };
		try {
			await api(
				activity ? `/admin/activities/${activity.id}` : '/admin/activities/',
				{
					method: activity ? 'PATCH' : 'POST',
					body: JSON.stringify(data)
				},
				true
			);
			await goto(resolve('/admin/actividades'));
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			pending = false;
		}
	}
</script>

<div class="container mx-auto max-w-2xl space-y-6 px-4 py-12">
	<h1 class="text-2xl font-semibold">{activity ? 'Editar actividad' : 'Nueva actividad'}</h1>
	{#if error}<p role="alert">{error}</p>{/if}
	<form class="space-y-4" on:submit|preventDefault={save}>
		<div>
			<label for="title">Título</label><input
				class="w-full rounded-md border p-2"
				id="title"
				bind:value={title}
				required
				maxlength="150"
			/>
		</div>
		<div>
			<label for="description">Descripción</label><textarea
				class="w-full rounded-md border p-2"
				id="description"
				bind:value={description}
				required
				maxlength="450"
			></textarea>
		</div>
		<div>
			<label for="date">Fecha</label><input
				class="w-full rounded-md border p-2"
				id="date"
				type="date"
				bind:value={date}
				required
			/>
		</div>
		<div>
			<label for="slug">Dirección de la actividad</label><input
				class="w-full rounded-md border p-2"
				id="slug"
				bind:value={slug}
				required
				maxlength="200"
				pattern="[a-z0-9]+(-[a-z0-9]+)*"
				title="Usá letras minúsculas, números y guiones"
			/>
		</div>
		<div>
			<label for="image">URL de la imagen (opcional)</label><input
				class="w-full rounded-md border p-2"
				id="image"
				type="url"
				bind:value={imageUrl}
			/>
		</div>
		<div class="flex gap-3">
			<Button type="submit" disabled={pending}>{pending ? 'Guardando…' : 'Guardar'}</Button
			><LinkButton href={resolve('/admin/actividades')} variant="outline">Cancelar</LinkButton>
		</div>
	</form>
</div>
