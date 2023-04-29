<script lang="ts">
  import { onMount } from "svelte";

  export let course_id: string;
  export let course_detail: string;
  export let credit_hours: string;
  export let sem_code: string;

  let sleft = 0;
  let headerMiddleText: HTMLElement;
</script>

<div class="grid grid-cols-[auto,1fr,auto] items-center gap-x-1 mx-1">
  <div class="text-black dark:text-white font-semibold whitespace-nowrap border-r border-neutral pr-1">
    {course_id}
  </div>
  <div class="relative overflow-x-scroll">
    <div class="absolute top-0 left-1 h-full w-4 bg-gradient-to-r from-base-200 to-transparent transition-opacity ease-in-out {sleft > 0 ? 'opacity-100' : 'opacity-0'}"></div>
    <div class="whitespace-nowrap overflow-x-scroll no-scrollbar scroll" bind:this={headerMiddleText} on:scroll={() => (sleft = headerMiddleText.scrollLeft)}>
      <div class="text-sm text-neutral font-light uppercase">{course_detail}&nbsp;&nbsp;&nbsp;</div>
    </div>
    <div class="absolute top-0 right-0 h-full w-4 bg-gradient-to-l from-base-200 to-transparent"></div>
  </div>
  <div class="flex flex-row flex-grow font-mono whitespace-nowrap pl-1 border-l border-neutral min-h-full items-center">
    <div class="pr-1">{credit_hours}HRS</div>
    <div class="bg-neutral w-[1px] flex-1 h-4"></div>
    <div class="pl-1">{sem_code}</div>
  </div>
</div>


<style>
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
