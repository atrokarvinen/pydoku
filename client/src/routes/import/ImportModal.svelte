<script lang="ts">
	import { ProgressRadial, getModalStore } from '@skeletonlabs/skeleton';
	import { importFromImage, importFromString } from './api';

	export const parent: any = {};

	const modalStore = getModalStore();
	let files: FileList | undefined;

	let isLoading = false;
	let sudokuString: string;
	let fileInput: HTMLInputElement;
	let stringInput: HTMLInputElement;

	$: noSudokuSelected = !sudokuString && (!files || files.length === 0);

	const importSudoku = async () => {
		isLoading = true;

		const isStringImport = !!sudokuString;
		try {
			let sudoku;
			if (isStringImport) {
				sudoku = await importFromString(sudokuString);
			} else {
				sudoku = await importFromImage(files);
			}
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

	const handleFileChange = (e: Event) => {
		const target = e.target as HTMLInputElement;
		if (target.files) {
			stringInput.value = '';
		}
	};
</script>

{#if $modalStore[0]}
	<div class="card p-4 w-modal space-y-4 shadow-xl">
		<header class="text-2xl font-bold">Import sudoku</header>
		<div class="flex flex-col gap-y-5">
			<input
				bind:this={fileInput}
				class="input"
				type="file"
				on:change={handleFileChange}
				bind:files
			/>
			<span> Or </span>
			<input
				class="input"
				type="text"
				placeholder="Paste sudoku here"
				bind:this={stringInput}
				bind:value={sudokuString}
				on:input={() => {
					if (!fileInput) return;
					files = undefined;
					fileInput.value = '';
				}}
			/>
		</div>
		<footer class="modal-footer flex flex-row space-x-2 justify-end">
			<button class="btn variant-filled-secondary" on:click={() => modalStore.close()}>Close</button
			>
			{#if !isLoading}
				<button
					class="btn variant-filled-primary"
					on:click={importSudoku}
					disabled={noSudokuSelected}>Import</button
				>
			{:else}
				<button class="btn variant-filled-primary" disabled><ProgressRadial width="w-6" /></button>
			{/if}
		</footer>
	</div>
{/if}
