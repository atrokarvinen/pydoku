<script lang="ts">
	import { NoteType } from '$lib/types/note-type';
	import {
		CANDIDATE_COLOR,
		CAUSING_NOTE_STYLE,
		COLORING_1_COLOR,
		COLORING_2_COLOR,
		ELIMINATED_STYLE,
		SELECTED_NUMBER_STYLE
	} from './theme';

	export let note: number;
	export let noteType: NoteType;
	export let selectedNumber: number | undefined;

	$: isSelected = selectedNumber === note;

	let className = '';
	$: {
		let noteStyle = 'flex items-center justify-center w-full h-full';
		if (noteType === NoteType.ELIMINATED) {
			noteStyle += ' ' + ELIMINATED_STYLE;
		} else if (noteType === NoteType.CAUSING) {
			noteStyle += ' ' + CAUSING_NOTE_STYLE;
		} else if (noteType === NoteType.CANDIDATE) {
			noteStyle += ' ' + CANDIDATE_COLOR;
		} else if (noteType === NoteType.COLORING_1) {
			noteStyle += ' ' + COLORING_1_COLOR;
		} else if (noteType === NoteType.COLORING_2) {
			noteStyle += ' ' + COLORING_2_COLOR;
		}
		if (isSelected) {
			noteStyle += ' ' + SELECTED_NUMBER_STYLE;
		}
		className = noteStyle;
	}
</script>

<span class={className} style="font-size: xx-small; line-height: 1;">{note}</span>
