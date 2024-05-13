import { browser } from '$app/environment';
import { emptySudoku9x9 } from '$lib/types/sudoku';
import { getSudoku } from './api';

export const load = async () => {
	if (!browser) return;

	let sudoku;
	if (process.env.NODE_ENV === 'development') {
		const response = await getSudoku();
		sudoku = response.data;
	} else {
		sudoku = emptySudoku9x9;
	}

	return { sudoku };
};
