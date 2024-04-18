<script lang="ts">
	import Game from './Game.svelte';
	export let data;

	$: sudoku = data.sudoku;
</script>

{#if !sudoku}
	Loading...
{:else}
	<Game {sudoku} />
{/if}
