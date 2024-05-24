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

	// Modals automatically receive focus, blur automatically here since it is readonly
	const handleFocus = (e: FocusEvent) => {
		if (e.target) {
			(e.target as HTMLInputElement).blur();
		}
	};
</script>

<div>
	<div class="flex flex-row gap-x-2">
		<input class="input" bind:value={text} readonly on:focus={handleFocus} />
		<div>
			<button class="btn-icon variant-filled" on:click={() => copy(text)}
				><i class="fas fa-copy" /></button
			>
		</div>
	</div>
	{#if copied}
		<span class="text-xs">Copied!</span>
	{/if}
</div>
