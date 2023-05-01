<script lang="ts">
  export let id: string;
  export let label: string;
  export let options: Array<{ value: string; text: string }>;
  export let selectedValue: string;
  export let addEmptyOption: boolean = true;
</script>

<div class="mb-1 !mt-1 md:!mt-0">
  <label for="{id}" class="label-text-alt  text-neutral !select-none text-base md:text-xs">{label}</label>
  <select id="{id}" bind:value="{selectedValue}" class="select md:select-sm md:text-sm text-base select-bordered w-full font-normal placeholder-neutral focus:outline-none focus:placeholder-transparent hover:border-primary">
    {#if addEmptyOption}
    <option value=""></option> <!-- add this line -->
    {/if}
    {#each options as option}
      <option value="{option.value}">{option.text}</option>
    {/each}
  </select>
</div>
