<script lang="ts">
	import { AppBar, AppShell, Modal, initializeStores } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import ExportModal from './export/ExportModal.svelte';
	import ImportModal from './import/ImportModal.svelte';

	initializeStores();

	const modalRegistry = {
		ImportModal: { ref: ImportModal },
		ExportModal: { ref: ExportModal }
	};
</script>

<Modal components={modalRegistry} />

<div class="w-screen h-screen">
	<AppShell slotPageContent="md:p-5 md:pt-2 p-2 max-h-full flex flex-col items-center">
		<svelte:fragment slot="header">
			<AppBar>
				<h1>Sudoku</h1>
			</AppBar>
		</svelte:fragment>
		<slot />
	</AppShell>
</div>
