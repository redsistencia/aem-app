<script lang="ts">
	import { goto } from '$app/navigation';
	import DataTable from '$lib/components/ui/Data-table.svelte';

	import { activities } from '$lib/mocks/activities';
	import { activityColumns } from './columns';
	import type { Activity } from '$lib/types/activity';

	function handleEdit(slug: string) {
		goto(`/admin/actividades/${slug}/edit`);
	}

	let showDeleteModal = false;
	let activityToDelete: string | null = null;

	function requestDelete(slug: string) {
		activityToDelete = slug;
		showDeleteModal = true;
	}

	function cancelDelete() {
		showDeleteModal = false;
		activityToDelete = null;
	}

	function confirmDelete() {
		if (!activityToDelete) return;

		console.log('Eliminar actividad:', activityToDelete);
		// luego:
		// await fetch(`/admin/actividades/${activityToDelete}`, { method: 'DELETE' });

		cancelDelete();
	}

	function handleTableClick(event: MouseEvent) {
		const target = event.target as HTMLElement;
		const action = target.getAttribute('data-action');
		const slug = target.getAttribute('data-slug');

		if (!action || !slug) return;

		if (action === 'edit') {
			handleEdit(slug);
		}

		if (action === 'delete') {
			requestDelete(slug);
		}
	}
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="flex flex-col gap-6">
		<div>
			<h1 class="text-2xl font-semibold">Actividades</h1>
			<p class="text-muted-foreground">
				Listado de actividades del colectivo.
			</p>
		</div>

		<!-- Delegación de eventos -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <div on:click={handleTableClick}>
            <DataTable columns={activityColumns} data={activities} />
        </div>

        {#if showDeleteModal}
            <div class="fixed inset-0 z-50 flex items-center justify-center">
                <!-- Overlay -->
                <div
                    class="absolute inset-0 bg-black/50"
                    on:click={cancelDelete}
                />

                <!-- Modal -->
                <div class="relative z-10 w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
                    <h2 class="text-lg font-semibold">
                        Eliminar actividad
                    </h2>

                    <p class="mt-2 text-sm text-muted-foreground">
                        ¿Seguro que querés eliminar esta actividad?
                        Esta acción no se puede deshacer.
                    </p>

                    <div class="mt-6 flex justify-end gap-3">
                        <button
                            class="inline-flex h-9 items-center rounded-md border px-4 text-sm hover:bg-muted"
                            on:click={cancelDelete}
                        >
                            Cancelar
                        </button>

                        <button
                            class="inline-flex h-9 items-center rounded-md bg-red-600 px-4 text-sm text-white hover:bg-red-700"
                            on:click={confirmDelete}
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>
        {/if}
	</div>
</div>
