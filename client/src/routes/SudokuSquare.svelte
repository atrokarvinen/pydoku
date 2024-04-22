<script lang="ts">
	import type { EliminationGroup } from '$lib/types/elimination-group';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square } from '$lib/types/sudoku';
	import SudokuNote from './SudokuNote.svelte';

	export let square: Square;
	export let size: number;
	export let selectedElimination: EliminationGroup | undefined;
	export let selectedCandidate: SingleCandidate | undefined;

	$: rowNumber = square.row;
	$: colNumber = square.column;
	$: targetSquare = selectedElimination
		? {
				row: selectedElimination.row,
				column: selectedElimination.column
			}
		: undefined;
	$: targetNote = selectedElimination?.number;
	$: candidateSquare = selectedCandidate
		? {
				row: selectedCandidate.row,
				column: selectedCandidate.column
			}
		: undefined;
	$: isCausedBy =
		!!selectedElimination &&
		square.row === selectedElimination.row &&
		square.column === selectedElimination.column;
	$: isCandidate =
		!!candidateSquare &&
		square.row === candidateSquare.row &&
		square.column === candidateSquare.column;

	const getBorderClass = (
		row: number,
		col: number,
		size: number,
		isCausedBy: boolean,
		isCandidate: boolean
	) => {
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
		if (isCandidate) {
			borderStyle += ' border-green-500';
		}
		return borderStyle;
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
</script>

<div class={getBorderClass(rowNumber, colNumber, size, isCausedBy, isCandidate)}>
	{#if square.number === 0}
		<button class="w-full h-full p-0.5">
			<div class="w-full h-full position: relative">
				{#each square.possibleNumbers as note}
					<SudokuNote {note} isEliminated={isNoteEliminated(note, square.row, square.column)} />
				{/each}
			</div>
		</button>
	{:else}
		<span class="text-3xl">
			{square.number}
		</span>
	{/if}
</div>
