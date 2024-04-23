<script lang="ts">
	import type { EliminationGroup } from '$lib/types/elimination-group';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Sudoku } from '$lib/types/sudoku';
	import SudokuSquare from './SudokuSquare.svelte';
	export let sudoku: Sudoku;
	export let selectedElimination: EliminationGroup | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let selectedNumber: number | undefined;

	$: size = sudoku.length;
</script>

<div class="grid grid-cols-9">
	{#each sudoku as row}
		{#each row as square}
			<SudokuSquare {square} {size} {selectedElimination} {selectedCandidate} {selectedNumber} />
		{/each}
	{/each}
</div>
