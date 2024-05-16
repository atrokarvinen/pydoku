<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { Square } from '$lib/types/sudoku';
	import SudokuNote from './SudokuNote.svelte';

	export let size: number;
	export let square: Square;
	export let selectedNumber: number | undefined;
	export let selectedElimination: Elimination | undefined;

	$: possibleNotes = Array.from({ length: size }, (_, i) => i + 1);

	const getContentClassName = (size: number) => {
		let className = 'w-full h-full grid gap-px';
		if (size === 4) {
			className += ' grid-cols-2 grid-rows-2';
		} else if (size === 9) {
			className += ' grid-cols-3 grid-rows-3';
		} else if (size === 16) {
			className += ' grid-cols-4 grid-rows-4';
		}
		return className;
	};

	const isNoteEliminated = (note: number, row: number, col: number) => {
		if (!selectedElimination || !selectedElimination.eliminatedNotes) {
			return false;
		}
		return selectedElimination.eliminatedNotes.some(
			(eliminationNote) =>
				eliminationNote.row === row &&
				eliminationNote.column === col &&
				eliminationNote.number === note
		);
	};

	const isNoteCausing = (note: number, row: number, col: number) => {
		if (!selectedElimination || !selectedElimination.causingNotes) {
			return false;
		}
		return selectedElimination.causingNotes.some(
			(eliminationNote) =>
				eliminationNote.row === row &&
				eliminationNote.column === col &&
				eliminationNote.number === note
		);
	};
</script>

<div class={getContentClassName(size)}>
	{#each possibleNotes as note}
		<div class="flex items-center justify-center">
			{#if square.possibleNumbers.includes(note)}
				<SudokuNote
					{note}
					isEliminated={isNoteEliminated(note, square.row, square.column)}
					isCausing={isNoteCausing(note, square.row, square.column)}
					{selectedNumber}
				/>
			{:else}
				<div />
			{/if}
		</div>
	{/each}
</div>
