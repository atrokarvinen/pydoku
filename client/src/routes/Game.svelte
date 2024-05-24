<script lang="ts">
	import { axios } from '$lib/axios';
	import { moveToSolutionStep } from '$lib/solution/solution-log';
	import { getSolutionStepsCount } from '$lib/solution/solution-parser';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import GameNumberButtons from './GameNumberButtons.svelte';
	import GameSolveButtons from './GameSolveButtons.svelte';
	import SudokuBoard from './board/SudokuBoard.svelte';
	import SudokuExport from './export/SudokuExport.svelte';
	import SudokuImport from './import/SudokuImport.svelte';
	import SolutionInfo from './solution/SolutionInfo.svelte';

	export let sudoku: Sudoku;
	let selectedNumber: number | undefined;
	let selectedElimination: Elimination | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let selectedSquare: Square | undefined;
	let solution: Solution = defaultSolution;
	let currentSolutionStep = 0;
	let isSolving = false;
	let isPlaying = false;
	$: boardSize = sudoku.length;

	const resetSelections = () => {
		selectedNumber = undefined;
		selectedElimination = undefined;
		selectedCandidate = undefined;
		selectedSquare = undefined;
	};

	const eliminationClicked = (elimination: Elimination) => {
		const newSudoku = moveToSolutionStep(
			sudoku,
			currentSolutionStep,
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
			currentSolutionStep,
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
			const sudokuToSolve = solution.sudoku.length > 0 ? solution.sudoku : sudoku;
			const response = await axios.post<Solution>('/sudoku/solve', { sudoku: sudokuToSolve });
			solution = response.data;
			sudoku = solution.sudoku;
			currentSolutionStep = 0;
			resetSelections();
		} catch (error) {
			console.log('solve error: ', error);
		} finally {
			isSolving = false;
		}
	};

	const jumpToStart = () => {
		resetSelections();
		currentSolutionStep = 0;
		sudoku = solution.sudoku;
	};

	const reverseSolution = async () => {
		isPlaying = true;
		try {
			resetSelections();
			for (let currentStep = currentSolutionStep; currentStep > 0; currentStep--) {
				const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep - 1);
				sudoku = newSudoku;
				await new Promise((resolve) => setTimeout(resolve, 20));
			}
			currentSolutionStep = 0;
		} catch (error) {
			console.error('reverse solution error: ', error);
		} finally {
			isPlaying = false;
		}
	};

	const next = () => {
		if (currentSolutionStep >= getSolutionStepsCount(solution)) {
			return;
		}
		const newSudoku = moveToSolutionStep(
			sudoku,
			currentSolutionStep,
			solution,
			currentSolutionStep + 1
		);
		resetSelections();
		selectedElimination = solution.eliminations.find(
			(e) => e.solutionIndex === currentSolutionStep + 1
		);
		if (!selectedElimination) {
			selectedCandidate = solution.singleCandidates.find(
				(c) => c.solutionIndex === currentSolutionStep + 1
			);
		}
		sudoku = newSudoku;
		currentSolutionStep++;
	};

	const playSolution = async () => {
		isPlaying = true;
		try {
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
		sudoku = solution.finalSudoku;
	};

	const numberClicked = (n: number) => {
		if (selectedNumber === n) {
			selectedNumber = undefined;
			return;
		}
		resetSelections();
		selectedNumber = n;
	};

	const onSudokuImported = (importedSudoku: Sudoku) => {
		if (!importedSudoku) {
			return;
		}
		console.log('sudoku imported: ', importedSudoku);
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

<div class="flex flex-col gap-2 max-h-full" style="width:360px">
	<div class="flex flex-row gap-5">
		<SudokuImport {onSudokuImported} />
		<SudokuExport {sudoku} />
	</div>
	<SudokuBoard
		{sudoku}
		{selectedElimination}
		{selectedCandidate}
		{selectedNumber}
		{selectedSquare}
		{squarePressed}
	/>
	<GameNumberButtons {boardSize} {numberClicked} />
	<GameSolveButtons
		{solve}
		{jumpToStart}
		{reverseSolution}
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
