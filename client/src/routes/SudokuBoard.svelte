<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	import { getHighlightedSquares } from './square-highlighting';
	export let sudoku: Sudoku;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;
	export let selectedSquare: Square | undefined;
	export let squarePressed: (square: Square) => void;

	$: size = sudoku.length;

	$: highlightedSquares = getHighlightedSquares(
		selectedElimination,
		selectedCandidate,
		selectedSquare,
		sudoku
	);
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
				{selectedSquare}
				{highlightedSquares}
				{squarePressed}
			/>
		{/each}
	{/each}
</div>
