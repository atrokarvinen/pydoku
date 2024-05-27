<script lang="ts">
	import ImportTypeButton from './ImportTypeButton.svelte';
</script>

<div class="flex flex-col w-full items-center">
	<h1 class="h3 mb-10">Import sudoku</h1>
	<p class="text-lg mb-3">Choose import type:</p>
	<div class="flex flex-row gap-5">
		<ImportTypeButton href="/import/text" icon="fas fa-font" text="Text" />
		<ImportTypeButton href="/import/image" icon="fas fa-image" text="Image" />
		<ImportTypeButton href="/import/preset" icon="fas fa-floppy-disk" text="Preset" />
	</div>
</div>
