<script lang="ts">
	export let text: string;

	let copied = false;

	const copy = (text: string) => {
		navigator.clipboard.writeText(text);
		copied = true;
		setTimeout(() => {
			copied = false;
		}, 1500);
	};
</script>

<div>
	<div class="flex flex-row gap-x-2">
		<input class="input" bind:value={text} readonly />
		<button class="btn-icon variant-filled" on:click={() => copy(text)}
			><i class="fas fa-copy" /></button
		>
	</div>
	{#if copied}
		<span class="text-xs">Copied!</span>
	{/if}
</div>
