import type { EliminationNote } from './elimination-note';

export type Elimination = {
	type: 'elimination';
	row: number;
	column: number;
	number: number;
	technique: string;
	formingNotes: EliminationNote[];
	eliminatedNotes: EliminationNote[];
	solutionIndex: number;
};
