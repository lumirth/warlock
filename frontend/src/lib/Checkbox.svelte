<script lang="ts">
  export let id: string;
  export let label: string;
  export let checked: boolean;
</script>
<div class="form-control !mt-0">
  <label for="{id}" class="label cursor-pointer">
    <span class="label-text">{label}</span> 
    <input type="checkbox" id="{id}" class="checkbox font-normal placeholder-neutral checkbox-primary bg-base-200 border-neutral focus:outline-none hover:border-primary focus:placeholder-transparent" bind:checked="{checked}"/>
  </label>
</div>