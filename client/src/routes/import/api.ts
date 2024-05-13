import { axios } from '$lib/axios';
import type { Sudoku } from '$lib/types/sudoku';

export const importFromImage = async (files: FileList | undefined) => {
	if (!files || files.length === 0) {
		return;
	}

	const formData = new FormData();
	formData.append('file', files[0]);

	try {
		const response = await axios.postForm<Sudoku>('/sudoku/import/image', formData);
		const sudoku = response.data;
		return sudoku;
	} catch (error) {
		console.log('import sudoku from image error: ', error);
		throw error;
	}
};

export const importFromString = async (sudokuString: string | undefined) => {
	if (!sudokuString) {
		return;
	}

	try {
		const response = await axios.post<Sudoku>('/sudoku/import/string', { sudoku: sudokuString });
		const sudoku = response.data;
		return sudoku;
	} catch (error) {
		console.log('import sudoku from string error: ', error);
		throw error;
	}
};
