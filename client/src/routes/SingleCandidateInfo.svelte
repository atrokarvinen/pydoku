<script lang="ts">
	import type { SingleCandidate } from '$lib/types/single-candidate';

	export let singleCandidates: SingleCandidate[];
</script>

<div class="flex flex-col gap-5 h-96 overflow-auto">
	<span>Found ({singleCandidates.length}) single candidates.</span>
	{#each singleCandidates as singleCandidate}
		<div>
			<button>
				<span>{`(${singleCandidate.column + 1}, ${singleCandidate.row + 1})`}</span>
				<span>{`number: ${singleCandidate.number}`}</span>
			</button>
		</div>
	{/each}
</div>
