<script lang="ts">
  export let openStatus: string = "Open";
  export let crn: string = "12345";
  export let type: string = "LCD";
  export let section: string = "AY2";
  export let sectionStatus: string = "";
  export let time: string = "3:40";
  export let day: string = "MWF";
  export let location: string = "David Kinley Hall 200";
  export let instructor: string = "Fagen-Ulmschneider, W";
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
  <td>
    
    <span class="badge bg-base-200 border-none rounded-full">{time}</span>
  </td>
  <td>{day}</td>
  <td class="whitespace-pre">
    <div class="flex !flex-col">
      <div>
        {location}
      </div>
    </div>
  </td>
  <td>{instructor}</td>
</tr>

<style>
  .radio:checked,
  .radio[aria-checked="true"] {
    box-shadow: 0 0 0 4px hsl(var(--b1)) inset, 0 0 0 4px hsl(var(--b1)) inset;
  }

</style>
