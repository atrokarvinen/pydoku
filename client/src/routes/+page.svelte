<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import Game from './Game.svelte';

	export let data;

	$: sudoku = data.sudoku;
</script>

{#if !sudoku}
	<div class="flex items-center justify-center h-full">
		<ProgressRadial width="w-16" />
	</div>
{:else}
	<Game {sudoku} />
{/if}
