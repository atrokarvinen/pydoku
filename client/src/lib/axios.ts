import { PUBLIC_BACKEND_BASE_URL } from '$env/static/public';
import base from 'axios';

export const axios = base.create({
	baseURL: PUBLIC_BACKEND_BASE_URL
});
