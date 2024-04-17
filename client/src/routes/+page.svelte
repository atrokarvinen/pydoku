<script lang="ts">
	import { axios } from '$lib/axios';
	import type { Sudoku } from '$lib/types';
	export let data;

	$: sudoku = data.sudoku;
	$: size = sudoku?.length || 0;

	const getBorderStyle = (row: number, col: number, size: number) => {
		let borderStyle = ' border-solid border border-black';
		const dividerSize = Math.sqrt(size);
		if (row % dividerSize === 0) {
			borderStyle += ' border-t-2';
		}
		if (row === size - 1) {
			borderStyle += ' border-b-2';
		}
		if (col % dividerSize === 0) {
			borderStyle += ' border-l-2';
		}
		if (col === size - 1) {
			borderStyle += ' border-r-2';
		}
		return borderStyle;
	};

	const getNoteStyle = (note: number) => {
		let noteStyle = 'position: absolute text-center';
		if (note === 1 || note === 4 || note === 7) {
			noteStyle += ' left-0';
		} else if (note === 2 || note === 5 || note === 8) {
			//middle
			noteStyle += ' left-1/2 transform -translate-x-1/2';
		} else {
			noteStyle += ' right-0';
		}
		if (note === 1 || note === 2 || note === 3) {
			noteStyle += ' top-0';
		} else if (note === 4 || note === 5 || note === 6) {
			//middle
			noteStyle += ' top-1/2 transform -translate-y-1/2';
		} else {
			noteStyle += ' bottom-0';
		}
		return noteStyle;
	};

	const fillNotes = async () => {
		const response = await axios.get<Sudoku>('/sudoku/notes');
		console.log('received response');
		sudoku = response.data;
	};
</script>

{#if !sudoku}
	Loading...
{:else}
	<div class="flex flex-col gap-5">
		<div class="grid grid-cols-9">
			{#each sudoku as row, rowNumber}
				{#each row as cell, colNumber}
					<div
						class={'flex items-center justify-center h-10 w-10' +
							getBorderStyle(rowNumber, colNumber, size)}
					>
						{#if cell.number === 0}
							<div class="w-full h-full p-0.5">
								<div class="w-full h-full position: relative">
									{#each cell.possibleNumbers as note}
										<span class={getNoteStyle(note)} style="font-size: xx-small; line-height: 1;"
											>{note}</span
										>
									{/each}
								</div>
							</div>
						{:else}
							<span>
								{cell.number}
							</span>
						{/if}
					</div>
				{/each}
			{/each}
		</div>
		<div>
			<button class="btn variant-filled-primary" on:click={fillNotes}>Notes</button>
		</div>
	</div>
{/if}
