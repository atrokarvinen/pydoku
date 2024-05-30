<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import SettingsPage from './SettingsPage.svelte';

	export let data;
</script>

{#if data.error || data.loadPromise === undefined}
	Error
{:else}
	{#await data.loadPromise}
		<div class="flex flex-col items-center justify-center w-full">
			<ProgressRadial width="w-16" />
		</div>
	{:then value}
		<SettingsPage settings={value.data} />
	{:catch error}
		<p>Error getting settings {error}</p>
	{/await}
{/if}
