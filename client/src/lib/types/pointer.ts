import type { Point } from './point';

export type Pointer = {
	start: Point;
	end: Point;
	dashed?: boolean;
	color?: string;
	bidirectional?: boolean;
};
