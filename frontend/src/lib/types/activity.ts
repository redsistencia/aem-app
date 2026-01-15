export type Activity = {
	slug: string;
	date: string; // ISO string yyyy-mm-dd
	title: string;
	description: string;
	instagramUrl?: string;
	sent: boolean;
};
