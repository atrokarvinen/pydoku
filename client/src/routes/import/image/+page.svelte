<script lang="ts">
	import { goto } from '$app/navigation';
	import { getApiErrorMessage } from '$lib/feedback/api-error-parser';
	import { triggerFadingError } from '$lib/feedback/fading-error';
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import ImportButton from '../common/ImportButton.svelte';
	import { importFromImage } from '../common/api';

	let files: FileList | undefined;

	const toastStore = getToastStore();
</script>

<div class="flex flex-col gap-2">
	<p>Import a sudoku from an image.</p>
	<p>
		The image should contain a sudoku puzzle. The app will try to extract the sudoku from the image.
	</p>
	<p>The image recognition works best on sudokus with white background and black numbers.</p>

	<form class="flex flex-col gap-5 mt-10 items-end">
		<input class="input" type="file" bind:files />
		<ImportButton
			disabled={!files || files.length === 0}
			importFunction={() => importFromImage(files)}
			onSuccess={(sudoku) => {
				sudokuStore.set(sudoku);
				goto('/');
			}}
			onError={(error) => {
				const errorMessage = getApiErrorMessage(error, 'Error importing sudoku from image');
				triggerFadingError(toastStore, errorMessage);
			}}
		/>
	</form>
</div>
