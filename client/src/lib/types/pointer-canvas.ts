import type { Pointer } from './pointer';

export type PointerCanvas = {
	x0: number;
	y0: number;
	x1: number;
	y1: number;
	dashed?: boolean;
	color?: string;
	bidirectional?: boolean;
};

export const pointerToPointerCanvas = (pointer: Pointer, squareSizePx: number): PointerCanvas => {
	return {
		x0: resize(pointer.start.column, squareSizePx),
		y0: resize(pointer.start.row, squareSizePx),
		x1: resize(pointer.end.column, squareSizePx),
		y1: resize(pointer.end.row, squareSizePx),
		dashed: pointer.dashed,
		color: pointer.color,
		bidirectional: pointer.bidirectional
	};
};

const resize = (length: number, squareSizePx: number) => {
	return length * squareSizePx + squareSizePx / 2;
};
