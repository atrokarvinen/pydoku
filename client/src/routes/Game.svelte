<script lang="ts">
	import { axios } from '$lib/axios';
	import { moveToSolutionStep } from '$lib/sudoku-log/sudoku-log';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Sudoku } from '$lib/types/sudoku';
	import SolutionInfo from './SolutionInfo.svelte';
	import SudokuBoard from './SudokuBoard.svelte';
	export let sudoku: Sudoku;
	let selectedElimination: Elimination | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let solution: Solution = defaultSolution;
	let currentSolutionStep = 0;

	const fillNotes = async () => {
		const response = await axios.get<Sudoku>('/sudoku/notes');
		sudoku = response.data;
	};

	const eliminationClicked = (elimination: Elimination) => {
		const newSudoku = moveToSolutionStep(
			sudoku,
			currentSolutionStep,
			solution,
			elimination.solutionIndex
		);

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

		selectedCandidate = candidate;
		currentSolutionStep = candidate.solutionIndex;
		sudoku = newSudoku;
	};

	const solve = async () => {
		const response = await axios.post<Solution>('/sudoku/solve', { sudoku });
		solution = response.data;
		sudoku = solution.sudoku;
	};

	const playSolution = async () => {
		const steps = solution.eliminations.length + solution.singleCandidates.length;
		for (let currentStep = 0; currentStep < steps; currentStep++) {
			const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep + 1);
			sudoku = newSudoku;
			await new Promise((resolve) => setTimeout(resolve, 20));
		}
	};

	const reverseSolution = async () => {
		const steps = solution.eliminations.length + solution.singleCandidates.length;
		const initialSudoku = moveToSolutionStep(sudoku, currentSolutionStep, solution, steps + 1);
		sudoku = initialSudoku;
		for (let currentStep = steps; currentStep > 0; currentStep--) {
			const newSudoku = moveToSolutionStep(sudoku, currentStep, solution, currentStep - 1);
			sudoku = newSudoku;
			await new Promise((resolve) => setTimeout(resolve, 20));
		}
	};
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} {selectedElimination} {selectedCandidate} />
	<div class="flex flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={solve}>Solve</button>
		<button class="btn variant-filled-primary" on:click={playSolution}>Play</button>
		<button class="btn variant-filled-primary" on:click={reverseSolution}>Reverse</button>
	</div>
	<SolutionInfo {solution} {candidateClicked} {eliminationClicked} />
</div>
