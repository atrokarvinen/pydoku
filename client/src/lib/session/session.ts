import { writable } from 'svelte/store';

export type Session = {
	userId: string | null;
};

export const session = writable<Session>({
	userId: null
});
