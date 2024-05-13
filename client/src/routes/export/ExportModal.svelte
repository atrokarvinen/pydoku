<script lang="ts">
	import type { Sudoku } from '$lib/types/sudoku';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import CopyInput from './CopyInput.svelte';

	export const parent: any = {};

	const modalStore = getModalStore();

	$: meta = $modalStore[0]?.meta;
	$: sudoku = meta?.sudoku as Sudoku;
	$: sudokuString = sudokuToString(sudoku);

	const sudokuToString = (sudoku: Sudoku) => {
		if (sudoku === undefined) {
			return '';
		}
		return sudoku
			.map((row) => row.map((square) => square.number))
			.flat()
			.map((number) => (number === 0 ? '.' : number.toString()))
			.join('');
	};
</script>

{#if $modalStore[0]}
	<div class="card p-4 w-modal space-y-4 shadow-xl">
		<header class="text-2xl font-bold">Export sudoku</header>
		<div>
			<span> Sudoku as string:</span>
			<CopyInput text={sudokuString} />
		</div>
		<footer class="modal-footer flex flex-row space-x-2 justify-end">
			<button class="btn variant-filled-secondary" on:click={() => modalStore.close()}>Close</button
			>
		</footer>
	</div>
{/if}
