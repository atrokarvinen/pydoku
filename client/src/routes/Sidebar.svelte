<script lang="ts">
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import type { Sudoku } from '$lib/types/sudoku';
	import { getDrawerStore } from '@skeletonlabs/skeleton';
	import SudokuExport from './export/SudokuExport.svelte';
	import SudokuImport from './import/SudokuImport.svelte';

	const drawerStore = getDrawerStore();

	$: sudoku = $sudokuStore ?? [];

	const onSudokuImported = (sudoku: Sudoku) => {
		if (!sudoku) return;
		sudokuStore.set(sudoku);
		drawerStore.close();
	};
</script>

<div class="p-1 space-y-5">
	<div class="flex flex-row justify-end">
		<button class="btn-icon variant-ghost-primary" on:click={drawerStore.close}
			><i class="fas fa-close" /></button
		>
	</div>
	<div class="flex flex-col gap-2 items-end">
		<SudokuImport {onSudokuImported} />
		<SudokuExport {sudoku} />
	</div>
</div>
