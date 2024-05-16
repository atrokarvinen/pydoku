<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square, Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	export let sudoku: Sudoku;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;
	export let selectedSquare: Square | undefined;
	export let squarePressed: (square: Square) => void;

	$: size = sudoku.length;

	$: highlightedSquares = getHighlightedSquares(selectedSquare, sudoku);

	const getHighlightedSquares = (square: Square | undefined, sudoku: Sudoku) => {
		if (!square) {
			return [];
		}
		const highlightedRow = getHighlightedRow(square.row, sudoku);
		const highlightedColumn = getHighlightedColumn(square.column, sudoku);
		const highlightedBox = getHighlightedBox(square.box, sudoku);
		const highlightedSquares = [...highlightedRow, ...highlightedColumn, ...highlightedBox];
		return highlightedSquares;
	};

	const getHighlightedRow = (row: number, sudoku: Sudoku) => {
		return sudoku[row];
	};

	const getHighlightedColumn = (column: number, sudoku: Sudoku) => {
		return sudoku.map((row) => row[column]);
	};

	const getHighlightedBox = (box: number, sudoku: Sudoku) => {
		return sudoku.map((row) => row.filter((square) => square.box === box)).flat();
	};
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
