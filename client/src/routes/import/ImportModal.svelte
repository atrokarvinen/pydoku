<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Sudoku } from '$lib/types/sudoku';
	import { ProgressRadial, getModalStore } from '@skeletonlabs/skeleton';

	export const parent: any = {};

	const modalStore = getModalStore();
	let file: File;
	let files: FileList;

	let isLoading = false;

	const importSudoku = async () => {
		if (!files || files.length === 0) {
			return;
		}

		isLoading = true;

		const formData = new FormData();
		formData.append('file', files[0]);

		try {
			const response = await axios.postForm<Sudoku>('/sudoku/import', formData);
			const sudoku = response.data;
			if ($modalStore[0] && $modalStore[0].response) {
				$modalStore[0].response(sudoku);
				modalStore.close();
			}
		} catch (error) {
			console.log('import sudoku error: ', error);
		} finally {
			isLoading = false;
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
			{#if !isLoading}
				<button
					class="btn variant-filled-primary"
					on:click={importSudoku}
					disabled={!files || files.length === 0}>Import</button
				>
			{:else}
				<button class="btn variant-filled-primary" disabled><ProgressRadial width="w-6" /></button>
			{/if}
		</footer>
	</div>
{/if}
