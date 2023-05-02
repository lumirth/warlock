<script lang="ts">
  import RadialRating from "./RadialRating.svelte";
  // TODO: just pass the whole section object to this component and let it handle the rest
  export let section;

  let openStatus = section.enrollmentStatus;
  let sectionStatus = section.statusCode;
  let sectionNumber = section.sectionNumber;
  let crn = section.id;
  let types = section.meetings.map((meeting: any) => {
    const type = meeting.typeCode ?? "";
    return type.charAt(0).toUpperCase() + type.slice(1);
  });
  let times = section.meetings.map((meeting: any) => {
    const startTime = meeting.start ?? "";
    const endTime = meeting.end ?? "";
    if (startTime == "" && endTime == "") return "";
    if (endTime == "") return `${startTime}`.trim();
    return `${startTime} - ${endTime}`.trim();
  });
  let days = section.meetings.map((meeting: any) => {
    const days = meeting.daysOfTheWeek ?? "";
    return days;
  });
  let locations = section.meetings.map((meeting: any) => {
    const buildingName = meeting.buildingName ?? "";
    const roomNumber = meeting.roomNumber ?? "";
    return `${buildingName} ${roomNumber}`.trim();
  });
  let instructors = section.meetings.map((meeting: any) =>
    meeting.instructors
      .map(
        (instructor: any) =>
          `${instructor.firstName} ${instructor.lastName}`
      )
      .join(", ")
  );
  // for each list of instructors, average their ratings
  let ratings = section.meetings.map((meeting: any) => {
    const instructors = meeting.instructors;
    if (instructors.length == 0) return 0;
    const ratings = instructors.map(
      (instructor: any) => instructor.avg_rating
    );
    // sum all non-zero ratings and divide by the number of non-zero ratings
    const sum = ratings.reduce((a: any, b: any) => a + b, 0);
    const count = ratings.filter((rating: any) => rating != 0).length;
    return sum / count;
  });
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
  <td >
    <div class="flex !flex-col">
      {#each ratings as rating}
      {#if rating != 0}
      <span>
        <RadialRating value={rating} maxValue={5.0}/>
        <span>
          &nbsp;{rating}&nbsp;&nbsp;
        </span>
      </span>
      {/if}
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
