<script context="module" lang="ts">
	export type Column<T> = {
		key: keyof T;
		label: string;
		class?: string;
		render?: (value: T[keyof T], row: T) => string;
	};
</script>

<script lang="ts">
	export let columns: Column<any>[] = [];
	export let data: any[] = [];
</script>


<div class="relative w-full overflow-x-auto rounded-md border">
	<table class="min-w-[640px] w-full text-sm whitespace-nowrap">
		<thead class="bg-muted">
			<tr>
				{#each columns as column}
					<th
						class="px-4 py-3 text-left font-medium text-muted-foreground {column.class}"
					>
						{column.label}
					</th>
				{/each}
			</tr>
		</thead>

		<tbody>
			{#if data.length === 0}
				<tr>
					<td
						colspan={columns.length}
						class="px-4 py-8 text-center text-muted-foreground"
					>
						Sin resultados
					</td>
				</tr>
			{:else}
				{#each data as row}
					<tr class="border-t hover:bg-muted/50 transition-colors">
						{#each columns as column}
							<td class="px-4 py-3 {column.class}">
								{#if column.render}
									{@html column.render(row[column.key], row)}
								{:else}
									{row[column.key]}
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
