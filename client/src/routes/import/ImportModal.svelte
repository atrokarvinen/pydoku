<script lang="ts">
	import { navigating } from '$app/stores';
	import { getModalStore } from '@skeletonlabs/skeleton';

	export const parent: any = {};

	const modalStore = getModalStore();

	$: {
		if ($navigating) {
			modalStore.close();
		}
	}
</script>

{#if $modalStore[0]}
	<div class="card p-4 w-modal space-y-4 shadow-xl">
		<header class="text-2xl font-bold">Import sudoku</header>
		<p>Choose import type:</p>
		<div class="flex flex-row gap-5">
			<a class="btn variant-filled-primary" href="/import/text">Text</a>
			<a class="btn variant-filled-primary" href="/import/image">Image</a>
			<a class="btn variant-filled-primary" href="/import/preset">Preset</a>
		</div>
		<footer class="modal-footer flex flex-row space-x-2 justify-end">
			<button class="btn variant-filled-secondary" on:click={() => modalStore.close()}>Close</button
			>
		</footer>
	</div>
{/if}
