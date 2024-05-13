<script lang="ts">
	import type { Sudoku } from '$lib/types/sudoku';
	import { getModalStore } from '@skeletonlabs/skeleton';

	export let onSudokuImported: (sudoku: Sudoku) => void;

	const modalStore = getModalStore();
	const importSudoku = () => {
		modalStore.trigger({
			type: 'component',
			component: 'ImportModal',
			response: (sudoku: Sudoku) => onSudokuImported(sudoku)
		});
	};
</script>

<button class="btn variant-filled-primary" on:click={importSudoku}>Import</button>
