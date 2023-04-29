<script lang="ts">
    export let description: string;
  
    let isDescriptionExpanded = false;
    function toggleDescription() {
      isDescriptionExpanded = !isDescriptionExpanded;
    }
  </script>
  
  <div class="p-1">
    <div class="relative">
      <div class="flex items-center">
        <div class={`${isDescriptionExpanded ? '' : 'line-clamp-1'} text-sm leading-4 flex-grow`}>
          {description}
        </div>
        {#if !isDescriptionExpanded}
          <div class="ml-1">
            <button
              class="text-xs py-0 px-1 cursor-pointer focus:outline-none border border-neutral hover:bg-neutral transition-colors duration-150 ease-in-out flex items-center justify-center h-4"
              on:click={toggleDescription}
            >
              ...
            </button>
          </div>
        {/if}
      </div>
      {#if isDescriptionExpanded}
        <div class="w-full flex justify-end mt-1">
          <button
            class="w-full text-xs p-1 h-4 flex items-center justify-center cursor-pointer focus:outline-none border border-neutral hover:bg-neutral transition-colors duration-150 ease-in-out "
            on:click={toggleDescription}
          >
            ⌃
          </button>
        </div>
      {/if}
    </div>
  </div>