<!-- ModalButton.svelte -->
<script lang="ts">
    export let modalId: string;
    export let label: string;
  </script>
  
  <label
    for="{modalId}"
    class="btn btn-xs mt-4 font-normal bg-base-100 border-none h-3 underline"
  >
    {label}
  </label>
  