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
		key: 'instagramUrl',
		label: 'Instagram post',
		render: (value: string) =>
			value ? `<a href="${value}" target="_blank" class="text-primary underline">Ver</a>` : '—'
	},
	{
		key: 'sent',
		label: 'Enviado',
		render: (value: string) =>
			value
				? `<span class="text-green-600 font-medium">Sí</span>`
				: `<span class="text-muted-foreground">No</span>`
	},
	{
		key: 'slug',
		label: 'Acciones',
		render: (_, row: Activity) => {
			return `
			<div class="flex gap-2">
				<button
					class="inline-flex h-8 items-center rounded-md border px-3 text-xs hover:bg-muted"
					data-action="edit"
					data-slug="${row.slug}"
				>
					Editar
				</button>

				<button
					class="inline-flex h-8 items-center rounded-md border border-red-200 px-3 text-xs text-red-600 hover:bg-red-50"
					data-action="delete"
					data-slug="${row.slug}"
				>
					Eliminar
				</button>
			</div>
		`;
		}
	}
];
