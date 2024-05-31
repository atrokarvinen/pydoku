<script lang="ts">
	import { getSolutionStepsByCount } from '$lib/solution/solution-parser';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Solution } from '$lib/types/solution';
	import type { SolutionGroup } from '$lib/types/solution-menu';
	import { techniqueToString } from './solution-string-conversion';

	export let solution: Solution;
	export let solutionSteps: (Elimination | SingleCandidate)[];
	export let eliminationClicked: (elimination: Elimination) => void;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	$: solutionStepsByCount = getSolutionStepsByCount(solutionSteps);

	const groupClicked = (group: SolutionGroup) => {
		if (group.steps.length === 0) return;
		const firstStep = group.steps[0];
		const solution = firstStep.solution;
		if (solution.type === 'elimination') {
			eliminationClicked(solution);
		} else {
			candidateClicked(solution);
		}
	};
</script>

<div class="flex flex-col gap-y-2">
	{#if solution.isSolved}
		<span>Solved after ({solutionSteps.length}) steps.</span>
	{:else if solution.isSolved === false}
		<span class="text-error-500 font-bold">Unable to solve sudoku</span>
	{/if}
	{#each solutionStepsByCount.groups as group}
		<div class="flex flex-row gap-5 items-center">
			<span class="font-bold w-48">{techniqueToString(group.technique)} ({group.steps.length})</span
			>
			<button class="btn-icon-sm rounded-full variant-filled" on:click={() => groupClicked(group)}
				><i class="fas fa-arrow-right" /></button
			>
		</div>
	{/each}
</div>
