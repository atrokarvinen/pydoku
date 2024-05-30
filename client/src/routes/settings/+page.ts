import { axios } from '$lib/axios';
import type { Settings } from './settings';

export const ssr = false;

export const load = async ({ parent }) => {
	try {
		await parent();
		console.log('loading settings...');
		const loadPromise = axios.get<Settings>('/settings');
		return { loadPromise };
	} catch (error) {
		return { error };
	}
};
