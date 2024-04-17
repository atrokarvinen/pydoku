import { browser } from '$app/environment';
import { getSudokuWithNotes } from './api';

export const load = async () => {
	console.log('loading...');
	if (!browser) {
		console.log('not in browser');
		return;
	}
	const response = await getSudokuWithNotes();
	const sudoku = response.data;
	console.log('received response: ', sudoku);
	return { sudoku };
};
