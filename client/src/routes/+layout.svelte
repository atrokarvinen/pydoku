<script lang="ts">
	import { AppBar, AppShell, Modal, initializeStores } from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import ImportModal from './import/ImportModal.svelte';

	initializeStores();

	const modalRegistry = {
		ImportModal: { ref: ImportModal }
	};
</script>

<Modal components={modalRegistry} />

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<h1>Sudoku</h1>
		</AppBar>
	</svelte:fragment>
	<div class="md:p-5 p-2 flex items-center justify-center">
		<slot />
	</div>
</AppShell>
