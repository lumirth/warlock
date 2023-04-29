<script lang="ts">
    let isCourseSectionsVisible = false;
    function toggleCourseSections() {
      isCourseSectionsVisible = !isCourseSectionsVisible;
    }
  </script>
  
  {#if isCourseSectionsVisible}
    <div
      class="border border-neutral p-1 mt-1"
      class:hidden={!isCourseSectionsVisible}
    >
      <p>Course Sections:</p>
      <ul>
        <li>Section 1</li>
        <li>Section 2</li>
        <li>Section 3</li>
      </ul>
    </div>
  {/if}
  
  <button class="flex w-20 h-4 items-center justify-center ml-auto p-1 text-xs cursor-pointer mt-1 mb-1 transition-colors duration-150 ease-in-out bg-base-200 border border-neutral hover:bg-neutral" on:click={toggleCourseSections}>
    {#if isCourseSectionsVisible}
      &#x25B2;
    {:else}
      &#x25BC;
    {/if}
  </button>