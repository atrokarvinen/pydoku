<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Sudoku } from '$lib/types/sudoku';
	import { getModalStore } from '@skeletonlabs/skeleton';

	export let parent: any;

	const modalStore = getModalStore();
	let file: File;
	let files: FileList;

	const importSudoku = async () => {
		if (!files || files.length === 0) {
			return;
		}

		const formData = new FormData();
		formData.append('file', files[0]);

		try {
			const response = await axios.postForm<Sudoku>('/sudoku/import', formData);
			// console.log('response: ', response);
			const sudoku = response.data;
			if (!$modalStore[0]) console.log('modalStore[0] is undefined');
			if (!$modalStore[0].response) console.log('modalStore[0].response is undefined');
			if (parent?.response) console.log('parent has response');

			if ($modalStore[0] && $modalStore[0].response) {
				$modalStore[0].response(sudoku);
				modalStore.close();
			}
		} catch (error) {
			console.log('import sudoku error: ', error);
		}
	};
</script>

{#if $modalStore[0]}
	<div class="card p-4 w-modal space-y-4 shadow-xl">
		<header class="text-2xl font-bold">Import sudoku</header>
		<div>
			<span> Content </span>
			<input class="input" type="file" bind:value={file} bind:files />
		</div>
		<footer class="modal-footer flex flex-row space-x-2 justify-end">
			<button class="btn variant-filled-secondary" on:click={() => modalStore.close()}>Close</button
			>
			<button class="btn variant-filled-primary" on:click={importSudoku}>Import</button>
		</footer>
	</div>
{/if}
