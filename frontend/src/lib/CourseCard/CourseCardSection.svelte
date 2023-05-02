<script lang="ts">
  import RadialRating from "./RadialRating.svelte";
  import OpenIndicator from "./OpenIndicator.svelte";
  import Cell from "./Cell.svelte";
  export let section: any;
  export let last: boolean = false;
  let showDetails: boolean = false;

  let openStatus = section.enrollmentStatus;
  let sectionStatus = section.statusCode;

  const toggleDetails = () => {
    showDetails = !showDetails;
  };

  const convertTZ = (date: string, tzString: string) => {
    return new Date(
      (typeof date === "string"
        ? new Date(date.substring(0, date.length - 1))
        : date
      ).toLocaleString("en-US", { timeZone: tzString })
    );
  };

  console.log(section.meetings[section.meetings.length - 1]);
</script>

{#each section.meetings as meeting}
  <tr
    on:click={toggleDetails}
    class="text-xs font-light cursor-pointer [&>td]:py-0 {JSON.stringify(
      meeting
    ) === JSON.stringify(section.meetings[section.meetings.length - 1]) &&
    section.meetings.length !== 1 &&
    !last
      ? '[&>td]:!pb-2'
      : ''}"
  >
    {#if meeting === section.meetings[0]}
      <td rowspan={section.meetings.length}>
        <OpenIndicator {openStatus} {sectionStatus} />
      </td>
    {/if}
    {#if meeting === section.meetings[0]}
      <td rowspan={section.meetings.length}>
        <span class="p-1 my-0.5 rounded-2xl bg-base-200 px-2">
          <span class="pr-0">
            {section.sectionNumber}
          </span>
        </span>
      </td>
    {/if}
    <Cell>
      <span>
        {meeting.typeCode}
      </span>
    </Cell>
    <Cell>
      <span class="p-1 my-0.5 flex flex-col w-fit">
        {#if meeting.start && meeting.end}
          <span class="flex flex-col p-1">
            <span class="leading-3 flex-nowrap">
              {meeting.start} - {meeting.end}
            </span>
          </span>
        {:else if meeting.start}
          <span class="flex flex-col p-1 leading-3 flex-nowrap">
            {meeting.start}
          </span>
        {:else if meeting.end}
          <span class="flex flex-col p-1 leading-3 flex-nowrap">
            {meeting.end}
          </span>
        {/if}
      </span>
    </Cell>
    <Cell>
      <span>
        {#if meeting.daysOfTheWeek}
          {meeting.daysOfTheWeek}
        {/if}
      </span>
    </Cell>
    <Cell>
      <span>
        {#if meeting.buildingName}
          {meeting.buildingName} {meeting.roomNumber}&nbsp;
        {/if}
      </span>
    </Cell>
    <Cell>
      <span class="rounded-xl bg-base-200 flex flex-col p-1 my-0.5 w-fit mr-2">
        <table class="[&>tr>td]:py-0">
          {#each meeting.instructors as instructor}
            <tr>
              <td class="!pl-1 !pr-1 leading-3">
                {instructor.firstName}
                {instructor.lastName}
              </td>
              <td class="text-right leading-3 align-middle flex flex-row gap-2">
                {#if instructor.avg_rating}
                  <RadialRating value={instructor.avg_rating} maxValue={5.0} />
                  <span class="self-center !pr-0">
                    {parseFloat(instructor.avg_rating).toFixed(1)}
                  </span>
                {:else}
                  <div
                    class="radial-progress bg-neutral text-neutral border-2 border-neutral"
                    style="--value:0; --size:1rem; --thickness:3px;"
                  />
                  <span class="text-neutral self-center"> N/A </span>
                {/if}
              </td>
            </tr>
          {/each}
        </table>
      </span>
    </Cell>
  </tr>
{/each}

{#if showDetails}
  <tr>
    <td colspan="100" class="pb-4">
      <table class="table table-compact [&>tr>td]:!py-0">
        <tr>
          <td>Status:</td>
          <td
            >{section.enrollmentStatus}{#if section.statusCode === "P"}(Pending){/if}</td
          >
        </tr>
        <tr>
          <td>CRN:</td>
          <td>{section.id}</td>
        </tr>
        <tr>
          <td
            >Type{#if section.meetings.length > 1}s{/if}:</td
          >
          <td>
            {#each section.meetings as meeting}
              {#if meeting === section.meetings[section.meetings.length - 1]}
                {meeting.typeDesc}
              {:else}
                {meeting.typeDesc},&nbsp;
              {/if}
            {/each}
          </td></tr
        >
        {#if section.startDate && section.endDate}
          <tr>
            <td>Date:</td>
            <td
              >{convertTZ(
                section.startDate,
                "America/Chicago"
              ).toLocaleDateString()} - {convertTZ(
                section.endDate,
                "America/Chicago"
              ).toLocaleDateString()}</td
            >
          </tr>
        {/if}
        {#if section.partOfTerm}
          <tr>
            <td>Part of Term:</td>
            <td>{section.partOfTerm}</td>
          </tr>
        {/if}
        {#if section.sectionText}
          <tr class="box-content">
            <td class="!py-0 align-top">Section Info:</td>
            <td
              class="!py-0 whitespace-pre-wrap max-w-[220px] sm:max-w-[350px] md:max-w-[450px]"
            >
              {section.sectionText}
            </td>
          </tr>
        {/if}
        {#if section.sectionNotes}
          <tr class="box-content">
            <td class="!py-0 align-top">Restrictions:</td>
            <td
              class="!py-0 whitespace-pre-wrap max-w-[220px] sm:max-w-[350px] md:max-w-[450px]"
            >
              {section.sectionNotes}
            </td>
          </tr>
        {/if}
      </table>
    </td>
  </tr>
{/if}

<style>
  .radio:checked,
  .radio[aria-checked="true"] {
    box-shadow: 0 0 0 4px hsl(var(--b1)) inset, 0 0 0 4px hsl(var(--b1)) inset;
  }
</style>
