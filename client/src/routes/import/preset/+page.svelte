<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import PresetImport from './PresetImport.svelte';

	export let data;
</script>

{#await data.loadPromise}
	<div class="flex flex-col items-center justify-center h-full w-full">
		<ProgressRadial width="w-16" />
	</div>
{:then value}
	{#if value}
		<PresetImport presets={value.data} />
	{:else}
		<p>No presets found</p>
	{/if}
{:catch error}
	<p>Error loading presets</p>
{/await}
