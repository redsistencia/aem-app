import { z } from 'zod';

export const subscribeSchema = z.object({
	name: z.string().trim().min(1).max(150),
	lastname: z.string().trim().min(1).max(150),
	email: z.string().trim().email().max(150),
	address: z.string().trim().max(250),
	nationality: z.string().trim().max(30),
	document_id: z
		.string()
		.trim()
		.min(1)
		.max(50)
		.regex(/^[A-Za-z0-9]+$/),
	phone: z.string().trim().max(30),
	privacy_policy: z.literal(true),
	newsletter: z.boolean().default(false)
});

export type SubscribeInput = z.infer<typeof subscribeSchema>;
