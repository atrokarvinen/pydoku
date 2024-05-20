import type { HighlightedRectangle } from './highlighted-rectangle';
import type { HighlightedRegion } from './highlighted-region';
import type { NumberedNote } from './numbered-note';
import type { NumberedSquare } from './numbered-square';
import type { Pointer } from './pointer';

export type Elimination = {
	type: 'elimination';
	technique: string;
	causingSquare?: NumberedSquare;
	causingNotes: NumberedNote[];
	eliminatedNotes: NumberedNote[];
	highlightedRegions: HighlightedRegion[];
	highlightedRectangle: HighlightedRectangle;
	pointers: Pointer[];
	solutionIndex: number;
};
