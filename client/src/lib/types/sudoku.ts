export type Sudoku = Square[][];

export type Square = {
	row: number;
	column: number;
	number: number;
	box: number;
	isInitial: boolean;
	possibleNumbers: number[];
};

export const emptySudoku9x9: Sudoku = Array.from({ length: 9 }, (_, row) =>
	Array.from({ length: 9 }, (_, column) => {
		const square: Square = {
			row,
			column,
			box: Math.floor(row / 3) * 3 + Math.floor(column / 3),
			number: 0,
			isInitial: false,
			possibleNumbers: []
		};
		return square;
	})
);
