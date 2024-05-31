import { AxiosError, isAxiosError } from 'axios';

export const getApiErrorMessage = (error: any, fallback: string = ''): string => {
	if (isAxiosError(error)) {
		const axiosError = error as AxiosError;
		const errorData = axiosError.response?.data;
		const errorMessage = (errorData as any)?.message;
		if (errorMessage) {
			return errorMessage;
		}
	}
	return fallback ? fallback : 'An error occurred';
};
