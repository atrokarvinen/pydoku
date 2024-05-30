export const triggerFadingError = (toastStore: any, message: string) => {
	toastStore.trigger({
		message,
		background: 'bg-error-500',
		autohide: true,
		timeout: 5000
	});
};
