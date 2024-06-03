export const triggerFadingSuccess = (toastStore: any, message: string) => {
	toastStore.trigger({
		message,
		// background: 'bg-success-500',
		autohide: true,
		timeout: 5000
	});
};
