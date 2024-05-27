<script lang="ts">
	import type { Sudoku } from '$lib/types/sudoku';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let disabled: boolean;
	export let importFunction: () => Promise<Sudoku>;
	export let onSuccess: (sudoku: Sudoku) => void;
	export let onError: (error: Error) => void;
	let isLoading = false;

	const importSudoku = async () => {
		isLoading = true;
		try {
			const sudoku = await importFunction();
			onSuccess(sudoku);
		} catch (error: any) {
			onError(error);
		} finally {
			isLoading = false;
		}
	};
</script>

{#if !isLoading}
	<button class="btn variant-filled-primary" on:click={importSudoku} {disabled}>Import</button>
{:else}
	<button class="btn variant-filled-primary" disabled><ProgressRadial width="w-6" /></button>
{/if}
