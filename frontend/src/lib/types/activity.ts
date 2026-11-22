export type Activity = {
	id: number;
	slug: string;
	date: string;
	title: string;
	description: string;
	image_url?: string | null;
	instagramUrl?: string;
	sent: boolean;
};
