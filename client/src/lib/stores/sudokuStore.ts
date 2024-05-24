import type { Sudoku } from '$lib/types/sudoku';
import { writable } from 'svelte/store';

export const sudokuStore = writable<Sudoku | undefined>();
