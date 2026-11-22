import { afterEach, describe, expect, it, vi } from 'vitest';
import { api, setToken } from './client';

vi.mock('$env/dynamic/public', () => ({ env: { PUBLIC_API_URL: 'http://localhost:8000' } }));

afterEach(() => vi.unstubAllGlobals());

describe('cliente API', () => {
	it('envía el token de la sesión en las operaciones de administración', async () => {
		const storage = new Map<string, string>();
		vi.stubGlobal('sessionStorage', {
			setItem: (key: string, value: string) => storage.set(key, value),
			getItem: (key: string) => storage.get(key)
		});
		setToken('test-token');
		const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: 1 })));
		vi.stubGlobal('fetch', fetchMock);
		await api('/admin/activities/', { method: 'POST', body: '{}' }, true);
		const [url, options] = fetchMock.mock.calls[0]!;
		expect(url).toBe('http://localhost:8000/admin/activities/');
		expect(options.headers.get('Authorization')).toBe('Bearer test-token');
		expect(options.headers.get('Content-Type')).toBe('application/json');
	});

	it('propaga los errores del backend sin informar éxito', async () => {
		vi.stubGlobal(
			'fetch',
			vi
				.fn()
				.mockResolvedValue(
					new Response(JSON.stringify({ detail: 'Subscriber already exists' }), { status: 409 })
				)
		);
		await expect(api('/subscribers/', { method: 'POST', body: '{}' })).rejects.toMatchObject({
			status: 409,
			message: 'Subscriber already exists'
		});
	});

	it('muestra un error útil cuando falla la conexión', async () => {
		vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
		await expect(api('/activities/')).rejects.toMatchObject({
			status: 0,
			message: expect.stringContaining('No se pudo conectar')
		});
	});
});
