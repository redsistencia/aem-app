import type { Column } from '$lib/components/ui/Data-table.svelte';
import type { Activity } from '$lib/types/activity';

export const activityColumns: Column<Activity>[] = [
	{ key: 'date', label: 'Fecha' },
	{ key: 'title', label: 'Título' },
	{ key: 'description', label: 'Descripción' },
	{ key: 'sent', label: 'Enviado' }
];
