export type Column<T> = {
	key: keyof T;
	label: string;
	class?: string;
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	render?: (value: any, row: T) => string;
};
