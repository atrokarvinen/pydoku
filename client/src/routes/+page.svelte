<script lang="ts">
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import Game from './Game.svelte';

	export let data;

	$: existingSudoku = data.sudoku;
	$: importedSudoku = $sudokuStore;
	$: sudoku = importedSudoku ?? existingSudoku;
	$: {
		sudokuStore.set(existingSudoku);
	}
</script>

{#if !sudoku}
	<div class="flex items-center justify-center h-full">
		<ProgressRadial width="w-16" />
	</div>
{:else}
	<Game {sudoku} />
{/if}
