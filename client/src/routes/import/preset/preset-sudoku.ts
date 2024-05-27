import type { Difficulty } from './difficulty';

export type PresetSudoku = {
	id: string;
	name: string;
	sudoku: string;
	difficulty: Difficulty;
};
