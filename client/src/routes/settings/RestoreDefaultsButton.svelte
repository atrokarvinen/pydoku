<script lang="ts">
	import { axios } from '$lib/axios';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	import type { Solver } from './solver';

	export let onDefaultsRestored: (defaults: Solver[]) => void;

	const modalStore = getModalStore();
	const toastStore = getToastStore();

	const onConfirm = async (confirmed: boolean) => {
		if (!confirmed) return;
		console.log('Restoring defaults');

		try {
			const response = await axios.post('/api/solvers/restore');
			const defaults = response.data;
			onDefaultsRestored(defaults);
		} catch (error) {
			console.error('Failed to restore defaults', error);
			triggerFadingError(toastStore, 'Failed to restore defaults');
		}
	};

	const confirmRestoreDefaults = () => {
		modalStore.trigger({
			type: 'confirm',
			title: 'Restore defaults',
			body: 'Are you sure?',
			modalClasses: 'w-96',
			response: onConfirm
		});
	};
</script>

<button class="btn variant-filled-secondary" on:click={confirmRestoreDefaults}
	>Restore defaults</button
>
