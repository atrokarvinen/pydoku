<script lang="ts">
	import type { Solution } from '$lib/types/solution';

	export let solution: Solution;
</script>

<div class="flex flex-col gap-5 h-96 overflow-auto">
	<span>Found ({solution.singleCandidates.length}) single candidates.</span>
	{#each solution.singleCandidates as singleCandidate}
		<div>
			<button>
				<span>{`(${singleCandidate.column + 1}, ${singleCandidate.row + 1})`}</span>
				<span>{`number: ${singleCandidate.number}`}</span>
			</button>
		</div>
	{/each}
</div>
