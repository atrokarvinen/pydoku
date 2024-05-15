import { axios } from '$lib/axios';
import type { User } from '$lib/types/auth/user';

export const createUser = async () => {
	return axios.get<User>('/auth/create');
};
