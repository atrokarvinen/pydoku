<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';

	export let step: number;
	export let elimination: Elimination;
	export let eliminationClicked: (elimination: Elimination) => void;

	const strategyToString = (strategy: string) => {
		switch (strategy) {
			case 'scan':
				return 'Scan';
			case 'naked-pair':
				return 'Naked Pair';
			case 'naked-triple':
				return 'Naked Triple';
			case 'naked-quad':
				return 'Naked Quadruple';
			case 'hidden-pair':
				return 'Hidden Pair';
			case 'hidden-triple':
				return 'Hidden Triple';
			case 'hidden-quad':
				return 'Hidden Quadruple';
			case 'pointing':
				return 'Pointing';
			case 'claiming':
				return 'Claiming';
			case 'x-wing':
				return 'X-Wing';
			case 'swordfish':
				return 'Swordfish';
			case 'jellyfish':
				return 'Jellyfish';
			case 'xy-wing':
				return 'XY-Wing';
			case 'simple-coloring':
				return 'Simple Coloring';
			default:
				return 'Unknown strategy';
		}
	};

	const numToThreeDigits = (num: number) => {
		return num.toString().padStart(3, '0');
	};
</script>

<div>
	<button on:click={() => eliminationClicked(elimination)}>
		<span>#{numToThreeDigits(step)}</span>
		<span>,</span>
		<span>{strategyToString(elimination.technique)}</span>
	</button>
</div>
