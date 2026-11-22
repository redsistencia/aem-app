import { page } from 'vitest/browser';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { render } from 'vitest-browser-svelte';
import { goto } from '$app/navigation';
import Page from './+page.svelte';

vi.mock('$env/dynamic/public', () => ({ env: { PUBLIC_API_URL: 'http://localhost:8000' } }));
vi.mock('$app/navigation', () => ({ goto: vi.fn() }));

afterEach(() => {
	vi.restoreAllMocks();
	vi.clearAllMocks();
	sessionStorage.clear();
});

describe('login de administración', () => {
	it('usa la ruta de login y conserva el token antes de navegar', async () => {
		const fetchMock = vi
			.spyOn(globalThis, 'fetch')
			.mockResolvedValue(new Response(JSON.stringify({ access_token: 'session-token' })));
		render(Page);
		await page.getByLabelText('Email').fill('admin@example.com');
		await page.getByLabelText('Password').fill('password');
		await page.getByRole('button', { name: 'Ingresar' }).click();
		await expect.poll(() => sessionStorage.getItem('aem_access_token')).toBe('session-token');
		expect(fetchMock.mock.calls[0]![0]).toMatch(/\/admin\/users\/login$/);
		expect(goto).toHaveBeenCalledWith('/admin/actividades');
	});

	it('muestra credenciales inválidas sin iniciar una sesión', async () => {
		vi.spyOn(globalThis, 'fetch').mockResolvedValue(
			new Response(JSON.stringify({ detail: 'Invalid user credentials' }), { status: 401 })
		);
		render(Page);
		await page.getByLabelText('Email').fill('admin@example.com');
		await page.getByLabelText('Password').fill('wrong');
		await page.getByRole('button', { name: 'Ingresar' }).click();
		await expect.element(page.getByRole('alert')).toHaveTextContent('Invalid user credentials');
		expect(sessionStorage.getItem('aem_access_token')).toBeNull();
		expect(goto).not.toHaveBeenCalled();
	});
});
