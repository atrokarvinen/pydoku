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
		<a class="btn-icon variant-ghost-primary" href="/">
			<i class="fas fa-home" />
		</a>
	</svelte:fragment>
	<svelte:fragment slot="trail"
		><button class="btn-icon variant-ghost-primary" on:click={onBarsClicked}
			><i class="fas fa-bars" /></button
		></svelte:fragment
	>
</AppBar>
