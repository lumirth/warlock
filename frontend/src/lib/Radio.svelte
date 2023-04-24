<script lang="ts">
  export let id: string;
  export let label: string;
  export let value: string;
  export let groupValue: string;
  export let onChange: (value: string) => void;
</script>

<div class="form-control !mt-0">
  <label for="{id}" class="label cursor-pointer !select-none">
    <span class="label-text">{label}</span> 
    <input 
      type="radio" 
      id="{id}" 
      class="radio radio-primary font-normal placeholder-neutral bg-base-200 border-neutral focus:outline-none hover:border-primary focus:placeholder-transparent" 
      name="radio-{id}" 
      bind:group="{groupValue}"
      value="{value}"
      on:change="{() => onChange(value)}" />
  </label>
</div>
