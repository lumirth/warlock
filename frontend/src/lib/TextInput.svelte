<script lang="ts">
    export let id: string;
    export let label: string;
    export let value: string;
  </script>
  
  <div class="mb-1 !mt-0">
    <label for="{id}" class="label-text-alt text-neutral !select-none">{label}</label>
    <input
      type="text"
      id="{id}"
      bind:value="{value}"
      class="input input-sm input-bordered w-full font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent hover:border-primary"
    />
  </div>
  