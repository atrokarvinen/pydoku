<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { defaultSolution, type Solution } from '$lib/types/solution';
	import type { Sudoku } from '$lib/types/sudoku';
	import EliminationInfo from './EliminationInfo.svelte';
	import SingleCandidateInfo from './SingleCandidateInfo.svelte';
	import SolutionInfo from './SolutionInfo.svelte';
	import SudokuBoard from './SudokuBoard.svelte';
	export let sudoku: Sudoku;
	let eliminations: Elimination[] = [];
	let selectedElimination: Elimination | undefined;
	let selectedCandidate: SingleCandidate | undefined;
	let singleCandidates: SingleCandidate[] = [];
	let solution: Solution = defaultSolution;

	const fillNotes = async () => {
		const response = await axios.get<Sudoku>('/sudoku/notes');
		sudoku = response.data;
	};

	const rowScan = async () => {
		const response = await axios.post<Elimination[]>('/sudoku/row-scan', { sudoku });
		eliminations = response.data;
	};

	const columnScan = async () => {
		const response = await axios.post<Elimination[]>('/sudoku/column-scan', { sudoku });
		eliminations = response.data;
	};

	const boxScan = async () => {
		const response = await axios.post<Elimination[]>('/sudoku/box-scan', { sudoku });
		eliminations = response.data;
	};

	const allScan = async () => {
		const response = await axios.post<Elimination[]>('/sudoku/all-scan', { sudoku });
		eliminations = response.data;
	};

	const singleCandidate = async () => {
		const response = await axios.post<SingleCandidate[]>('/sudoku/single-candidate', { sudoku });
		singleCandidates = response.data;
	};

	const isSolved = async () => {
		const response = await axios.post('/sudoku/is-solved', { sudoku });
		const errors = response.data;
	};

	const eliminationClicked = (elimination: Elimination) => {
		selectedElimination = elimination;
	};

	const candidateClicked = (candidate: SingleCandidate) => {
		selectedCandidate = candidate;
	};

	const applyEliminations = () => eliminations.forEach(applyElimination);
	const applyElimination = (elimination: Elimination) => {
		const { row, column, number } = elimination;
		const square = sudoku[row][column];
		square.possibleNumbers = square.possibleNumbers.filter((n) => n !== number);
		sudoku = sudoku;
	};

	const applySingleCandidates = () => singleCandidates.forEach(applySingleCandidate);
	const applySingleCandidate = (singleCandidate: SingleCandidate) => {
		const { row, column, number } = singleCandidate;
		sudoku[row][column].number = number;
		sudoku = sudoku;
	};

	const solve = async () => {
		const response = await axios.post<Solution>('/sudoku/solve', { sudoku });
		solution = response.data;
		sudoku = solution.sudoku;
	};

	const playSolution = async () => {
		const actions: (Elimination | SingleCandidate)[] = [
			...solution.eliminations,
			...solution.singleCandidates
		].sort((a, b) => a.solutionIndex - b.solutionIndex);
		for (const action of actions) {
			const nextIndex = action.solutionIndex;
			const nextElimination = solution.eliminations.find(
				(elimination) => elimination.solutionIndex === nextIndex
			);
			const nextSingleCandidate = solution.singleCandidates.find(
				(singleCandidate) => singleCandidate.solutionIndex === nextIndex
			);
			if (nextElimination) {
				applyElimination(nextElimination);
			} else if (nextSingleCandidate) {
				applySingleCandidate(nextSingleCandidate);
			}
			await new Promise((resolve) => setTimeout(resolve, 20));
		}
	};
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} {selectedElimination} {selectedCandidate} />
	<div class="flex flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={solve}>Solve</button>
		<button class="btn variant-filled-primary" on:click={playSolution}>Play solution</button>
	</div>
	<SolutionInfo {solution} {candidateClicked} {eliminationClicked} />
	<button class="btn variant-filled-primary" on:click={applyEliminations}>Apply eliminations</button
	>
	<EliminationInfo {eliminations} {eliminationClicked} />
	<button class="btn variant-filled-primary" on:click={applySingleCandidates}
		>Apply single candidates</button
	>
	<SingleCandidateInfo {singleCandidates} />
	<div class="flex flex-wrap flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={fillNotes}>Notes</button>
		<button class="btn variant-filled-primary" on:click={rowScan}>Row scan</button>
		<button class="btn variant-filled-primary" on:click={columnScan}>Column scan</button>
		<button class="btn variant-filled-primary" on:click={boxScan}>Box scan</button>
		<button class="btn variant-filled-primary" on:click={allScan}>All scan</button>
		<button class="btn variant-filled-primary" on:click={singleCandidate}>Single candidate</button>
		<button class="btn variant-filled-primary" on:click={isSolved}>Is solved</button>
	</div>
</div>
