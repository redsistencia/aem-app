<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import DataTable, { type Column } from '$lib/components/ui/Data-table.svelte';

	type Asociade = {
		id: number;
		nombre: string;
		email: string;
		estado: 'activo' | 'pendiente' | 'baja';
		fecha: string;
	};

	const data: Asociade[] = [
		{
			id: 1,
			nombre: 'María González',
			email: 'maria@gmail.com',
			estado: 'activo',
			fecha: '2025-01-12'
		},
		{
			id: 2,
			nombre: 'Juan Pérez',
			email: 'juan@gmail.com',
			estado: 'pendiente',
			fecha: '2025-01-20'
		},
		{
			id: 3,
			nombre: 'Lucía Fernández',
			email: 'lucia@gmail.com',
			estado: 'baja',
			fecha: '2024-12-03'
		}
	];

	const columns: Column<Asociade>[] = [
		{
			key: 'nombre',
			label: 'Nombre'
		},
		{
			key: 'email',
			label: 'Email',
			class: 'text-muted-foreground'
		},
        {
            key: 'estado',
            label: 'Estado',
            render: (value, row) => {
                const estado = value as Asociade['estado'];

                const styles: Record<Asociade['estado'], string> = {
                    activo: 'bg-green-100 text-green-800',
                    pendiente: 'bg-yellow-100 text-yellow-800',
                    baja: 'bg-red-100 text-red-800'
                };

                return `
                    <span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${styles[estado]}">
                        ${estado}
                    </span>
                `;
            }
        },
		{
			key: 'fecha',
			label: 'Fecha'
		},
		{
			key: 'id',
			label: '',
			class: 'text-right',
			render: () =>
				`<button class="inline-flex items-center justify-center rounded-md border px-3 h-8 text-sm hover:bg-muted transition-colors">
					Ver
				</button>`
		}
	];
</script>

<div class="container mx-auto px-4 py-12 space-y-8">
	<header class="space-y-2">
		<h1 class="text-3xl font-semibold tracking-tight">
			Panel de administración
		</h1>
		<p class="text-muted-foreground">
			Listado de personas asociadas (mock)
		</p>
	</header>

	<DataTable {columns} {data} />
</div>
