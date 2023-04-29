<!-- RadialProgress.svelte -->
<script lang="ts">
  export let value: number;
  export let maxValue: number;
  export let size: string = "1rem";
  export let thickness: string = "3px";

  $: progressPercentage = (value / maxValue) * 100;
</script>

<!-- rewrite the above to set the border color conditionally -->
<div 
    class="radial-progress {progressPercentage >= 80 ? 'bg-success' : progressPercentage >= 60 ? 'bg-warning' : 'bg-error'} text-base-200 border-2 {progressPercentage >= 80 ? 'border-success' : progressPercentage >= 60 ? 'border-warning' : 'border-error'}"
    style="--value:{progressPercentage}; --size:{size}; --thickness: {thickness};"
/>