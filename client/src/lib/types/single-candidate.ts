export type SingleCandidate = {
	type: 'single-candidate';
	row: number;
	column: number;
	number: number;
	otherNumbers: number[];
	alignment: Alignment;
	solutionIndex: number;
};

export type Alignment = 'row' | 'column' | 'box' | 'cell';
