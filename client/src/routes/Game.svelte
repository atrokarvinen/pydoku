<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Sudoku } from '$lib/types/sudoku';
	import SudokuBoard from './SudokuBoard.svelte';
	export let sudoku: Sudoku;

	const fillNotes = async () => {
		const response = await axios.get<Sudoku>('/sudoku/notes');
		sudoku = response.data;
	};

	const rowScan = async () => {
		const response = await axios.post<Sudoku>('/sudoku/row-scan', { sudoku });
		sudoku = response.data;
	};

	const columnScan = async () => {
		const response = await axios.post<Sudoku>('/sudoku/column-scan', { sudoku });
		sudoku = response.data;
	};

	const boxScan = async () => {
		const response = await axios.post<Sudoku>('/sudoku/box-scan', { sudoku });
		sudoku = response.data;
	};

	const allScan = async () => {
		const response = await axios.post<Sudoku>('/sudoku/all-scan', { sudoku });
		sudoku = response.data;
	};

	const singleCandidate = async () => {
		const response = await axios.post<Sudoku>('/sudoku/single-candidate', { sudoku });
		sudoku = response.data;
	};

	const isSolved = async () => {
		const response = await axios.post('/sudoku/is-solved', { sudoku });
		const errors = response.data;
	};
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} />
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
