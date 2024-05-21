import type { Point } from './point';

export type Pointer = {
	start: Point;
	end: Point;
	dash?: boolean;
	color?: string;
	bidirectional?: boolean;
};
