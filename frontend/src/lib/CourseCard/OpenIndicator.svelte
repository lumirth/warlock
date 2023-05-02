<script lang="ts">
    export let openStatus: string;
    export let sectionStatus: string;
</script>
{#if openStatus == "Open"}
<div class="flex justify-start">
  <input
    type="radio"
    class="flex justify-center radio radio-sm radio-success cursor-default"
    checked
  />
</div>
{:else if openStatus == "Open (Restricted)" || openStatus == "CrossListOpen (Restricted)"}
<div class="flex justify-start">
  <input
    type="radio"
    class="flex justify-center radio radio-sm radio-warning cursor-default"
    checked
  />
</div>
{:else if openStatus == "UNKNOWN"}
<div class="flex justify-start">
  <input
    type="radio"
    class="flex justify-center radio radio-sm !bg-base-100 !text-base-100 !border-neutral cursor-default"
    checked
  />
</div>
{:else if sectionStatus == "P"}
<div class="flex justify-start">
  <input
    type="radio"
    class="flex justify-center radio radio-sm radio-primary !bg-base-100 !text-base-100 cursor-default"
    checked
  />
</div>
{:else}
<div class="flex justify-start">
  <input
    type="radio"
    class="flex justify-center radio radio-sm radio-error cursor-default"
    checked
  />
</div>
{/if}
