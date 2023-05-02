<script lang="ts">
  import CourseCardSection from "./CourseCardSection.svelte";
  let isCourseSectionsVisible = false;
  // TODO: make this download course sections if none are found in the object. this may require restructuring how this component gets values
  function toggleCourseSections() {
    if (sections && sections.length > 0)
      isCourseSectionsVisible = !isCourseSectionsVisible;
  }

  let sleft = 0;
  let tableElem: HTMLElement;
  let tableWidth: number;
  let tableContainerWidth: number;
  let showRightGradient: boolean = false;
  export let sections: any = [];

  $: {
    if (tableElem) {
      tableWidth = tableElem.scrollWidth;
      tableContainerWidth = tableElem.clientWidth;
    }
    if (tableWidth && tableContainerWidth) {
      showRightGradient = tableWidth > tableContainerWidth;
    }
  }
</script>

{#if isCourseSectionsVisible}
  <div class="relative overflow-x-scroll mt-1 border border-neutral">
    <div
      class="absolute top-0 left-0 h-full w-4 bg-gradient-to-r from-base-100 to-transparent transition-opacity ease-in-out z-50 {sleft >
      0
        ? 'opacity-100'
        : 'opacity-0'}"
    />
    <div
      class="bg-base-100 overflow-x-auto no-scrollbar scroll relative pl-2 py-2"
      class:hidden={!isCourseSectionsVisible}
      bind:this={tableElem}
      on:scroll={() => (sleft = tableElem.scrollLeft)}
    >
      <table
        class="bg-transparent table table-compact !border-neutral !rounded-none w-full"
      >
        <!-- <thead class="!rounded-tl-none !rounded-tr-none">
        <tr class="!rounded-none">
          <th class="!rounded-none">Open</th>
          <th>Code</th>
          <th>CRN</th>
          <th>Type</th>
          <th class="!rounded-none">Favorite Color</th>
        </tr>
      </thead> -->
        {#if sections && sections.length > 0}
          {#each sections as section}
            <CourseCardSection
              section = {section}
            />
          {/each}
        {/if}
        <!-- <CourseCardSection crn="54321" />
        <CourseCardSection crn="12345" openStatus="Closed" /> -->
      </table>
    </div>
    {#if showRightGradient}
      <div
        class="absolute top-0 right-0 h-full w-4 bg-gradient-to-l from-base-100 to-transparent"
      />
    {/if}
  </div>
{/if}

<button
  class="flex w-20 h-4 items-center justify-center ml-auto p-1 text-xs cursor-pointer mt-1 transition-colors duration-150 ease-in-out bg-base-200 border border-neutral hover:bg-neutral"
  on:click={toggleCourseSections}
>
  {#if isCourseSectionsVisible && sections && sections.length > 0}
    &#x25B2;
  {:else}
    &#x25BC;
  {/if}
</button>

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
