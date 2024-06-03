<script lang="ts">
	import { axios } from '$lib/axios';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { triggerFadingSuccess } from '$lib/feedback/fading-success';
	import { ProgressRadial, getModalStore, getToastStore } from '@skeletonlabs/skeleton';
	import type { Settings } from './settings';
	import type { Solver } from './solver';

	export let onDefaultsRestored: (defaults: Solver[]) => void;

	let loading: boolean = false;

	const modalStore = getModalStore();
	const toastStore = getToastStore();

	const onConfirm = async (confirmed: boolean) => {
		if (!confirmed) return;
		console.log('Restoring defaults');

		loading = true;

		try {
			const response = await axios.get<Settings>('/settings/restore');
			const defaults = response.data.solvers;
			onDefaultsRestored(defaults);
			triggerFadingSuccess(toastStore, 'Defaults restored');
		} catch (error) {
			console.error('Failed to restore defaults', error);
			triggerFadingError(toastStore, 'Failed to restore defaults');
		} finally {
			loading = false;
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

<button class="btn variant-filled-secondary" on:click={confirmRestoreDefaults} disabled={loading}>
	{#if loading}
		<ProgressRadial width="w-6" />
	{:else}
		<span> Restore defaults </span>
	{/if}
</button>
