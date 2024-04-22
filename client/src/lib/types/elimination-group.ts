import type { EliminationNote } from './elimination-note';

export type EliminationGroup = {
	type: 'elimination';
	row: number;
	column: number;
	number: number;
	technique: string;
	formingNotes: EliminationNote[];
	eliminatedNotes: EliminationNote[];
	solutionIndex: number;
};
