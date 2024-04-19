import { browser } from '$app/environment';
import { getSudoku } from './api';

export const load = async () => {
	if (!browser) return;
	// const response = await getSudokuWithNotes();
	const response = await getSudoku();
	const sudoku = response.data;
	return { sudoku };
};
