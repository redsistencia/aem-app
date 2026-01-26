import type { Actions } from '@sveltejs/kit';
import { fail } from '@sveltejs/kit';

export const actions: Actions = {
	default: async ({ request }) => {
		const formData = await request.formData();

		const name = formData.get('name')?.toString().trim();
		const lastname = formData.get('lastname')?.toString().trim();
		const email = formData.get('email')?.toString().trim();
		const privacyPolicy = formData.get('privacy_policy');

		// Validación mínima
		if (!name || !lastname || !email || !privacyPolicy) {
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
