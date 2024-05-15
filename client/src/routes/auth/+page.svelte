<script lang="ts">
	export let data;

	$: error = data.error;
</script>

{#if error}
	<div>
		<p>Error happened</p>
		<p>{error}</p>
	</div>
{:else}
	Success
{/if}
