export type Sudoku = Square[][];

export type Square = {
	row: number;
	column: number;
	number: number;
	possibleNumbers: number[];
};

export const emptySudoku9x9: Sudoku = Array.from({ length: 9 }, (_, row) =>
	Array.from({ length: 9 }, (_, column) => {
		const square: Square = {
			row,
			column,
			number: 0,
			possibleNumbers: []
		};
		return square;
	})
);
