<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { Square } from '$lib/types/sudoku';
	import SudokuNote from './SudokuNote.svelte';

	export let square: Square;
	export let size: number;
	export let selectedElimination: Elimination | undefined;

	$: rowNumber = square.row;
	$: colNumber = square.column;
	$: causedBy = selectedElimination?.causedBy;
	$: targetSquare = selectedElimination
		? {
				row: selectedElimination.row,
				column: selectedElimination.column
			}
		: undefined;
	$: targetNote = selectedElimination?.number;
	$: isTarget =
		!!targetSquare && square.row === targetSquare.row && square.column === targetSquare.column;
	$: isCausedBy = !!causedBy && square.row === causedBy.row && square.column === causedBy.column;

	const getBorderClass = (row: number, col: number, size: number, isCausedBy: boolean) => {
		const baseStyle = 'flex items-center justify-center h-10 w-10 border-solid border border-black';
		let borderStyle = baseStyle;
		const boxSize = Math.sqrt(size);
		if (row % boxSize === 0) {
			borderStyle += ' border-t-2';
		}
		if (row === size - 1) {
			borderStyle += ' border-b-2';
		}
		if (col % boxSize === 0) {
			borderStyle += ' border-l-2';
		}
		if (col === size - 1) {
			borderStyle += ' border-r-2';
		}
		if (isCausedBy) {
			borderStyle += ' border-red-500';
		}
		return borderStyle;
	};
</script>

<div class={getBorderClass(rowNumber, colNumber, size, isCausedBy)}>
	{#if square.number === 0}
		<button class="w-full h-full p-0.5">
			<div class="w-full h-full position: relative">
				{#each square.possibleNumbers as note}
					<SudokuNote {note} isTarget={isTarget && note === targetNote} />
				{/each}
			</div>
		</button>
	{:else}
		<span class="text-3xl">
			{square.number}
		</span>
	{/if}
</div>
