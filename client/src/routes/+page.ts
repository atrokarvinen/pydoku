import { browser } from '$app/environment';
import { getSudokuWithNotes } from './api';

export const load = async () => {
	if (!browser) return;
	const response = await getSudokuWithNotes();
	const sudoku = response.data;
	return { sudoku };
};
