<script lang="ts">
	export let icon: string;
	export let text: string;
	export let href: string;
</script>

<a class="flex flex-col items-center" {href}>
	<button class="btn-icon variant-ringed">
		<i class="{icon} fa-xl" />
	</button>
	<span>{text}</span>
</a>
