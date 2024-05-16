<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square } from '$lib/types/sudoku';
	import SudokuNote from './SudokuNote.svelte';
	import {
		BASE_BORDER_COLOR,
		CANDIDATE_COLOR,
		CAUSING_SQUARE_COLOR,
		INITIAL_NUMBER_STYLE,
		SELECTED_NUMBER_STYLE,
		SELECTED_STYLE
	} from './theme';

	export let square: Square;
	export let size: number;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;
	export let selectedSquare: Square | undefined;
	export let highlightedSquares: Square[];
	export let squarePressed: (square: Square) => void;

	$: rowNumber = square.row;
	$: colNumber = square.column;
	$: candidateSquare = selectedCandidate
		? {
				row: selectedCandidate.row,
				column: selectedCandidate.column
			}
		: undefined;
	$: isCausedBy =
		!!selectedElimination &&
		!!selectedElimination.causingSquare &&
		square.row === selectedElimination.causingSquare.row &&
		square.column === selectedElimination.causingSquare.column;
	$: isCandidate =
		!!candidateSquare &&
		square.row === candidateSquare.row &&
		square.column === candidateSquare.column;
	$: isSelected =
		!!selectedSquare &&
		square.row === selectedSquare.row &&
		square.column === selectedSquare.column;
	$: isNumberSelected = !!selectedNumber && square.number === selectedNumber;
	$: isHighlighted = highlightedSquares.some(
		(highlightedSquare) =>
			highlightedSquare.row === square.row && highlightedSquare.column === square.column
	);
	$: isInitial = square.isInitial;

	const getBorderClass = (row: number, col: number, size: number) => {
		let borderStyle = 'flex items-center justify-center h-10 w-10 border-solid border ';
		borderStyle += BASE_BORDER_COLOR + ' ';
		const boxSize = Math.sqrt(size);
		if (row % boxSize === 0) {
			borderStyle += 'border-t-2 ';
		}
		if (row === size - 1) {
			borderStyle += 'border-b-2 ';
		}
		if (col % boxSize === 0) {
			borderStyle += 'border-l-2 ';
		}
		if (col === size - 1) {
			borderStyle += 'border-r-2 ';
		}
		return borderStyle;
	};

	const getInnerBorderClass = (isCausedBy: boolean, isCandidate: boolean) => {
		let borderStyle = 'border-solid border-2 ';
		if (isCausedBy) {
			borderStyle += CAUSING_SQUARE_COLOR;
		} else if (isCandidate) {
			borderStyle += CANDIDATE_COLOR;
		} else {
			borderStyle += 'border-transparent';
		}
		return borderStyle;
	};

	const getFontClass = (isInitial: boolean) => {
		return isInitial ? INITIAL_NUMBER_STYLE : '';
	};

	const getSelectedClass = (
		isNumberSelected: boolean,
		isSelected: boolean,
		isHighlighted: boolean
	) => {
		if (isSelected) {
			return SELECTED_STYLE;
		} else if (isHighlighted) {
			return 'bg-gray-200';
		} else if (isNumberSelected) {
			return SELECTED_NUMBER_STYLE;
		}
		return '';
	};

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

	$: possibleNotes = Array.from({ length: size }, (_, i) => i + 1);
</script>

<div class={getBorderClass(rowNumber, colNumber, size)}>
	<div class={`w-full h-full ${getInnerBorderClass(isCausedBy, isCandidate)} flex`}>
		{#if square.number === 0}
			<button class={`w-full h-full`}>
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
			</button>
		{:else}
			<button
				class={`text-3xl flex items-center justify-center h-full w-full ${getSelectedClass(isNumberSelected, isSelected, isHighlighted)} ${getFontClass(isInitial)}`}
				on:click={() => squarePressed(square)}
			>
				{square.number}
			</button>
		{/if}
	</div>
</div>
