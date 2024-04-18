<script lang="ts">
	import type { Square } from '$lib/types/sudoku';
	import SudokuNote from './SudokuNote.svelte';

	export let square: Square;
	export let size: number;
	$: rowNumber = square.row;
	$: colNumber = square.column;

	const getBorderClass = (row: number, col: number, size: number) => {
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
		return borderStyle;
	};
</script>

<div class={getBorderClass(rowNumber, colNumber, size)}>
	{#if square.number === 0}
		<button class="w-full h-full p-0.5">
			<div class="w-full h-full position: relative">
				{#each square.possibleNumbers as note}
					<SudokuNote {note} />
				{/each}
			</div>
		</button>
	{:else}
		<span class="text-3xl">
			{square.number}
		</span>
	{/if}
</div>
