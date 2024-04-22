<script lang="ts">
	import type { EliminationGroup } from '$lib/types/elimination-group';

	export let step: number;
	export let elimination: EliminationGroup;
	export let eliminationClicked: (elimination: EliminationGroup) => void;

	const strategyToString = (strategy: string) => {
		switch (strategy) {
			case 'scan':
				return 'Scan';
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
		<span>{strategyToString(elimination.technique)}</span>
	</button>
</div>
