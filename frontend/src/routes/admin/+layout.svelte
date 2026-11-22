<script lang="ts">
	import { resolve } from '$app/paths';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { api, clearToken, errorMessage, getToken } from '$lib/api/client';

	let ready = false;
	let error = '';
	onMount(async () => {
		if (!getToken()) {
			await goto(resolve('/login'));
			return;
		}
		try {
			await api('/admin/users/me', {}, true);
			ready = true;
		} catch (cause) {
			error = errorMessage(cause);
		}
	});

	function logout() {
		clearToken();
		goto(resolve('/login'));
	}
</script>

{#if ready}
	<nav class="container mx-auto flex gap-4 px-4 pt-6" aria-label="Administración">
		<a href={resolve('/admin')}>Personas asociadas</a>
		<a href={resolve('/admin/actividades')}>Actividades</a>
		<button type="button" on:click={logout}>Cerrar sesión</button>
	</nav>
	<slot />
{:else if error}
	<p role="alert" class="container mx-auto p-8">{error}</p>
{:else}
	<p class="container mx-auto p-8">Verificando sesión…</p>
{/if}
