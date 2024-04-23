<script lang="ts">
	import { getSolutionSteps } from '$lib/sudoku-log/sudoku-log';
	import type { EliminationGroup } from '$lib/types/elimination-group';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Solution } from '$lib/types/solution';
	import SolutionInfoElimination from './SolutionInfoElimination.svelte';
	import SolutionInfoSingleCandidate from './SolutionInfoSingleCandidate.svelte';

	export let solution: Solution;
	export let eliminationClicked: (elimination: EliminationGroup) => void;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	$: solutionSteps = getSolutionSteps(solution);
</script>

<div class="flex flex-col gap-5 h-48 overflow-auto">
	{#if solution.isSolved}
		<span>Solved after ({solutionSteps.length}) steps.</span>
	{:else}
		<span>Unable to solve sudoku</span>
	{/if}
	{#each solutionSteps as action, step}
		{#if action.type === 'elimination'}
			<SolutionInfoElimination step={step + 1} elimination={action} {eliminationClicked} />
		{:else}
			<SolutionInfoSingleCandidate step={step + 1} candidate={action} {candidateClicked} />
		{/if}
	{/each}
</div>
