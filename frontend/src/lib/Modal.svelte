<script lang="ts">
  export let modalId = "";
  export let title = "";
  export let content = null;
</script>

<input type="checkbox" id={modalId} class="modal-toggle" />
<label for={modalId} class="modal modal-bottom sm:modal-middle cursor-pointer">
  <label class="modal-box relative no-scrollbar" for="">
    <label
      for={modalId}
      class="btn btn-sm absolute right-2 top-2 border-neutral bg-base-200"
      >✕</label
    >
    <h3 class="text-lg font-bold">{title}</h3>
    <slot />
  </label>
</label>
