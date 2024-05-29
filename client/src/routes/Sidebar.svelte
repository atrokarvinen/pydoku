<script lang="ts">
	import { navigating } from '$app/stores';
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { getDrawerStore, getModalStore } from '@skeletonlabs/skeleton';
	import SudokuExport from './export/SudokuExport.svelte';

	const drawerStore = getDrawerStore();
	const modalStore = getModalStore();

	$: sudoku = $sudokuStore ?? [];
	$: {
		if ($modalStore[0]) {
			drawerStore.close();
		} else if ($navigating) {
			drawerStore.close();
		}
	}
</script>

<div class="p-1 space-y-5">
	<div class="flex flex-row justify-end">
		<button class="btn-icon variant-ghost-primary" on:click={drawerStore.close}
			><i class="fas fa-close" /></button
		>
	</div>
	<div class="flex flex-col gap-2 items-end">
		<a class="btn variant-ghost-primary" href="/import">
			<i class="fas fa-file-import" />
			<span>Import</span>
		</a>
		<SudokuExport {sudoku} />
		<a class="btn variant-ghost-primary" href="/settings">
			<i class="fas fa-cog" />
			<span>Solver settings</span>
		</a>
	</div>
</div>
