import type { Elimination } from './elimination';
import type { SingleCandidate } from './single-candidate';

export type Solution = {
	eliminations: Elimination[];
	singleCandidates: SingleCandidate[];
};
