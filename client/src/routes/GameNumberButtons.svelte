<script lang="ts">
	export let boardSize: number;
	export let numberClicked: (n: number) => void;

	$: numbers = Array.from({ length: boardSize }, (_, i) => i + 1);
</script>

<div class="flex flex-row gap-2">
	{#each numbers as number}
		<button class="btn-sm variant-filled-primary" on:click={(e) => numberClicked(number)}
			>{number}</button
		>
	{/each}
</div>
