<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let onClick: () => void;
	export let disabled: boolean = false;
	export let icon: string;
	export let text: string = '';
	export let isLoading: boolean = false;

	const btnClass = 'btn-icon variant-filled-primary';
</script>

<div class="flex flex-col items-center">
	<button class={btnClass} on:click={onClick} {disabled}>
		{#if isLoading}
			<ProgressRadial width="w-6" />
		{:else}
			<i class={icon} />
		{/if}
	</button>
	<span class="text-xs">{text}</span>
</div>
