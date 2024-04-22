<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Solution } from '$lib/types/solution';
	import SolutionInfoElimination from './SolutionInfoElimination.svelte';
	import SolutionInfoSingleCandidate from './SolutionInfoSingleCandidate.svelte';

	export let solution: Solution;
	export let eliminationClicked: (elimination: Elimination) => void;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	let actions: (Elimination | SingleCandidate)[] = [];
	$: actions = [...solution.eliminations, ...solution.singleCandidates].sort(
		(a, b) => a.solutionIndex - b.solutionIndex
	);

	const isElimination = (action: Elimination | SingleCandidate) => {
		return solution.eliminations.some((x) => x.solutionIndex === action.solutionIndex);
	};

	const toElimination = (action: Elimination | SingleCandidate) => {
		return action as Elimination;
	};

	const toSingleCandidate = (action: Elimination | SingleCandidate) => {
		return action as SingleCandidate;
	};
</script>

<div class="flex flex-col gap-5 h-96 overflow-auto">
	<span>Solved after ({actions.length}) steps.</span>
	{#each actions as action, step}
		{#if isElimination(action)}
			<SolutionInfoElimination
				step={step + 1}
				elimination={toElimination(action)}
				{eliminationClicked}
			/>
		{:else}
			<SolutionInfoSingleCandidate
				step={step + 1}
				candidate={toSingleCandidate(action)}
				{candidateClicked}
			/>
		{/if}
	{/each}
</div>
