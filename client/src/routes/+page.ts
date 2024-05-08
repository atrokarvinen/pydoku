import { browser } from '$app/environment';
import { emptySudoku9x9 } from '$lib/types/sudoku';

export const load = async () => {
	if (!browser) return;
	// const response = await getSudoku();
	// const sudoku = response.data;
	const sudoku = emptySudoku9x9;
	return { sudoku };
};
