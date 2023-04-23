<script lang="ts">
    export let id: string;
    export let label: string;
    export let value: string;
  </script>
  
  <div class="mb-1">
    <label for="{id}" class="label-text">{label}</label>
    <input
      type="text"
      id="{id}"
      bind:value="{value}"
      class="input input-sm input-bordered w-full"
    />
  </div>
  