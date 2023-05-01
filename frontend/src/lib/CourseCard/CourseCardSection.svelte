<script lang="ts">
  export let openStatus: string = "Open";
  export let crn: string = "12345";
  export let type: string = "LCD";
  export let section: string = "AY2";
  export let sectionStatus: string = "";
  export let startTime: string = "3:40";
  export let endTime: string = "4:30";
  export let day: string = "MWF";
  export let locations: any = [];
  export let instructors: any = [];
</script>

<tr class="text-xs font-light">
  <td>
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
  </td>
  <!-- <td>{section}</td> -->
  <!-- <td>{crn}</td> -->
  <td>{type}</td>
  <td class="w-fit pr-0">
    <div class="flex !flex-col gap-1 align-middle justify-center">
        <span class="badge bg-base-200 border-none rounded-full">{startTime}</span>
        {#if endTime}
        <span class="badge bg-base-200 border-none rounded-full">{endTime}</span>
        {/if}
    </div>
  </td>
  <td class="!pl-1">{day}</td>
  <td >
    <div class="flex !flex-row">
      {#each locations as location}
      <span>
        {location}
      </span>
      {/each}
    </div>
  </td>
  <td >
    <div class="flex !flex-row">
      {#each instructors as instructor}
      <span>
        {instructor}
      </span>
      {/each}
    </div>
  </td>
</tr>

<style>
  .radio:checked,
  .radio[aria-checked="true"] {
    box-shadow: 0 0 0 4px hsl(var(--b1)) inset, 0 0 0 4px hsl(var(--b1)) inset;
  }

</style>
