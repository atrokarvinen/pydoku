export const triggerFadingSuccess = (toastStore: any, message: string) => {
	toastStore.trigger({
		message,
		autohide: true,
		timeout: 5000
	});
};
