<script lang="ts">
	import type { PointerCanvas } from '$lib/types/pointer-canvas';
	import { getArrow, type ArrowOptions } from 'perfect-arrows';

	export let pointer: PointerCanvas;

	const options: ArrowOptions | undefined = { padEnd: 20 };
	$: x0 = pointer.x0;
	$: y0 = pointer.y0;
	$: x1 = pointer.x1;
	$: y1 = pointer.y1;
	$: [sx, sy, cx, cy, ex, ey, ae, as, sc] = getArrow(x0, y0, x1, y1, options);
</script>

<circle cx={sx} cy={sy} r={4} />
<path d="M{sx},{sy} Q{cx},{cy} {ex},{ey}" fill="none" />
<polygon points="0,-6 12,0, 0,6" transform="translate({ex},{ey}) rotate({ae * (180 / Math.PI)})" />
