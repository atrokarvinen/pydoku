<script lang="ts">
	import type { Elimination } from '$lib/types/elimination';

	export let step: number;
	export let elimination: Elimination;
	export let eliminationClicked: (elimination: Elimination) => void;

	const strategyToString = (strategy: string) => {
		switch (strategy) {
			case 'row-scan':
				return 'Row scan';
			case 'column-scan':
				return 'Column scan';
			case 'box-scan':
				return 'Box scan';
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
		<span>{`(${elimination.column + 1}, ${elimination.row + 1})`}</span>
		<span>{`number: ${elimination.number}`}</span>
		<span>,</span>
		<span>{strategyToString(elimination.causedBy.strategy)}</span>
	</button>
</div>
