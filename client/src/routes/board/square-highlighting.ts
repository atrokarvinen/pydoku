import type { Elimination } from '$lib/types/elimination';
import type { HighlightedRegion } from '$lib/types/highlighted-region';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Square, Sudoku } from '$lib/types/sudoku';

export const getHighlightedSquares = (
	solutionStep: Elimination | SingleCandidate | undefined,
	square: Square | undefined,
	sudoku: Sudoku
) => {
	let regions: Square[] = [];
	let rectangles: Square[] = [];
	if (solutionStep) {
		regions = highlightRegionFromSolutionStep(solutionStep, sudoku);
		rectangles = highlightRectangleFromSolutionStep(solutionStep, sudoku);
	} else if (square) {
		regions = highlightFromSelectedSquare(square, sudoku);
	}
	return [...regions, ...rectangles];
};

const highlightRegionFromSolutionStep = (
	elimination: Elimination | SingleCandidate,
	sudoku: Sudoku
) => {
	const regions = elimination.highlightedRegions;
	return highlightFromRegions(regions, sudoku);
};

const highlightFromRegions = (regions: HighlightedRegion[], sudoku: Sudoku) => {
	const highlightedSquares = regions
		.map((region) => {
			if (region.type === 'row') {
				return getHighlightedRow(region.value, sudoku);
			} else if (region.type === 'column') {
				return getHighlightedColumn(region.value, sudoku);
			} else if (region.type === 'box') {
				return getHighlightedBox(region.value, sudoku);
			} else {
				throw new Error('Invalid region type');
			}
		})
		.flat();
	return highlightedSquares;
};

const highlightFromSelectedSquare = (square: Square, sudoku: Sudoku) => {
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

const highlightRectangleFromSolutionStep = (
	solutionStep: Elimination | SingleCandidate,
	sudoku: Sudoku
) => {
	const rects = solutionStep.highlightedRectangles;
	const squares: Square[] = [];
	for (const rect of rects) {
		const { start, end } = rect;
		const rowRange = Array.from({ length: end.row - start.row + 1 }, (_, i) => i + start.row);
		const columnRange = Array.from(
			{ length: end.column - start.column + 1 },
			(_, i) => i + start.column
		);
		const rectSquares = rowRange
			.map((row) => columnRange.map((column) => sudoku[row][column]))
			.flat();
		squares.push(...rectSquares);
	}
	return squares;
};
