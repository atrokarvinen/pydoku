import type { Elimination } from '$lib/types/elimination';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Solution } from '$lib/types/solution';
import type { Sudoku } from '$lib/types/sudoku';
import _ from 'lodash';

export const playSolution = (solution: Solution) => {
	const actions: (Elimination | SingleCandidate)[] = [
		...solution.eliminations,
		...solution.singleCandidates
	].sort((a, b) => a.solutionIndex - b.solutionIndex);

	const sudoku = solution.sudoku;
	for (const action of actions) {
		const nextIndex = action.solutionIndex;
		const nextElimination = solution.eliminations.find(
			(elimination) => elimination.solutionIndex === nextIndex
		);
		const nextSingleCandidate = solution.singleCandidates.find(
			(singleCandidate) => singleCandidate.solutionIndex === nextIndex
		);
		if (nextElimination) {
			applyElimination(sudoku, nextElimination);
		} else if (nextSingleCandidate) {
			applySingleCandidate(sudoku, nextSingleCandidate);
		}
	}
};

export const moveToSolutionStep = (
	current: Sudoku,
	currentStep: number,
	solution: Solution,
	targetStep: number
) => {
	const isCurrentCloser = currentStep - targetStep < targetStep - 0;
	const isReverse = isCurrentCloser && targetStep < currentStep;
	const initialStep = isCurrentCloser ? currentStep : 0;
	const initialSudoku = isCurrentCloser ? current : solution.sudoku;
	const sudoku = _.cloneDeep(initialSudoku);
	const stepRange = [initialStep, targetStep];
	const includedSteps = Array.from(
		{ length: Math.abs(targetStep - initialStep) },
		(_, i) => i + Math.min(...stepRange)
	);

	console.log('moving from step', currentStep, ' to step', targetStep);
	console.log('isCurrentCloser', isCurrentCloser, ' isReverse', isReverse);
	console.log('includedSteps', includedSteps);

	let steps = getSolutionSteps(solution).filter((step) =>
		includedSteps.includes(step.solutionIndex)
	);

	for (const step of steps) {
		const operation = isReverse ? undoStep : applyStep;
		operation(sudoku, step);
	}
	return sudoku;
};

const getSolutionSteps = (solution: Solution) => {
	const steps: (Elimination | SingleCandidate)[] = [
		...solution.eliminations,
		...solution.singleCandidates
	];
	return steps;
};

const undoStep = (sudoku: Sudoku, step: Elimination | SingleCandidate) => {
	if (step.type === 'elimination') {
		undoElimination(sudoku, step);
	}
	if (step.type === 'single-candidate') {
		undoSingleCandidate(sudoku, step);
	}
};

const applyStep = (sudoku: Sudoku, step: Elimination | SingleCandidate) => {
	if (step.type === 'elimination') {
		applyElimination(sudoku, step);
	}
	if (step.type === 'single-candidate') {
		applySingleCandidate(sudoku, step);
	}
};

const applyEliminations = (sudoku: Sudoku, eliminations: Elimination[]) => {
	eliminations.forEach((e) => applyElimination(sudoku, e));
};
const applyElimination = (sudoku: Sudoku, elimination: Elimination) => {
	const { row, column, number } = elimination;
	const square = sudoku[row][column];
	square.possibleNumbers = square.possibleNumbers.filter((n) => n !== number);
};

const applySingleCandidates = (sudoku: Sudoku, singleCandidates: SingleCandidate[]) => {
	singleCandidates.forEach((s) => applySingleCandidate(sudoku, s));
};
const applySingleCandidate = (sudoku: Sudoku, singleCandidate: SingleCandidate) => {
	const { row, column, number } = singleCandidate;
	sudoku[row][column].number = number;
};

const undoElimination = (sudoku: Sudoku, elimination: Elimination) => {
	const { row, column, number } = elimination;
	const square = sudoku[row][column];
	square.possibleNumbers.push(number);
};

const undoSingleCandidate = (sudoku: Sudoku, singleCandidate: SingleCandidate) => {
	const { row, column } = singleCandidate;
	sudoku[row][column].number = 0;
};
