<script lang="ts">
	import { goto } from '$app/navigation';
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import ImportButton from '../common/ImportButton.svelte';
	import { importFromPreset } from '../common/api';
	import PresetSelector from './PresetSelector.svelte';
	import type { PresetSudoku } from './preset-sudoku';

	const toastStore = getToastStore();

	export let presets: PresetSudoku[];

	let selectedValue: string;

	$: selectedPreset = presets.find((preset) => preset.id === selectedValue);
</script>

<div class="flex flex-col gap-2 w-full">
	<p>Select from preset sudokus.</p>

	<form class="flex flex-col gap-5 mt-10 items-end">
		<PresetSelector {presets} bind:value={selectedValue} />
		<ImportButton
			disabled={!selectedPreset}
			importFunction={() => importFromPreset(selectedPreset?.id)}
			onSuccess={(sudoku) => {
				sudokuStore.set(sudoku);
				goto('/');
			}}
			onError={(error) => {
				console.log('error importing from preset', error);
				toastStore.trigger({
					message: 'Error importing sudoku from preset',
					autohide: true,
					timeout: 5000,
					background: 'bg-error-500'
				});
			}}
		/>
	</form>
</div>
