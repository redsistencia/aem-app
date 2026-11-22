import { env } from '$env/dynamic/public';

const apiUrl = (env.PUBLIC_API_URL || 'http://localhost:8000').replace(/\/$/, '');
const sessionKey = 'aem_access_token';

export class ApiError extends Error {
	constructor(
		public status: number,
		message: string
	) {
		super(message);
	}
}

export function getToken(): string | null {
	return typeof sessionStorage === 'undefined' ? null : sessionStorage.getItem(sessionKey);
}

export function setToken(token: string): void {
	sessionStorage.setItem(sessionKey, token);
}

export function clearToken(): void {
	sessionStorage.removeItem(sessionKey);
}

export async function api<T>(
	path: string,
	options: RequestInit = {},
	authenticated = false
): Promise<T> {
	const headers = new Headers(options.headers);
	if (options.body) headers.set('Content-Type', 'application/json');
	if (authenticated) {
		const token = getToken();
		if (token) headers.set('Authorization', `Bearer ${token}`);
	}
	let response: Response;
	try {
		response = await fetch(`${apiUrl}${path}`, { ...options, headers });
	} catch {
		throw new ApiError(0, 'No se pudo conectar con el servidor. Intentá de nuevo.');
	}
	if (!response.ok) {
		const body = await response.json().catch(() => null);
		if (authenticated && response.status === 401) {
			clearToken();
			window.location.assign('/login');
		}
		const message =
			typeof body?.detail === 'string' ? body.detail : 'Revisá los datos e intentá de nuevo.';
		throw new ApiError(response.status, message);
	}
	return response.status === 204 ? (undefined as T) : response.json();
}

export function errorMessage(error: unknown): string {
	return error instanceof Error ? error.message : 'Ocurrió un error. Intentá de nuevo.';
}
