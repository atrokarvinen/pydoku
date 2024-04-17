export type Sudoku = Square[][];

export type Square = {
	row: number;
	column: number;
	number: number;
	possibleNumbers: number[];
};
