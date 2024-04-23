import type { NumberedNote } from './numbered-note';
import type { NumberedSquare } from './numbered-square';

export type Elimination = {
	type: 'elimination';
	technique: string;
	causingSquare?: NumberedSquare;
	causingNotes: NumberedNote[];
	eliminatedNotes: NumberedNote[];
	solutionIndex: number;
};
