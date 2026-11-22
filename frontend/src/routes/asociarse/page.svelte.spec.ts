import { page } from 'vitest/browser';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { render } from 'vitest-browser-svelte';
import Page from './+page.svelte';

vi.mock('$env/dynamic/public', () => ({ env: { PUBLIC_API_URL: 'http://localhost:8000' } }));

afterEach(() => vi.restoreAllMocks());

async function fillForm() {
	await page.getByLabelText('Nombre o alias').fill('Daniela');
	await page.getByLabelText('Apellido/s').fill('Pérez');
	await page.getByLabelText('Email', { exact: true }).fill('socia@example.com');
	await page.getByLabelText('Dirección').fill('Palma');
	await page.getByLabelText('Nacionalidad').fill('Argentina');
	await page.getByLabelText('DNI / NIE / Pasaporte').fill('AB12345');
	await page.getByLabelText('Teléfono').fill('+34600123456');
	await page.getByLabelText('Acepto la política de privacidad').click();
}

describe('alta de asociación', () => {
	it('guarda los datos y permite no recibir newsletters', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify({ id: 1 }), { status: 201 }));
		render(Page);
		await fillForm();
		await page.getByRole('button', { name: 'Asociarse', exact: true }).click();
		await expect
			.element(page.getByText('¡Gracias por asociarte!', { exact: false }))
			.toBeInTheDocument();
		expect(fetchMock.mock.calls[0]![0]).toMatch(/\/subscribers\/$/);
		expect(JSON.parse(fetchMock.mock.calls[0]![1]?.body as string)).toMatchObject({
			lastname: 'Pérez',
			newsletter: false,
			privacy_policy: true
		});
	});

	it('muestra el fallo de la API y conserva los datos para reintentar', async () => {
		vi.spyOn(globalThis, 'fetch').mockResolvedValue(
			new Response(JSON.stringify({ detail: 'Subscriber already exists' }), { status: 409 })
		);
		render(Page);
		await fillForm();
		await page.getByRole('button', { name: 'Asociarse', exact: true }).click();
		await expect.element(page.getByText('Subscriber already exists')).toBeInTheDocument();
		await expect
			.element(page.getByLabelText('Email', { exact: true }))
			.toHaveValue('socia@example.com');
		await expect
			.element(page.getByText('¡Gracias por asociarte!', { exact: false }))
			.not.toBeInTheDocument();
	});
});
