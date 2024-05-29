<script lang="ts">
	import { axios } from '$lib/axios';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { triggerFadingSuccess } from '$lib/feedback/fading-success';
	import type { Solver } from './solver';

	export let solvers: Solver[];

	const onSave = async () => {
		console.log('Saving solver settings...');
		try {
			const response = await axios.put('/settings', { solvers });
			triggerFadingSuccess('Settings saved');
		} catch (error) {
			console.error('Failed to save settings', error);
			triggerFadingError('Failed to save settings');
		}
	};
</script>

<button class="btn variant-filled-primary" on:click={onSave}>Save</button>
