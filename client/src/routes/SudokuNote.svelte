<script lang="ts">
	export let note: number;
	export let isEliminated: boolean;
	export let isForming: boolean;
	export let selectedNumber: number | undefined;

	$: isSelected = selectedNumber === note;

	let className = '';
	$: {
		let noteStyle = 'position: absolute text-center';
		if (note === 1 || note === 4 || note === 7) {
			noteStyle += ' left-0';
		} else if (note === 2 || note === 5 || note === 8) {
			noteStyle += ' left-1/2 transform -translate-x-1/2';
		} else {
			noteStyle += ' right-0';
		}
		if (note === 1 || note === 2 || note === 3) {
			noteStyle += ' top-0';
		} else if (note === 4 || note === 5 || note === 6) {
			noteStyle += ' top-1/2 transform -translate-y-1/2';
		} else {
			noteStyle += ' bottom-0';
		}
		if (isEliminated) {
			noteStyle += ' border border-red-500';
		}
		if (isForming) {
			noteStyle += ' border border-green-500';
		}
		if (isSelected) {
			noteStyle += ' bg-green-700';
		}
		className = noteStyle;
	}
</script>

<span class={className} style="font-size: xx-small; line-height: 1;">{note}</span>
