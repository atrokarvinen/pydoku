<script lang="ts">
	import type { Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	export let sudoku: Sudoku;

	$: size = sudoku.length;
</script>

<div class="grid grid-cols-9">
	{#each sudoku as row}
		{#each row as square}
			<SudokuSquare {square} {size} />
		{/each}
	{/each}
</div>
