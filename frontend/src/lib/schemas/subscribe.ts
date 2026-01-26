import { z } from 'zod';

export const subscribeSchema = z.object({
    // TO-DO: completar el schema con todos los campos del formulario
	name: z.string().min(1).max(150),
	email: z.string().email().max(150),
	privacyPolicy: z.literal(true),
	newsletterConsent: z.literal(true)
});

export type SubscribeInput = z.infer<typeof subscribeSchema>;
