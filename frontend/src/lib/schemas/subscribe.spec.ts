import { describe, expect, it } from 'vitest';
import { subscribeSchema } from './subscribe';

const input = {
	name: ' Daniela ',
	lastname: ' Pérez ',
	email: 'socia@example.com',
	address: 'Palma',
	nationality: 'Argentina',
	document_id: 'AB12345',
	phone: '+34600123456',
	privacy_policy: true
};

describe('formulario de asociación', () => {
	it('permite asociarse sin consentir newsletters', () => {
		const parsed = subscribeSchema.parse(input);
		expect(parsed.newsletter).toBe(false);
		expect(parsed.name).toBe('Daniela');
	});

	it('exige el consentimiento de privacidad y un email válido', () => {
		expect(subscribeSchema.safeParse({ ...input, privacy_policy: false }).success).toBe(false);
		expect(subscribeSchema.safeParse({ ...input, email: 'invalid' }).success).toBe(false);
	});

	it('valida límites compatibles con PostgreSQL', () => {
		expect(subscribeSchema.safeParse({ ...input, nationality: 'x'.repeat(31) }).success).toBe(
			false
		);
		expect(subscribeSchema.safeParse({ ...input, document_id: 'x'.repeat(51) }).success).toBe(
			false
		);
	});
});
