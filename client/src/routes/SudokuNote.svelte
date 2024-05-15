<script lang="ts">
	import { CAUSING_NOTE_STYLE, ELIMINATED_STYLE, SELECTED_STYLE } from './theme';

	export let note: number;
	export let isEliminated: boolean;
	export let isCausing: boolean;
	export let selectedNumber: number | undefined;

	$: isSelected = selectedNumber === note;

	let className = '';
	$: {
		let noteStyle = 'flex items-center justify-center w-full h-full';
		if (isEliminated) {
			noteStyle += ' ' + ELIMINATED_STYLE;
		}
		if (isCausing) {
			noteStyle += ' ' + CAUSING_NOTE_STYLE;
		}
		if (isSelected) {
			noteStyle += ' ' + SELECTED_STYLE;
		}
		className = noteStyle;
	}
</script>

<span class={className} style="font-size: xx-small; line-height: 1;">{note}</span>
