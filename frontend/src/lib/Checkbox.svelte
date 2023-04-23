<script lang="ts">
  export let id: string;
  export let label: string;
  export let checked: boolean;
</script>
<div class="form-control">
  <label for="{id}" class="label cursor-pointer">
    <span class="label-text">{label}</span> 
    <input type="checkbox" id="{id}" class="checkbox" bind:checked="{checked}"/>
  </label>
</div>