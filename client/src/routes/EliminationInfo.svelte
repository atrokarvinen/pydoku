<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';

	export let eliminations: Elimination[];
	export let eliminationClicked: (elimination: Elimination) => void;
</script>

<div class="flex flex-col gap-5 h-96 overflow-auto">
	<span>Found ({eliminations.length}) eliminations.</span>
	{#each eliminations as elimination}
		<div>
			<button on:click={() => eliminationClicked(elimination)}>
				<span>{`(${elimination.column + 1}, ${elimination.row + 1})`}</span>
				<span>{`number: ${elimination.number}`}</span>
				<span
					>{`caused by: (${elimination.causedBy.column + 1}, ${elimination.causedBy.row + 1})`}</span
				>
			</button>
		</div>
	{/each}
</div>
