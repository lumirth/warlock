<script lang="ts">
  import { onMount } from "svelte";
  import { convertCourseURL } from "cisurls";

  export let course_id: string;
  export let course_detail: string;
  // export let credit_hours: string;
  // export let sem_code: string;
  export let href: string;

  let link = convertCourseURL(href);

  let sleft = 0;
  let headerMiddleText: HTMLElement;
</script>

<div class="grid grid-cols-[auto,1fr,auto] items-center gap-x-2 mx-2 h-10">
  <div class="text-lg font-semibold whitespace-nowrap border-r border-neutral pr-3 pl-1 h-full flex flex-col justify-center decoration-1 underline underline-offset-2 transition-all hover:underline-offset-4 hover:text-primary">
    <a class="cursor-pointer" href={link}>{course_id}</a>
  </div>
  <div class="relative overflow-x-scroll pl-1 pr-1">
    <div class="absolute top-0 left-1 h-full w-4 bg-gradient-to-r from-base-200 to-transparent transition-opacity ease-in-out {sleft > 0 ? 'opacity-100' : 'opacity-0'}"></div>
    <div class="whitespace-nowrap overflow-x-scroll no-scrollbar scroll" bind:this={headerMiddleText} on:scroll={() => (sleft = headerMiddleText.scrollLeft)}>
      <div class="text-lg text-neutral font-light uppercase">{course_detail}&nbsp;&nbsp;&nbsp;</div>
    </div>
    <div class="absolute top-0 right-1 h-full w-4 bg-gradient-to-l from-base-200 to-transparent"></div>
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
