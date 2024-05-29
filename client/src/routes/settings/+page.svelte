<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import SettingsPage from './SettingsPage.svelte';

	export let data;
</script>

{#await data.loadPromise}
	<div class="flex flex-col items-center justify-center w-full">
		<ProgressRadial width="w-16" />
	</div>
{:then value}
	<SettingsPage settings={value.data} />
{:catch error}
	<p>Error gettings settings: {error}</p>
{/await}
