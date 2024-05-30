<script lang="ts">
	import { moveToSolutionStep } from '$lib/solution/solution-log';
	import { getSolutionStepsCount } from '$lib/solution/solution-parser';
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import GameSolveButtons from './GameSolveButtons.svelte';
	import { solveSudoku } from './api';
	import SudokuBoard from './board/SudokuBoard.svelte';
	import SolutionInfo from './solution/SolutionInfo.svelte';

	export let sudoku: Sudoku;
	export let maxWidth: number;
	let selectedNumber: number | undefined;
	let selectedElimination: Elimination | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let selectedSquare: Square | undefined;
	let solution: Solution = defaultSolution;
	let currentSolutionStep: number | undefined = undefined;
	let isSolving = false;
	let isPlaying = false;
	$: onSudokuImported($sudokuStore);

	const resetSelections = () => {
		selectedNumber = undefined;
		selectedElimination = undefined;
		selectedCandidate = undefined;
		selectedSquare = undefined;
	};

	const eliminationClicked = (elimination: Elimination) => {
		const newSudoku = moveToSolutionStep(
			sudoku,
			currentSolutionStep ?? 0,
			solution,
			elimination.solutionIndex
		);

		resetSelections();
		selectedElimination = elimination;
		currentSolutionStep = elimination.solutionIndex;
		sudoku = newSudoku;
	};

	const candidateClicked = (candidate: SingleCandidate) => {
		const newSudoku = moveToSolutionStep(
			sudoku,
			currentSolutionStep ?? 0,
			solution,
			candidate.solutionIndex
		);

		resetSelections();
		selectedCandidate = candidate;
		currentSolutionStep = candidate.solutionIndex;
		sudoku = newSudoku;
	};

	const solve = async () => {
		isSolving = true;
		try {
			const originalSudoku = solution.sudoku.length > 0 ? solution.sudoku : undefined;
			solution = await solveSudoku(sudoku);
			solution.sudoku = originalSudoku ?? solution.sudoku;
			sudoku = solution.sudoku;
			currentSolutionStep = undefined;
			resetSelections();
		} catch (error) {
			console.log('solve error: ', error);
		} finally {
			isSolving = false;
		}
	};

	const jumpToStart = () => {
		resetSelections();
		currentSolutionStep = undefined;
		sudoku = solution.sudoku.length > 0 ? solution.sudoku : sudoku;
	};

	const back = async () => {
		if (currentSolutionStep === undefined || currentSolutionStep <= 0) {
			return;
		}
		const currentStep = currentSolutionStep;
		const nextStep = currentSolutionStep - 1;
		const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, nextStep);
		resetSelections();
		selectedElimination = solution.eliminations.find((e) => e.solutionIndex === nextStep);
		selectedCandidate = solution.singleCandidates.find((c) => c.solutionIndex === nextStep);
		sudoku = newSudoku;
		currentSolutionStep = nextStep;
	};

	const next = () => {
		if (
			currentSolutionStep !== undefined &&
			currentSolutionStep >= getSolutionStepsCount(solution)
		) {
			return;
		}
		const currentStep = currentSolutionStep ?? 0;
		const nextStep = currentSolutionStep === undefined ? 0 : currentSolutionStep + 1;
		const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, nextStep);
		resetSelections();
		selectedElimination = solution.eliminations.find((e) => e.solutionIndex === nextStep);
		selectedCandidate = solution.singleCandidates.find((c) => c.solutionIndex === nextStep);
		sudoku = newSudoku;
		currentSolutionStep = nextStep;
	};

	const playSolution = async () => {
		isPlaying = true;
		try {
			if (currentSolutionStep === undefined) {
				currentSolutionStep = 0;
			}
			resetSelections();
			const stepCount = getSolutionStepsCount(solution);
			for (let currentStep = currentSolutionStep; currentStep < stepCount; currentStep++) {
				const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep + 1);
				sudoku = newSudoku;
				await new Promise((resolve) => setTimeout(resolve, 20));
			}
			currentSolutionStep = stepCount;
		} catch (error) {
			console.error('play solution error: ', error);
		} finally {
			isPlaying = false;
		}
	};

	const jumpToEnd = () => {
		resetSelections();
		const stepCount = getSolutionStepsCount(solution);
		currentSolutionStep = stepCount;
		sudoku = solution.finalSudoku.length > 0 ? solution.finalSudoku : sudoku;
	};

	const numberClicked = (n: number) => {
		if (selectedNumber === n) {
			selectedNumber = undefined;
			return;
		}
		resetSelections();
		selectedNumber = n;
	};

	const onSudokuImported = (importedSudoku: Sudoku | undefined) => {
		if (!importedSudoku) {
			return;
		}
		resetSelections();
		currentSolutionStep = 0;
		solution = defaultSolution;
		sudoku = importedSudoku;
	};

	const squarePressed = (square: Square) => {
		numberClicked(square.number);
		selectedSquare = square;
	};
</script>

<div class="flex flex-col gap-2 max-h-full" style="width:{maxWidth}px">
	<SudokuBoard
		{sudoku}
		{maxWidth}
		{selectedElimination}
		{selectedCandidate}
		{selectedNumber}
		{selectedSquare}
		{squarePressed}
	/>
	<GameSolveButtons
		{solve}
		{jumpToStart}
		{back}
		{next}
		{playSolution}
		{jumpToEnd}
		{isSolving}
		{isPlaying}
	/>
	<SolutionInfo
		{solution}
		{candidateClicked}
		{eliminationClicked}
		{selectedElimination}
		{selectedCandidate}
	/>
</div>
