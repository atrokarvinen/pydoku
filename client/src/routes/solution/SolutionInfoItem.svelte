<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';
	import type { SingleCandidate } from '$lib/types/single-candidate';
	import { techniqueToString } from './solution-string-conversion';

	export let step: number;
	export let solutionStep: Elimination | SingleCandidate;
	export let stepClicked: (candidate: Elimination | SingleCandidate) => void;
	export let isSelected: boolean;

	let buttonRef: HTMLButtonElement;

	const numToThreeDigits = (num: number) => {
		return num.toString().padStart(3, '0');
	};

	$: {
		if (isSelected) {
			buttonRef.focus();
		}
	}
</script>

<div class={isSelected ? ' bg-green-500' : ''}>
	<button
		class="p-2 w-full text-start"
		bind:this={buttonRef}
		on:click={() => stepClicked(solutionStep)}
	>
		<span>#{numToThreeDigits(step)}</span>
		<span>,</span>
		<span>{techniqueToString(solutionStep.technique)}</span>
	</button>
</div>
