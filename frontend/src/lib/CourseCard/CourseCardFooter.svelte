<script lang="ts">
  import RadialRating from "./RadialRating.svelte";
  export let average_gpa: number;
  export let tags_text: Array<string>;
  export let credit_hours: string;
  export let sem_code: string;
  let gpa_string: string;
  $: gpa_string = average_gpa.toFixed(1);
</script>

<div class="flex justify-between items-center h-10 px-3">
  <div
    class="text-lg flex flex-row font-mono whitespace-nowrap pr-3 border-r border-neutral min-h-full items-center"
  >
    <div class="pr-2">{credit_hours}HRS</div>
    <div class="bg-neutral w-[1px] flex-1 h-6" />
    <div class="pl-2 uppercase">{sem_code}</div>
  </div>
  <div class="flex flex-row flex-nowrap gap-2 py-2 flex-grow pl-3">
    <div class="flex flex-row items-center flex-nowrap whitespace-nowrap flex-shrink-0">
      {#if average_gpa}
      <div class="flex items-center tooltip tooltip-neutral tooltip-bottom before:font-mono before:uppercase before:text-xs" data-tip="Historic average GPA">
        <div class="flex items-center">
          <RadialRating value={average_gpa} maxValue={4.0} />
        </div>
        <span class="pl-2 mb-[0.6px] text-lg leading-4 flex items-center font-mono self-center">
          {gpa_string} GPA
        </span>
        </div>
      {:else}
      <div class="flex items-center tooltip tooltip-neutral tooltip-bottom before:font-mono before:uppercase before:text-xs " data-tip="No GPA data available">
        <div class="flex items-center">
          <div    class="radial-progress bg-neutral text-neutral border-2 border-neutral" style="--value:0; --size:1rem; --thickness:3px;"/>
        </div>
        <p class="pl-2 mb-[0.6px] text-lg leading-4 flex items-center text-neutral flex-nowrap whitespace-nowrap flex-shrink-0 font-mono self-center">
          NO GPA
        </p>
      </div>
      {/if}
    </div>
  </div>
  <div class="flex gap-2 flex-nowrap !overflow-scroll ml-3 no-scrollbar relative overflow-x-scroll">
    <!-- TODO: add tooltips for full name of gened -->
    {#each tags_text as tag}
      <div
        class="px-2 h-6 bg-base-200 border border-neutral text-base font-mono flex flex-col justify-center"
      >
        {tag}
      </div>
    {/each}
    <!-- show gradient if there is overflow -->
    <!-- <div class="absolute top-0 right-0 h-full w-4 bg-gradient-to-l from-base-200 to-transparent"></div> -->
  </div>
</div>

<style>
  .tooltip::before {
    border-radius: 0 !important;
    border-top-left-radius: 0 !important;
    border-top-right-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
  }

  /* Hide scrollbar for Chrome, Safari and Opera */
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }
  
  /* Hide scrollbar for IE, Edge and Firefox */
  .no-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none !important; /* Firefox */
  }
</style>