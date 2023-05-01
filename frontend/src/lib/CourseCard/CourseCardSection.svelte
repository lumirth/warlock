<script lang="ts">
  export let openStatus: string = "Open";
  export let crn: string = "12345";
  export let type: string = "LCD";
  export let section: string = "AY2";
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
          class="flex justify-center radio radio-sm radio-success !border-neutral"
          checked
        />
      </div>
    {:else}
      <div class="flex justify-start">
        <input
          type="radio"
          class="flex justify-center radio radio-sm radio-error !border-neutral"
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
  <td>{location}</td>
  <td>{instructor}</td>
</tr>

<style>
  .radio:checked,
  .radio[aria-checked="true"] {
    box-shadow: 0 0 0 4px hsl(var(--b2)) inset, 0 0 0 4px hsl(var(--b2)) inset;
  }

</style>
