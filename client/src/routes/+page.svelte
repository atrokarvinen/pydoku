<script lang="ts">
	import { sudokuStore } from '$lib/stores/sudokuStore';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import Game from './Game.svelte';

	export let data;

	$: sudoku = data.sudoku;
	let innerHeight = 0;
	let innerWidth = 0;

	const margin = 20;
	$: widthWithoutMargin = innerWidth - margin;
	$: maxWidth = calculateWidth(widthWithoutMargin);
	$: {
		if ($sudokuStore === undefined) {
			sudokuStore.set(sudoku);
		}
	}

	const calculateWidth = (width: number) => {
		const min = 0;
		const max = 360;
		const divisibleByNine = width - (width % 9);
		return Math.min(max, Math.max(min, divisibleByNine));
	};
</script>

<svelte:window bind:innerHeight bind:innerWidth />

{#if !sudoku}
	<div class="flex items-center justify-center h-full">
		<ProgressRadial width="w-16" />
	</div>
{:else}
	<Game {sudoku} {maxWidth} />
{/if}
