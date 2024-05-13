<script lang="ts">
	import { axios } from '$lib/axios';
	import { getSolutionStepsCount, moveToSolutionStep } from '$lib/sudoku-log/sudoku-log';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import GameActionButtons from './GameActionButtons.svelte';
	import SolutionInfo from './SolutionInfo.svelte';
	import SudokuBoard from './SudokuBoard.svelte';
	import SudokuExport from './export/SudokuExport.svelte';
	import SudokuImport from './import/SudokuImport.svelte';

	export let sudoku: Sudoku;
	let selectedNumber: number | undefined;
	let selectedElimination: Elimination | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let solution: Solution = defaultSolution;
	let currentSolutionStep = 0;
	$: boardSize = sudoku.length;

	const resetSelections = () => {
		selectedNumber = undefined;
		selectedElimination = undefined;
		selectedCandidate = undefined;
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
		const response = await axios.post<Solution>('/sudoku/solve', { sudoku });
		solution = response.data;
		sudoku = solution.sudoku;
		currentSolutionStep = 0;
		resetSelections();
	};

	const next = async () => {
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
		resetSelections();
		const stepCount = getSolutionStepsCount(solution);
		for (let currentStep = currentSolutionStep; currentStep < stepCount; currentStep++) {
			const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep + 1);
			sudoku = newSudoku;
			await new Promise((resolve) => setTimeout(resolve, 20));
		}
		currentSolutionStep = stepCount;
	};

	const reverseSolution = async () => {
		resetSelections();
		for (let currentStep = currentSolutionStep; currentStep > 0; currentStep--) {
			const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep - 1);
			sudoku = newSudoku;
			await new Promise((resolve) => setTimeout(resolve, 20));
		}
		currentSolutionStep = 0;
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
	};
</script>

<div class="flex flex-col gap-5">
	<div class="flex flex-row gap-5">
		<SudokuImport {onSudokuImported} />
		<SudokuExport {sudoku} />
	</div>
	<SudokuBoard
		{sudoku}
		{selectedElimination}
		{selectedCandidate}
		{selectedNumber}
		{squarePressed}
	/>
	<GameActionButtons {boardSize} {numberClicked} />
	<div class="flex flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={solve}>Solve</button>
		<button class="btn variant-filled-primary" on:click={next}>N</button>
		<button class="btn variant-filled-primary" on:click={playSolution}>Play</button>
		<button class="btn variant-filled-primary" on:click={reverseSolution}>Reverse</button>
	</div>
	<SolutionInfo {solution} {candidateClicked} {eliminationClicked} />
</div>
