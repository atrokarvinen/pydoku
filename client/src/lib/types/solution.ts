import type { Elimination } from './elimination';
import type { SingleCandidate } from './single-candidate';
import type { Sudoku } from './sudoku';

export type Solution = {
	isSolved?: boolean;
	sudoku: Sudoku;
	finalSudoku: Sudoku;
	eliminations: Elimination[];
	singleCandidates: SingleCandidate[];
};

export const defaultSolution: Solution = {
	eliminations: [],
	singleCandidates: [],
	sudoku: [],
	finalSudoku: [],
	isSolved: undefined
};
