import type { EliminationReason } from './elimination-reason';

export type Elimination = {
	row: number;
	column: number;
	number: number;
	causedBy: EliminationReason;
};
