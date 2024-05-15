<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import Game from './Game.svelte';

	export let data;

	$: sudoku = data.sudoku;
</script>

{#if !sudoku}
	<ProgressRadial width="w-16" />
{:else}
	<Game {sudoku} />
{/if}
