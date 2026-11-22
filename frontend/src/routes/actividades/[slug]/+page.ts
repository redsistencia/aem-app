import { error } from '@sveltejs/kit';
import { api, ApiError } from '$lib/api/client';
import type { Activity } from '$lib/types/activity';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
	try {
		return { activity: await api<Activity>(`/activities/${encodeURIComponent(params.slug)}`) };
	} catch (cause) {
		error(
			cause instanceof ApiError && cause.status === 404 ? 404 : 503,
			cause instanceof ApiError && cause.status === 404
				? 'Actividad no encontrada'
				: 'No se pudo cargar la actividad'
		);
	}
};
