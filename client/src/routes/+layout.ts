import { setUserIdHeader } from '$lib/axios';
import { session } from '$lib/session/session';
import { emptySudoku9x9 } from '$lib/types/sudoku';
import { getSudoku } from './api';
import { createUser } from './auth/api';

export const ssr = false;

export const load = async () => {
	const userId = await getUserId();
	setUserIdHeader(userId);

	let sudoku;
	if (process.env.NODE_ENV === 'development') {
		const response = await getSudoku();
		sudoku = response.data;
	} else {
		sudoku = emptySudoku9x9;
	}

	return { sudoku };
};

const getUserId = async (): Promise<string> => {
	let userId = localStorage.getItem('userId');
	if (!userId) {
		try {
			const response = await createUser();
			const user = response.data;
			localStorage.setItem('userId', user.id);
			userId = user.id;
		} catch (error) {
			console.log('create user error: ', error);
			throw new Error('Failed to create new user.');
		}
	}
	session.update((s) => ({ ...s, userId }));

	setUserIdHeader(userId);
	return userId!;
};
