<script lang="ts">
	import { getSolutionSteps } from '$lib/solution/solution-parser';
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import type { Solution } from '$lib/types/solution';
	import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import SolutionInfoItem from './SolutionInfoItem.svelte';
	import SolutionSummary from './SolutionSummary.svelte';

	export let solution: Solution;
	export let selectedElimination: Elimination | undefined;
	export let selectedCandidate: SingleCandidate | undefined;
	export let eliminationClicked: (elimination: Elimination) => void;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	$: solutionSteps = getSolutionSteps(solution);

	const solutionStepClick = (step: Elimination | SingleCandidate) => {
		if (step.type === 'elimination') {
			eliminationClicked(step);
		} else {
			candidateClicked(step);
		}
	};
</script>

<div class="flex flex-col gap-2 overflow-auto h-max-full">
	<Accordion>
		<AccordionItem open>
			<svelte:fragment slot="summary">Solution steps</svelte:fragment>
			<svelte:fragment slot="content">
				{#each solutionSteps as action, step}
					<SolutionInfoItem
						step={step + 1}
						solutionStep={action}
						stepClicked={solutionStepClick}
						isSelected={step === selectedElimination?.solutionIndex ||
							step === selectedCandidate?.solutionIndex}
					/>
				{/each}
			</svelte:fragment>
		</AccordionItem>
		<AccordionItem>
			<svelte:fragment slot="summary">Summary</svelte:fragment>
			<svelte:fragment slot="content">
				<SolutionSummary {solution} {solutionSteps} {eliminationClicked} {candidateClicked} />
			</svelte:fragment>
		</AccordionItem>
	</Accordion>
</div>
