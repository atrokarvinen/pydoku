<script lang="ts">
	import GameSolveButton from './GameSolveButton.svelte';

	export let solve: () => void;
	export let jumpToStart: () => void;
	export let back: () => void;
	export let next: () => void;
	export let playSolution: () => void;
	export let jumpToEnd: () => void;

	export let isSolving: boolean;
	export let isPlaying: boolean;

	$: disabled = isSolving || isPlaying;
</script>

<div class="flex flex-row justify-around">
	<GameSolveButton
		onClick={solve}
		icon="fas fa-lightbulb"
		text="Solve"
		{disabled}
		isLoading={isSolving}
	/>
	<GameSolveButton onClick={jumpToStart} icon="fas fa-backward-fast" {disabled} />
	<GameSolveButton onClick={back} icon="fas fa-backward-step" {disabled} />
	<GameSolveButton onClick={playSolution} icon="fas fa-play" {disabled} />
	<GameSolveButton onClick={next} icon="fas fa-forward-step" {disabled} />
	<GameSolveButton onClick={jumpToEnd} icon="fas fa-forward-fast" {disabled} />
</div>
