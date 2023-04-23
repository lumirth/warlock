<script lang="ts">
  export let id: string;
  export let label: string;
  export let options: Array<{ value: string; text: string }>;
  export let selectedValue: string;
</script>

<div class="mb-1 !mt-0">
  <label for="{id}" class="label-text text-neutral">{label}</label>
  <select id="{id}" bind:value="{selectedValue}" class="select select-sm select-bordered w-full font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent">
    {#each options as option}
      <option value="{option.value}">{option.text}</option>
    {/each}
  </select>
</div>
