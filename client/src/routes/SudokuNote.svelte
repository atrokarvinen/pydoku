<script lang="ts">
	export let note: number;
	export let isEliminated: boolean;
	export let isForming: boolean;
	export let selectedNumber: number | undefined;

	$: isSelected = selectedNumber === note;

	let className = '';
	$: {
		let noteStyle = 'flex items-center justify-center w-full h-full';
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
