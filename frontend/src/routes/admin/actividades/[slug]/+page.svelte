<script lang="ts">
	import type { PageData } from './$types';
	import ActivityEditor from '$lib/components/ActivityEditor.svelte';
	export let data: PageData;
</script>

{#key data.activity.id}
	<ActivityEditor activity={data.activity} />
{/key}
