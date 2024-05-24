<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Square } from '$lib/types/sudoku';
	import SudokuNotes from './SudokuNotes.svelte';
	import {
		BASE_BORDER_COLOR,
		CAUSING_SQUARE_COLOR,
		HIGHLIGHTED_STYLE,
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
	$: isCausedBy =
		!!selectedElimination &&
		!!selectedElimination.causingSquare &&
		square.row === selectedElimination.causingSquare.row &&
		square.column === selectedElimination.causingSquare.column;
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

	const getOuterBorderClass = (row: number, col: number, size: number) => {
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

	const getInnerBorderClass = (isCausedBy: boolean) => {
		let borderStyle = 'border-solid border-2 ';
		if (isCausedBy) {
			borderStyle += CAUSING_SQUARE_COLOR;
		} else {
			borderStyle += 'border-transparent';
		}
		return borderStyle;
	};

	const getFontClass = (isInitial: boolean) => {
		return isInitial ? INITIAL_NUMBER_STYLE : '';
	};

	const getBackgroundClass = (
		isNumberSelected: boolean,
		isSelected: boolean,
		isHighlighted: boolean
	) => {
		if (isSelected) {
			return SELECTED_STYLE;
		} else if (isHighlighted) {
			return HIGHLIGHTED_STYLE;
		} else if (isNumberSelected) {
			return SELECTED_NUMBER_STYLE;
		}
		return '';
	};
</script>

<div class={getOuterBorderClass(rowNumber, colNumber, size)}>
	<div
		class={`w-full h-full flex ${getInnerBorderClass(isCausedBy)} ${getBackgroundClass(isNumberSelected, isSelected, isHighlighted)}`}
	>
		<button
			class={`text-3xl flex items-center justify-center h-full w-full  ${getFontClass(isInitial)}`}
			on:click={() => squarePressed(square)}
		>
			{#if square.number === 0}
				<SudokuNotes {size} {square} {selectedElimination} {selectedCandidate} {selectedNumber} />
			{:else}
				{square.number}
			{/if}
		</button>
	</div>
</div>
