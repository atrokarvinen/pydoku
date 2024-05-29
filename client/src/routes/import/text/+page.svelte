<script lang="ts">
	import { goto } from '$app/navigation';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import ImportButton from '../common/ImportButton.svelte';
	import { importFromString } from '../common/api';

	let sudokuString: string;

	const toastStore = getToastStore();
</script>

<div class="flex flex-col gap-2">
	<p>Import a sudoku from a text.</p>
	<p>
		The expected format is a string of 81 characters, where each character represents a cell in the
		sudoku.
	</p>
	<p>Empty cells should be represented by a dot (.), a zero (0) or an empty space (" ").</p>
	<p>Example:</p>
	<textarea readonly style="resize: none;"
		>.785.64.9.69....52...941.6861.2......45.1.....2.....9..567..81..9....6.5281465..3</textarea
	>

	<form class="flex flex-col gap-5 mt-10 items-end">
		<input class="input" type="text" placeholder="Paste sudoku here" bind:value={sudokuString} />
		<ImportButton
			disabled={!sudokuString}
			importFunction={() => importFromString(sudokuString)}
			onSuccess={(sudoku) => {
				sudokuStore.set(sudoku);
				goto('/');
			}}
			onError={(error) => {
				console.log('error importing from string', error);
				triggerFadingError('Error importing sudoku from text');
			}}
		/>
	</form>
</div>
