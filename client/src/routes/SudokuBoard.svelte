<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	export let sudoku: Sudoku;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;
	export let squarePressed: (square: Square) => void;

	$: size = sudoku.length;
</script>

<div class="grid grid-cols-9">
	{#each sudoku as row}
		{#each row as square}
			<SudokuSquare
				{square}
				{size}
				{selectedElimination}
				{selectedCandidate}
				{selectedNumber}
				{squarePressed}
			/>
		{/each}
	{/each}
</div>
