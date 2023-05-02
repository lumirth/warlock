<script lang="ts">
  import CourseCardSection from "./CourseCardSection.svelte";
  import { dev } from "$app/environment";
  let isCourseSectionsVisible = false;

  export let year: string;
  export let term: string;
  export let course_id: string;
  let subj = course_id.split(" ")[0];
  let course_num = course_id.split(" ")[1];
  let loading = false;

  let adv_params: any = {
    course_id: course_num,
    subject: subj,
    year: year,
    term: term,
  };
  let sleft = 0;
  let tableElem: HTMLElement;
  let tableWidth: number;
  let tableContainerWidth: number;
  let showRightGradient: boolean = false;
  export let sections: any = [];

  // TODO: make this download course sections if none are found in the object. this may require restructuring how this component gets values
  const queryAndToggle = async () => {
    await queryBackend();
    if (sections && sections.length > 0) {
      isCourseSectionsVisible = !isCourseSectionsVisible;
    }
  };

  const queryBackend = async () => {
    if (sections && sections.length > 0) return;
    loading = true;
    try {
      let url = "";
      if (dev) url = "http://localhost:8000/search/advanced";
      else url = "https://warlock-backend.fly.dev/search/advanced";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(adv_params),
      });
      const data = await response.json();
      sections = data[0].sections;
      loading = false;
    } catch (error) {
      console.error(error);
      sections = [];
      loading = false;
    }
  };

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

{#if isCourseSectionsVisible && sections && sections.length > 0}
  <div class="relative overflow-x-auto mt-1 border border-neutral">
    <div
      class="absolute top-0 left-0 h-full w-4 bg-gradient-to-r from-base-100 to-transparent transition-opacity ease-in-out z-50 {sleft >
      0
        ? 'opacity-100'
        : 'opacity-0'}"
    />
    <div
      class="bg-base-100 overflow-x-scroll scroll relative pl-2 py-2"
      class:hidden={!isCourseSectionsVisible}
      bind:this={tableElem}
      on:scroll={() => (sleft = tableElem.scrollLeft)}
    >
      <table
        class="bg-transparent table table-compact !border-neutral !rounded-none w-full"
      >
        {#if sections && sections.length > 0}
          {#each sections as section, i}
            {#if i === sections.length - 1}
              <CourseCardSection {section} last={true} />
            {:else}
              <CourseCardSection {section} />
            {/if}
          {/each}
        {/if}
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
  class="flex btn btn-xs !min-h-0 leading-3 !h-6 md:!h-4 w-20 items-center justify-center ml-auto text-xs cursor-pointer mt-1 transition-colors duration-150 ease-in-out bg-base-200 border border-neutral hover:bg-neutral transition-none {loading
    ? 'loading'
    : ''}"
  on:click={queryAndToggle}
>
<!-- The above does some secret loading to make desktop experience smoother -->
  {#if !loading}
    {#if isCourseSectionsVisible}
      &#x25B2;
    {:else}
      &#x25BC;
    {/if}
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
