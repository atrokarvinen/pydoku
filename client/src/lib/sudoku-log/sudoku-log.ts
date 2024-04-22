import type { Elimination } from '$lib/types/elimination';
import type { EliminationGroup } from '$lib/types/elimination-group';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Solution } from '$lib/types/solution';
import type { Sudoku } from '$lib/types/sudoku';
import _ from 'lodash';

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

export const getSolutionStepsCount = (solution: Solution) => {
	return solution.eliminationGroups.length + solution.singleCandidates.length;
};

export const getSolutionSteps = (solution: Solution) => {
	const steps: (EliminationGroup | SingleCandidate)[] = [
		...solution.eliminationGroups,
		...solution.singleCandidates
	].sort((a, b) => a.solutionIndex - b.solutionIndex);
	return steps;
};

const undoStep = (sudoku: Sudoku, step: EliminationGroup | SingleCandidate) => {
	if (step.type === 'elimination') {
		undoEliminationGroup(sudoku, step);
	}
	if (step.type === 'single-candidate') {
		undoSingleCandidate(sudoku, step);
	}
};

const applyStep = (sudoku: Sudoku, step: EliminationGroup | SingleCandidate) => {
	if (step.type === 'elimination') {
		applyEliminationGroup(sudoku, step);
	}
	if (step.type === 'single-candidate') {
		applySingleCandidate(sudoku, step);
	}
};

const applyEliminationGroup = (sudoku: Sudoku, eliminationGroup: EliminationGroup) => {
	const eliminations: Elimination[] = eliminationGroup.eliminatedNotes.map((note) => ({
		row: note.row,
		column: note.column,
		number: note.number,
		causedBy: {} as any,
		solutionIndex: eliminationGroup.solutionIndex,
		type: 'elimination'
	}));
	applyEliminations(sudoku, eliminations);
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

const undoEliminationGroup = (sudoku: Sudoku, eliminationGroup: EliminationGroup) => {
	const eliminations: Elimination[] = eliminationGroup.eliminatedNotes.map((note) => ({
		row: note.row,
		column: note.column,
		number: note.number,
		causedBy: {} as any,
		solutionIndex: eliminationGroup.solutionIndex,
		type: 'elimination'
	}));
	undoEliminations(sudoku, eliminations);
};
const undoEliminations = (sudoku: Sudoku, eliminations: Elimination[]) => {
	eliminations.forEach((e) => undoElimination(sudoku, e));
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
