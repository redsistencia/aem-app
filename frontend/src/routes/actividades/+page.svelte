<script lang="ts">
	import DataTable from '$lib/components/ui/Data-table.svelte';

	import { activities } from '$lib/mocks/activities';
	import { activityColumns } from './columns';
</script>

<div class="container mx-auto px-4 sm:px-6 lg:px-24 xl:px-24 py-24">
	<div class="flex flex-col gap-6">
		<div>
			<h1 class="text-2xl font-semibold">Actividades</h1>
			<p class="text-muted-foreground">
				Listado de actividades del colectivo.
			</p>
		</div>

		<DataTable columns={activityColumns} data={activities} />
	</div>
</div>
