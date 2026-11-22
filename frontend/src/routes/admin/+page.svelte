<script lang="ts">
	import { onMount } from 'svelte';
	import { api, errorMessage } from '$lib/api/client';
	import DataTable, { type Column } from '$lib/components/ui/Data-table.svelte';

	type Subscriber = {
		id: number;
		name: string;
		lastname: string;
		email: string;
		active: boolean;
		newsletter: boolean;
		created_at: string;
	};
	let data: Subscriber[] = [];
	let error = '';
	let loading = true;
	const columns: Column<Subscriber>[] = [
		{ key: 'name', label: 'Nombre' },
		{ key: 'lastname', label: 'Apellido/s' },
		{ key: 'email', label: 'Email' },
		{ key: 'active', label: 'Activo' },
		{ key: 'newsletter', label: 'Newsletter' },
		{ key: 'created_at', label: 'Fecha' }
	];

	onMount(async () => {
		try {
			data = await api<Subscriber[]>('/admin/subscribers/', {}, true);
		} catch (cause) {
			error = errorMessage(cause);
		} finally {
			loading = false;
		}
	});
</script>

<div class="container mx-auto space-y-8 px-4 py-12">
	<h1 class="text-3xl font-semibold">Panel de administración</h1>
	<p>Listado de personas asociadas</p>
	{#if error}<p role="alert">{error}</p>
	{:else if loading}<p>Cargando…</p>
	{:else}<DataTable {columns} {data} />{/if}
</div>
