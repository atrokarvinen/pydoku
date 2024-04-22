import type { Elimination } from './elimination';
import type { SingleCandidate } from './single-candidate';
import type { Sudoku } from './sudoku';

export type Solution = {
	sudoku: Sudoku;
	eliminations: Elimination[];
	singleCandidates: SingleCandidate[];
};
