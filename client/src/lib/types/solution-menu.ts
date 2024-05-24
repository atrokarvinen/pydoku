import type { Elimination } from './elimination';
import type { SingleCandidate } from './single-candidate';

export type SolutionMenu = {
	groups: SolutionGroup[];
};

export type SolutionGroup = {
	technique: string;
	steps: SolutionStep[];
};

export type SolutionStep = {
	step: number;
	solution: Elimination | SingleCandidate;
};
