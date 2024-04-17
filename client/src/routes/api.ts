import { axios } from '$lib/axios';
import type { Sudoku } from '$lib/types/sudoku';

export const getSudoku = async () => {
	return axios.get<Sudoku>('/sudoku');
};

export const getSudokuWithNotes = async () => {
	return axios.get<Sudoku>('/sudoku/notes');
};
