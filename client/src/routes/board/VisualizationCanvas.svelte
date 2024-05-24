<script lang="ts">
	import type { Pointer } from '$lib/types/pointer';
	import { pointerToPointerCanvas } from '$lib/types/pointer-canvas';
	import Arrow from './Arrow.svelte';

	export let size: number;
	export let pointers: Pointer[];
	export let maxWidth: number;

	$: squareSizePx = maxWidth / size;
	$: canvas_size = maxWidth;
	$: canvasPointers = pointers.map((p) => pointerToPointerCanvas(p, squareSizePx));
</script>

<svg
	class="absolute"
	pointer-events="none"
	viewBox="0 0 {canvas_size} {canvas_size}"
	style="width: {canvas_size}px; height: {canvas_size}px;"
	stroke="#000"
	fill="#000"
	stroke-width={1}
>
	{#each canvasPointers as pointer}
		<Arrow {pointer} />
	{/each}
</svg>
