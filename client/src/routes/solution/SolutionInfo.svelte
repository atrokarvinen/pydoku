<script lang="ts">
	import { getSolutionSteps, getSolutionStepsByCount } from '$lib/solution/solution-parser';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Solution } from '$lib/types/solution';
	import type { SolutionGroup } from '$lib/types/solution-menu';
	import SolutionInfoItem from './SolutionInfoItem.svelte';

	export let solution: Solution;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let eliminationClicked: (elimination: Elimination) => void;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	$: solutionSteps = getSolutionSteps(solution);
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

	const solutionStepClick = (step: Elimination | SingleCandidate) => {
		if (step.type === 'elimination') {
			eliminationClicked(step);
		} else {
			candidateClicked(step);
		}
	};
</script>

<div class="flex flex-col gap-2 h-48 overflow-auto">
	{#if solution.isSolved}
		<span>Solved after ({solutionSteps.length}) steps.</span>
	{:else if solution.isSolved === false}
		<span>Unable to solve sudoku</span>
	{/if}
	{#each solutionStepsByCount.groups as group}
		<div class="flex flex-col gap-2">
			<div class="flex flex-row gap-5 items-center">
				<span class="font-bold">{group.technique} ({group.steps.length})</span>
				<button class="btn-icon variant-filled" on:click={() => groupClicked(group)}
					><i class="fas fa-arrow-right" /></button
				>
			</div>
		</div>
	{/each}
	{#each solutionSteps as action, step}
		<SolutionInfoItem
			step={step + 1}
			solutionStep={action}
			stepClicked={solutionStepClick}
			isSelected={step === selectedElimination?.solutionIndex ||
				step === selectedCandidate?.solutionIndex}
		/>
	{/each}
</div>
