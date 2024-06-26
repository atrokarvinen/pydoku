import type { Elimination } from '$lib/types/elimination';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Solution } from '$lib/types/solution';
import type { Sudoku } from '$lib/types/sudoku';
import _ from 'lodash';
import { getSolutionSteps } from './solution-parser';

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

	let steps = getSolutionSteps(solution).filter((step) =>
		includedSteps.includes(step.solutionIndex)
	);

	for (const step of steps) {
		const operation = isReverse ? undoStep : applyStep;
		operation(sudoku, step);
	}
	return sudoku;
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

const applyElimination = (sudoku: Sudoku, elimination: Elimination) => {
	elimination.eliminatedNotes.forEach((note) => {
		const { column, row, number } = note;
		const square = sudoku[row][column];
		square.possibleNumbers = square.possibleNumbers.filter((n) => n !== number);
	});
};

const applySingleCandidate = (sudoku: Sudoku, singleCandidate: SingleCandidate) => {
	const { row, column, number } = singleCandidate;
	sudoku[row][column].number = number;
	sudoku[row][column].possibleNumbers = [];
};

const undoElimination = (sudoku: Sudoku, elimination: Elimination) => {
	elimination.eliminatedNotes.forEach((note) => {
		const { column, row, number } = note;
		const square = sudoku[row][column];
		square.possibleNumbers.push(number);
	});
};

const undoSingleCandidate = (sudoku: Sudoku, singleCandidate: SingleCandidate) => {
	const { row, column, number } = singleCandidate;
	const square = sudoku[row][column];
	square.number = 0;
	square.possibleNumbers.push(number);
	square.possibleNumbers.push(...singleCandidate.otherNumbers);
};
