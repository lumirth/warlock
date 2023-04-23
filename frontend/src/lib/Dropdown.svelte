<script lang="ts">
  export let id: string;
  export let label: string;
  export let options: Array<{ value: string; text: string }>;
  export let selectedValue: string;
</script>

<div class="mb-1">
  <label for="{id}" class="label-text">{label}</label>
  <select id="{id}" bind:value="{selectedValue}" class="select select-sm select-bordered w-full">
    {#each options as option}
      <option value="{option.value}">{option.text}</option>
    {/each}
  </select>
</div>
