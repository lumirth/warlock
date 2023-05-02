<script lang="ts">
  // TODO: just pass the whole section object to this component and let it handle the rest
  export let openStatus: string = "Open";
  export let crn: string = "12345";
  export let section: string = "AY2";
  export let sectionStatus: string = "";
  export let times: any = [];
  export let days: any = [];
  export let types: any = [];
  export let locations: any = [];
  export let instructors: any = [];
</script>

<tr class="text-xs font-light">
  <!-- TODO: add explanation somewhere of what different colors mean-->
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
  <td >
    <div class="flex !flex-col">
      {#each types as type}
      <span>
        {type}&nbsp;
      </span>
      {/each}
    </div>
  </td>
  <td >
    <div class="flex !flex-col">
      {#each times as time}
      <span >
        {time}
      </span>
      {/each}
    </div>
  </td>
  <!-- <td class="w-fit pr-0">
    <div class="flex !flex-col gap-1 align-middle justify-center">
        <span class="badge bg-base-200 border-none rounded-full">{startTime}</span>
        {#if endTime}
        <span class="badge bg-base-200 border-none rounded-full">{endTime}</span>
        {/if}
    </div>
  </td> -->
  <!-- todo fix the fact that spaces are gone -->
  <td >
    <div class="flex !flex-col">
      {#each days as day}
      <span>
        {day}&nbsp;
      </span>
      {/each}
    </div>
  </td>
  <td >
    <div class="flex !flex-col">
      {#each locations as location}
      <span>
        {location}&nbsp;
      </span>
      {/each}
    </div>
  </td>
  <td >
    <div class="flex !flex-col">
      {#each instructors as instructor}
      <span>
        {instructor}&nbsp;
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
