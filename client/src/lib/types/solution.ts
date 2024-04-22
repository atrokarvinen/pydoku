import type { Elimination } from './elimination';
import type { EliminationGroup } from './elimination-group';
import type { SingleCandidate } from './single-candidate';
import type { Sudoku } from './sudoku';

export type Solution = {
	isSolved: boolean;
	sudoku: Sudoku;
	eliminations: Elimination[];
	eliminationGroups: EliminationGroup[];
	singleCandidates: SingleCandidate[];
};

export const defaultSolution: Solution = {
	eliminations: [],
	eliminationGroups: [],
	singleCandidates: [],
	sudoku: [],
	isSolved: false
};
