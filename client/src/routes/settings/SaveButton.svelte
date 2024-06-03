<script lang="ts">
	import { axios } from '$lib/axios';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { triggerFadingSuccess } from '$lib/feedback/fading-success';
	import { ProgressRadial, getToastStore } from '@skeletonlabs/skeleton';
	import type { Solver } from './solver';

	export let solvers: Solver[];

	let loading: boolean = false;

	const toastStore = getToastStore();

	const onSave = async () => {
		console.log('Saving solver settings...');
		loading = true;
		try {
			const response = await axios.put('/settings', { solvers });
			triggerFadingSuccess(toastStore, 'Settings saved');
		} catch (error) {
			console.error('Failed to save settings', error);
			triggerFadingError(toastStore, 'Failed to save settings');
		} finally {
			loading = false;
		}
	};
</script>

<button class="btn variant-filled-primary" on:click={onSave}>
	{#if loading}
		<ProgressRadial width="w-6" />
	{:else}
		<span> Save </span>
	{/if}
</button>
