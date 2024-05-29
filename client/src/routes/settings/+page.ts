import { axios } from '$lib/axios';
import type { Settings } from './settings';

export const load = async () => {
	const loadPromise = axios.get<Settings>('/settings');
	return { loadPromise };
};
