<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	export let sudoku: Sudoku;
	export let selectedElimination: Elimination | undefined;

	$: console.log('selectedElimination', selectedElimination);

	$: size = sudoku.length;
</script>

<div class="grid grid-cols-9">
	{#each sudoku as row}
		{#each row as square}
			<SudokuSquare {square} {size} {selectedElimination} />
		{/each}
	{/each}
</div>
