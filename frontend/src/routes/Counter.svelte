<script lang="ts">
	let count = 0;
</script>

<div>
	<button on:click={() => (count -= 1)} aria-label="Decrease the counter by one">-</button>
	<div>
		<div>
			<strong>{Math.floor(count)}</strong>
		</div>
	</div>

	<button on:click={() => (count += 1)} aria-label="Increase the counter by one">+</button>
</div>

<style>
</style>
