import type { EliminationNote } from './elimination-note';

export type EliminationGroup = {
	type: 'elimination';
	row: number;
	column: number;
	number: number;
	technique: string;
	eliminatedNotes: EliminationNote[];
	solutionIndex: number;
};
