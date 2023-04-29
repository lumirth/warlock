<script lang="ts">
  export let openStatus: string = "";
  export let crn: string = "";
  export let type: string = "";
  export let section: string = "";
  export let time: string = "";
  export let day: string = "";
  export let location: string = "";
  export let instructor: string = "";
</script>

<tr
  class="bg-white dark:bg-gray-900 border dark:border-gray-600 text-gray-700 dark:text-gray-300 text-xs font-light"
>
  <td class="border-r dark:border-gray-600 p-1 text-center">{openStatus}</td>
  <td class="border-r dark:border-gray-600 p-1 text-center">{crn}</td>
  <td class="border-r dark:border-gray-600 p-1 text-center">{type}</td>
  <td class="border-r dark:border-gray-600 p-1 text-center">{section}</td>
  <td class="border-r dark border-gray-600 p-1 text-center">{time}</td>
  <td class="border-r dark:border-gray-600 p-1 text-center">{day}</td>
  <td class="border-r dark:border-gray-600 p-1 text-center">{location}</td>
  <td class="p-1 text-center">{instructor}</td>
</tr>
