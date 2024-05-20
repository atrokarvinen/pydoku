<script lang="ts">
	import type { Pointer } from '$lib/types/pointer';
	import { pointerToPointerCanvas } from '$lib/types/pointer-canvas';
	import Arrow from './Arrow.svelte';

	export let size: number;
	export let pointers: Pointer[];

	const squareSizePx = 40;

	$: canvas_size = size * squareSizePx;
	$: canvasPointers = pointers.map((p) => pointerToPointerCanvas(p, squareSizePx));
</script>

<div class="absolute">
	<svg
		viewBox="0 0 {canvas_size} {canvas_size}"
		style="width: {canvas_size}px; height: {canvas_size}px;"
		stroke="#000"
		fill="#000"
		stroke-width={3}
	>
		{#each canvasPointers as pointer}
			<Arrow {pointer} />
		{/each}
	</svg>
</div>
