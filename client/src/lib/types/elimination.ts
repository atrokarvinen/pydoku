import type { EliminationReason } from './elimination-reason';

export type Elimination = {
	type: 'elimination';
	row: number;
	column: number;
	number: number;
	causedBy: EliminationReason;
	solutionIndex: number;
};
