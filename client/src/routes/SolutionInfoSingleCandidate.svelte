<script lang="ts">
	import type { SingleCandidate } from '$lib/types/single-candidate';

	export let step: number;
	export let candidate: SingleCandidate;
	export let candidateClicked: (candidate: SingleCandidate) => void;

	const numToThreeDigits = (num: number) => {
		return num.toString().padStart(3, '0');
	};
</script>

<div>
	<button on:click={() => candidateClicked(candidate)}>
		<span>#{numToThreeDigits(step)}</span>
		<span>{`(${candidate.column + 1}, ${candidate.row + 1})`}</span>
		<span>{`number: ${candidate.number}`}</span>
		<span>,</span>
		<span>Single candidate</span>
	</button>
</div>
