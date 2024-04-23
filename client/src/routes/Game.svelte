<script lang="ts">
	import { axios } from '$lib/axios';
	import { getSolutionStepsCount, moveToSolutionStep } from '$lib/sudoku-log/sudoku-log';
	import type { EliminationGroup } from '$lib/types/elimination-group';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Sudoku } from '$lib/types/sudoku';
	import GameActionButtons from './GameActionButtons.svelte';
	import SolutionInfo from './SolutionInfo.svelte';
	import SudokuBoard from './SudokuBoard.svelte';
	export let sudoku: Sudoku;
	let selectedNumber: number | undefined;
	let selectedElimination: EliminationGroup | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let solution: Solution = defaultSolution;
	let currentSolutionStep = 0;
	$: boardSize = sudoku.length;

	const fillNotes = async () => {
		const response = await axios.get<Sudoku>('/sudoku/notes');
		sudoku = response.data;
	};

	const resetSelections = () => {
		selectedNumber = undefined;
		selectedElimination = undefined;
		selectedCandidate = undefined;
	};

	const eliminationClicked = (elimination: EliminationGroup) => {
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
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} {selectedElimination} {selectedCandidate} {selectedNumber} />
	<GameActionButtons {boardSize} {numberClicked} />
	<div class="flex flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={solve}>Solve</button>
		<button class="btn variant-filled-primary" on:click={playSolution}>Play</button>
		<button class="btn variant-filled-primary" on:click={reverseSolution}>Reverse</button>
	</div>
	<SolutionInfo {solution} {candidateClicked} {eliminationClicked} />
</div>
