import type { HighlightedRectangle } from './highlighted-rectangle';
import type { HighlightedRegion } from './highlighted-region';

export type SingleCandidate = {
	type: 'single-candidate';
	row: number;
	column: number;
	number: number;
	otherNumbers: number[];
	highlightedRegions: HighlightedRegion[];
	highlightedRectangle: HighlightedRectangle;
	alignment: Alignment;
	solutionIndex: number;
};

export type Alignment = 'row' | 'column' | 'box' | 'cell';
