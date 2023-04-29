<script lang="ts">
  import RadialRating from "./RadialRating.svelte";
  export let average_gpa: number;
  export let tags_text: Array<string>;
  let gpa_string: string;
  $: gpa_string = average_gpa.toFixed(1)
</script>

<div class="flex justify-between items-center p-1">
  <div class="flex flex-nowrap gap-1">

    <div class="flex flex-row items-center">
      <div class="flex items-center">
        <RadialRating value={average_gpa} maxValue={4.0} />
      </div>
      <p class="pl-1 mb-[1.4px] text-base leading-4 flex items-center">{gpa_string} GPA</p>
    </div>
  </div>
  <div class="flex flex-wrap gap-1">
    {#each tags_text as tag}
      <div
        class="px-2 bg-base-200 border border-neutral text-xs font-mono"
      >
        {tag}
      </div>
    {/each}
  </div>
</div>