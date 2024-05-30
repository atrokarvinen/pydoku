import { setUserIdHeader } from '$lib/axios';
import { emptySudoku9x9 } from '$lib/types/sudoku';
import { redirect } from '@sveltejs/kit';
import { getSudoku } from './api';

export const ssr = false;

export const load = async () => {
	const userId = localStorage.getItem('userId');
	const isAuthenticated = !!userId;
	if (!isAuthenticated) {
		console.log('not authenticated, redirecting to auth...');
		throw redirect(300, '/auth');
	}
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
