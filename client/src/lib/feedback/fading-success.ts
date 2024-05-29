import { getToastStore } from '@skeletonlabs/skeleton';

export const triggerFadingSuccess = (message: string) => {
	const toastStore = getToastStore();
	toastStore.trigger({
		message,
		background: 'bg-success-500',
		autohide: true,
		timeout: 5000
	});
};
