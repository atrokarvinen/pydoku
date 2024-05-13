<script lang="ts">
	import type { Sudoku } from '$lib/types/sudoku';
	import { getModalStore } from '@skeletonlabs/skeleton';

	export let sudoku: Sudoku;

	const modalStore = getModalStore();
	const exportSudoku = () => {
		modalStore.trigger({
			type: 'component',
			component: 'ExportModal',
			meta: { sudoku }
		});
	};
</script>

<button class="btn variant-filled-primary" on:click={exportSudoku}>Export</button>
