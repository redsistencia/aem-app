import { page } from 'vitest/browser';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { render } from 'vitest-browser-svelte';
import { goto } from '$app/navigation';
import ActivityEditor from './ActivityEditor.svelte';

vi.mock('$env/dynamic/public', () => ({ env: { PUBLIC_API_URL: 'http://localhost:8000' } }));
vi.mock('$app/navigation', () => ({ goto: vi.fn() }));

afterEach(() => {
	vi.restoreAllMocks();
	vi.clearAllMocks();
	sessionStorage.clear();
});

describe('editor de actividades', () => {
	it('guarda una actividad nueva en la API', async () => {
		sessionStorage.setItem('aem_access_token', 'session-token');
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify({ id: 1 }), { status: 201 }));
		render(ActivityEditor);
		await page.getByLabelText('Título').fill('Mateada');
		await page.getByLabelText('Descripción').fill('Encuentro en Palma');
		await page.getByLabelText('Fecha').fill('2026-12-10');
		await page.getByLabelText('Dirección de la actividad').fill('mateada');
		await page.getByRole('button', { name: 'Guardar', exact: true }).click();
		await expect.poll(() => vi.mocked(goto).mock.calls.length).toBe(1);
		const [url, options] = fetchMock.mock.calls[0]!;
		expect(url).toMatch(/\/admin\/activities\/$/);
		expect(options?.method).toBe('POST');
		expect(new Headers(options?.headers).get('Authorization')).toBe('Bearer session-token');
	});

	it('edita por ID y conserva el formulario cuando falla el guardado', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(
				new Response(JSON.stringify({ detail: 'An activity with this slug already exists' }), {
					status: 409
				})
			);
		render(ActivityEditor, {
			activity: {
				id: 42,
				title: 'Mateada',
				description: 'Encuentro en Palma',
				date: '2026-12-10',
				slug: 'mateada',
				sent: true
			}
		});
		await page.getByLabelText('Título').fill('Mateada actualizada');
		await page.getByRole('button', { name: 'Guardar', exact: true }).click();
		await expect
			.element(page.getByRole('alert'))
			.toHaveTextContent('An activity with this slug already exists');
		const [url, options] = fetchMock.mock.calls[0]!;
		expect(url).toMatch(/\/admin\/activities\/42$/);
		expect(options?.method).toBe('PATCH');
		expect(JSON.parse(options?.body as string)).not.toHaveProperty('sent');
		expect(goto).not.toHaveBeenCalled();
		await expect.element(page.getByLabelText('Título')).toHaveValue('Mateada actualizada');
	});
});
