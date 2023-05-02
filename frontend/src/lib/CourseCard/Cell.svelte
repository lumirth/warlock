<script lang="ts">
  export let addClass: string = "";
</script>
<td class="{addClass}">
  <div class="flex !flex-col">
    <slot />
  </div>
</td>
