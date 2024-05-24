<script lang="ts">
	import { AppBar, getDrawerStore } from '@skeletonlabs/skeleton';

	const drawerStore = getDrawerStore();

	const onBarsClicked = () => {
		drawerStore.open({ id: 'sidebar' });
	};
</script>

<AppBar
	gridColumns="grid-cols-3"
	slotDefault="place-self-center"
	slotTrail="place-content-end"
	padding="p-1"
	regionRowMain="md:w-96"
>
	<svelte:fragment slot="lead">
		<button class="btn-icon variant-ghost-primary">
			<i class="fas fa-home" />
		</button>
	</svelte:fragment>
	<h1 class="h3">Sudoku</h1>
	<svelte:fragment slot="trail"
		><button class="btn-icon variant-ghost-primary" on:click={onBarsClicked}
			><i class="fas fa-bars" /></button
		></svelte:fragment
	>
</AppBar>
