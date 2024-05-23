<script lang="ts">
	import type { PointerCanvas } from '$lib/types/pointer-canvas';
	import { getArrow, type ArrowOptions } from 'perfect-arrows';

	export let pointer: PointerCanvas;

	const options: ArrowOptions | undefined = {
		padStart: 10,
		padEnd: 18
	};
	$: x0 = pointer.x0;
	$: y0 = pointer.y0;
	$: x1 = pointer.x1;
	$: y1 = pointer.y1;
	$: [sx, sy, cx, cy, ex, ey, ae, as, ac] = getArrow(x0, y0, x1, y1, options);
	$: isBidirectional = pointer.bidirectional;
	$: isDashed = pointer.dashed;

	const arrowSize = 2;
</script>

{#if isBidirectional}
	<polygon
		points="0,-{arrowSize} {2 * arrowSize},0, 0,{arrowSize}"
		transform="translate({sx},{sy}) rotate({as * (180 / Math.PI)})"
	/>
{/if}
<path
	d="M{sx},{sy} Q{cx},{cy} {ex},{ey}"
	fill="none"
	stroke-dasharray={isDashed ? '8 4' : undefined}
/>
<polygon
	points="0,-{arrowSize} {2 * arrowSize},0, 0,{arrowSize}"
	transform="translate({ex},{ey}) rotate({ae * (180 / Math.PI)})"
/>
