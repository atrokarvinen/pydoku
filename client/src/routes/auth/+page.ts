import { browser } from '$app/environment';
import { setUserIdHeader } from '$lib/axios';
import { session } from '$lib/session/session';
import { redirect } from '@sveltejs/kit';
import { createUser } from './api';

export const load = async () => {
	if (!browser) return;

	console.log('loading auth page');
	let userId = localStorage.getItem('userId');
	if (!userId) {
		try {
			const response = await createUser();
			const user = response.data;
			localStorage.setItem('userId', user.id);
			userId = user.id;
		} catch (error) {
			console.log('create user error: ', error);
			return { error: 'Failed to create new user.' };
		}
	}
	session.update((s) => ({ ...s, userId }));
	console.log('userId: ', userId);

	setUserIdHeader(userId);
	throw redirect(300, '/');
};
