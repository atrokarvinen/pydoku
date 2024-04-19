<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Sudoku } from '$lib/types/sudoku';
	import EliminationInfo from './EliminationInfo.svelte';
	import SingleCandidateInfo from './SingleCandidateInfo.svelte';
	import SudokuBoard from './SudokuBoard.svelte';
	export let sudoku: Sudoku;
	let eliminations: Elimination[] = [];
	let selectedElimination: Elimination | undefined;
	let singleCandidates: SingleCandidate[] = [];

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
		const response = await axios.post<Sudoku>('/sudoku/all-scan', { sudoku });
		sudoku = response.data;
	};

	const singleCandidate = async () => {
		const response = await axios.post<SingleCandidate[]>('/sudoku/single-candidate', { sudoku });
		singleCandidates = response.data;
	};

	const isSolved = async () => {
		const response = await axios.post('/sudoku/is-solved', { sudoku });
		const errors = response.data;
	};

	const applyEliminations = () => {
		eliminations.forEach((elimination) => {
			const { row, column, number } = elimination;
			const square = sudoku[row][column];
			square.possibleNumbers = square.possibleNumbers.filter((n) => n !== number);
			sudoku = sudoku;
		});
	};

	const eliminationClicked = (elimination: Elimination) => {
		selectedElimination = elimination;
	};

	const applySingleCandidates = () => {
		singleCandidates.forEach((singleCandidate) => {
			const { row, column, number } = singleCandidate;
			sudoku[row][column].number = number;
			sudoku = sudoku;
		});
	};
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} {selectedElimination} />
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
