<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import { api, errorMessage } from '$lib/api/client';
	import LinkButton from '$lib/components/ui/Link-button.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import type { Activity } from '$lib/types/activity';

	let activities: Activity[] = [];
	let loading = true;
	let error = '';
	let pending = false;
	let activityToDelete: Activity | null = null;
	onMount(async () => {
		try {
			activities = await api<Activity[]>('/admin/activities/', {}, true);
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			loading = false;
		}
	});

	async function confirmDelete() {
		if (!activityToDelete || pending) return;
		pending = true;
		error = '';
		const id = activityToDelete.id;
		try {
			await api(`/admin/activities/${id}`, { method: 'DELETE' }, true);
			activities = activities.filter((activity) => activity.id !== id);
			activityToDelete = null;
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			pending = false;
		}
	}
</script>

<div class="container mx-auto space-y-6 px-4 py-24 sm:px-6 lg:px-24">
	<h1 class="text-2xl font-semibold">Actividades</h1>
	<LinkButton href="/admin/actividades/nueva">Nueva actividad</LinkButton>
	{#if error}<p role="alert">{error}</p>{/if}
	{#if loading}<p>Cargando…</p>
	{:else}
		<div class="overflow-x-auto rounded-md border">
			<table class="w-full text-left text-sm">
				<thead
					><tr
						><th class="p-4">Fecha</th><th>Título</th><th>Newsletter enviado</th><th>Acciones</th
						></tr
					></thead
				>
				<tbody>
					{#each activities as activity (activity.id)}
						<tr class="border-t">
							<td class="p-4">{activity.date}</td>
							<td
								><a href={resolve('/actividades/[slug]', { slug: activity.slug })}
									>{activity.title}</a
								></td
							>
							<td>{activity.sent ? 'Sí' : 'No'}</td>
							<td class="flex gap-3 p-4">
								<LinkButton href={`/admin/actividades/${activity.slug}`} variant="outline" size="sm"
									>Editar</LinkButton
								>
								<Button variant="outline" size="sm" on:click={() => (activityToDelete = activity)}
									>Eliminar</Button
								>
							</td>
						</tr>
					{:else}<tr><td colspan="4" class="p-4">Sin actividades</td></tr>{/each}
				</tbody>
			</table>
		</div>
	{/if}
	{#if activityToDelete}
		<section class="space-y-4 rounded-md border p-6" aria-label="Confirmar eliminación">
			<p>¿Querés eliminar «{activityToDelete.title}»? Esta acción no se puede deshacer.</p>
			<Button disabled={pending} on:click={confirmDelete}>Eliminar</Button>
			<Button variant="outline" disabled={pending} on:click={() => (activityToDelete = null)}
				>Cancelar</Button
			>
		</section>
	{/if}
</div>
