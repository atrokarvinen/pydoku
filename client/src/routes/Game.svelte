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
</script>

<div class="flex flex-col gap-5">
	<SudokuBoard {sudoku} />
	<div class="flex flex-row gap-5">
		<button class="btn variant-filled-primary" on:click={fillNotes}>Notes</button>
		<button class="btn variant-filled-primary" on:click={rowScan}>Row scan</button>
	</div>
</div>
