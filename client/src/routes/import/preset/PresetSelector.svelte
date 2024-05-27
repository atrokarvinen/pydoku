<script lang="ts">
	import type { PresetSudoku } from './preset-sudoku';

	export let presets: PresetSudoku[];
	export let value: string;

	$: options = presets.map((preset) => ({
		value: preset.id,
		text: preset.name
	}));
</script>

<select class="select overflow-auto" bind:value>
	{#each options as option}
		<option value={option.value}>{option.text}</option>
	{/each}
</select>
