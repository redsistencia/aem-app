export type Activity = {
	slug: string;
	date: string; // ISO string yyyy-mm-dd
	title: string;
	description: string;
	imageUrl?: string;
	activityUrl: string;
	sent: boolean;
};
