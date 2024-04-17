<script lang="ts">
	import { AppBar, AppShell } from '@skeletonlabs/skeleton';
	import '../app.postcss';
</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<h1>Sudoku</h1>
		</AppBar>
	</svelte:fragment>
	<div class="md:p-5 p-2 flex items-center justify-center">
		<slot />
	</div>
</AppShell>
