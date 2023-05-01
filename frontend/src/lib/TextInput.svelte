<script lang="ts">
    export let id: string;
    export let label: string;
    export let value: string;
  </script>
  
  <div class="mb-1 !mt-1 md:!mt-0">
    <label for="{id}" class="label-text-alt text-neutral !select-none text-base md:text-xs">{label}</label>
    <input
      type="text"
      id="{id}"
      bind:value="{value}"
      class="input md:input-sm md:text-sm text-base input-bordered w-full font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent hover:border-primary"
    />
  </div>
  