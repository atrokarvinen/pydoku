import { PUBLIC_BACKEND_BASE_URL } from '$env/static/public';
import base from 'axios';

export const axios = base.create({
	baseURL: PUBLIC_BACKEND_BASE_URL
});

export const setUserIdHeader = (userId: string) => {
	axios.defaults.headers.common['UserId'] = userId;
};

export const clearUserIdHeader = () => {
	axios.defaults.headers.common['UserId'] = '';
};
