import { setUserIdHeader } from '$lib/axios';
import { session } from '$lib/session/session';
import { redirect } from '@sveltejs/kit';
import { createUser } from './api';

export const ssr = false;

export const load = async () => {
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

	setUserIdHeader(userId);
	throw redirect(300, '/');
};
