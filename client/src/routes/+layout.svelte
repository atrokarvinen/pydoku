<script lang="ts">
	import {
		AppShell,
		Drawer,
		Modal,
		Toast,
		getDrawerStore,
		initializeStores
	} from '@skeletonlabs/skeleton';
	import '../app.postcss';
	import Header from './Header.svelte';
	import Sidebar from './Sidebar.svelte';
	import ExportModal from './export/ExportModal.svelte';
	import ImportModal from './import/ImportModal.svelte';

	initializeStores();

	const modalRegistry = {
		ImportModal: { ref: ImportModal },
		ExportModal: { ref: ExportModal }
	};

	const drawerStore = getDrawerStore();
</script>

<Modal components={modalRegistry} />
<Drawer position="right" width="w-64">
	{#if $drawerStore.id === 'sidebar'}
		<Sidebar />
	{/if}
</Drawer>
<Toast position="t" />

<div class="w-screen h-screen">
	<AppShell
		slotHeader="md:flex flex-row justify-center bg-surface-100-800-token"
		slotPageContent="md:p-5 md:pt-2 p-2 max-h-full flex flex-col items-center"
	>
		<svelte:fragment slot="header">
			<Header />
		</svelte:fragment>
		<slot />
	</AppShell>
</div>
