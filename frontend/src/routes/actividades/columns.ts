import type { Column } from '$lib/types/data-table';
import type { Activity } from '$lib/types/activity';

export const activityColumns: Column<Activity>[] = [
	{
		key: 'date',
		label: 'Fecha',
		render: (value: string) => new Date(value).toLocaleDateString()
	},
	{
		key: 'title',
		label: 'Título',
		class: 'font-medium',
		render: (_value, row) =>
			`<a href="/actividades/${row.slug}" class="hover:underline text-primary">
				${row.title}
			</a>`
	},
	{
		key: 'description',
		label: 'Descripción',
		class: 'max-w-[450px] truncate'
	},
	{
		key: 'imageUrl',
		label: 'Imagen',
		render: (value: string) =>
			value ? `<a href="${value}" target="_blank" class="text-primary underline">Ver</a>` : '—'
	},
	{
		key: 'activityUrl',
		label: 'URL',
		render: (value: string) =>
			`<a href="${value}" target="_blank" class="text-primary underline">Abrir</a>`
	},
	{
		key: 'sent',
		label: 'Enviado',
		render: (value: string) =>
			value
				? `<span class="text-green-600 font-medium">Sí</span>`
				: `<span class="text-muted-foreground">No</span>`
	}
];
