import { axios } from '$lib/axios';
import type { PresetSudoku } from './preset-sudoku';

export const load = async () => {
	try {
		const loadPromise = axios.get<PresetSudoku[]>('/import/preset');
		return { loadPromise, error: undefined };
	} catch (error) {
		console.log('load presets error: ', error);
		return { presets: [], error: error as any };
	}
};
