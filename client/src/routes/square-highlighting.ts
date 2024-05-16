import type { Elimination } from '$lib/types/elimination';
import type { HighlightedRegion } from '$lib/types/highlighted-region';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Square, Sudoku } from '$lib/types/sudoku';

export const getHighlightedSquares = (
	elimination: Elimination | undefined,
	candidate: SingleCandidate | undefined,
	square: Square | undefined,
	sudoku: Sudoku
) => {
	if (elimination) {
		return highlightFromElimination(elimination, sudoku);
	} else if (candidate) {
		return highlightFromCandidate(candidate, sudoku);
	} else if (square) {
		return highlightFromSelectedSquare(square, sudoku);
	}
	return [];
};

const highlightFromElimination = (elimination: Elimination, sudoku: Sudoku) => {
	const regions = elimination.highlightedRegions;
	return highlightFromRegions(regions, sudoku);
};

const highlightFromCandidate = (candidate: SingleCandidate, sudoku: Sudoku) => {
	const regions = candidate.highlightedRegions;
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
