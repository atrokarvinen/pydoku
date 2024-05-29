import { getToastStore } from '@skeletonlabs/skeleton';

export const triggerFadingError = (message: string) => {
	const toastStore = getToastStore();
	toastStore.trigger({
		message,
		background: 'bg-error-500',
		autohide: true,
		timeout: 5000
	});
};
