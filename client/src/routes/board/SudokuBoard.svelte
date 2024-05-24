<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	import VisualizationCanvas from './VisualizationCanvas.svelte';
	import { getHighlightedSquares } from './square-highlighting';
	export let sudoku: Sudoku;
	export let maxWidth: number;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;
	export let selectedSquare: Square | undefined;
	export let squarePressed: (square: Square) => void;

	$: size = sudoku.length;

	$: highlightedSquares = getHighlightedSquares(
		selectedElimination ?? selectedCandidate,
		selectedSquare,
		sudoku
	);

	$: pointers = selectedElimination?.pointers ?? [];
</script>

<div>
	<VisualizationCanvas {size} {pointers} {maxWidth} />
	<div class="grid grid-cols-9">
		{#each sudoku as row}
			{#each row as square}
				<SudokuSquare
					{square}
					{maxWidth}
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
</div>
