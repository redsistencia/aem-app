import type { Actions } from '@sveltejs/kit';
import { fail } from '@sveltejs/kit';

export const actions: Actions = {
	default: async ({ request }) => {
		const formData = await request.formData();

		const email = formData.get('email')?.toString().trim();
		const document_id = formData.get('document_id')?.toString().trim();

		// Validación mínima
		if (!email || !document_id) {
			return fail(400, {
				error: 'Faltan campos obligatorios'
			});
		}

		// Validación simple de email
		if (!email.includes('@')) {
			return fail(400, {
				error: 'Email inválido'
			});
		}

		return {
			success: true
		};
	}
};
