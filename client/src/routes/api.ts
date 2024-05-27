import { axios } from '$lib/axios';
import type { Elimination } from '$lib/types/elimination';
import type { NumberedNote } from '$lib/types/numbered-note';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Solution } from '$lib/types/solution';
import type { Sudoku } from '$lib/types/sudoku';

export const getSudoku = async () => {
	return axios.get<Sudoku>('/sudoku');
};

export const getSudokuWithNotes = async () => {
	return axios.get<Sudoku>('/sudoku/notes');
};

export const solveSudoku = async (sudokuToSolve: Sudoku) => {
	const response = await axios.post<Solution>('/sudoku/solve', { sudoku: sudokuToSolve });
	const solution = response.data;
	const allSteps = [...solution.eliminations, ...solution.singleCandidates].sort(
		(a, b) => a.solutionIndex - b.solutionIndex
	);
	const firstNonScanIndex = allSteps.findIndex((step) => step.technique !== 'scan');
	const initialScan = allSteps.slice(0, firstNonScanIndex);
	const afterInitialScan = allSteps.slice(firstNonScanIndex);

	const eliminatedInitialNotes = initialScan.reduce((acc: NumberedNote[], step) => {
		if (step.type === 'elimination') {
			return [...acc, ...step.eliminatedNotes];
		}
		return acc;
	}, []);
	const initialScanStep: Elimination = {
		causingNotes: [],
		eliminatedNotes: eliminatedInitialNotes,
		technique: 'initial scan',
		highlightedRectangles: [],
		highlightedRegions: [],
		pointers: [],
		solutionIndex: 0,
		type: 'elimination',
		causingSquare: undefined
	};

	const newSteps = [initialScanStep, ...afterInitialScan];
	newSteps.forEach((step, index) => {
		step.solutionIndex = index;
	});

	solution.eliminations = newSteps.filter((step) => step.type === 'elimination') as Elimination[];
	solution.singleCandidates = newSteps.filter(
		(step) => step.type === 'single-candidate'
	) as SingleCandidate[];

	return solution;
};
