<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";

  export let query = "";
  export let loading = false;
  export let results: any = [];

  const examples = [
    "CS 222",
    "math257",
    "pysch 101",
    "MACS, western",
    "hrs:1, is:online",
    "gen:HUM, is:campus",
    "adv comp, pot:b",
    "prof: wade",
    "keyword: data",
    "life sciences",
    "natural sciences, quant1",
    "PSYC, non-western",
    "fall, 2021, cs 128",
    "anthropology, 2019",
    "2005, mathematics, hrs:2",
  ];

  let placeholder_example = "";

  const randomExample = () => {
    placeholder_example =
      '"' + examples[Math.floor(Math.random() * examples.length)] + '"';
  };

  const dispatch = createEventDispatcher();

  const handleSubmit = (event: Event) => {
    results = [];
    queryBackend();
    event.preventDefault();
    dispatch("submit", query);
    loading = true;
    setTimeout(() => {
      loading = false;
    }, 10000);
  };

  const queryBackend = async () => {
    const response = await fetch(
      "http://localhost:8000/search/simple?query=" + query
    );
    const data = await response.json();
    results = data;
  };

  export { placeholder_example };

  onMount(() => {
    randomExample();
    // code to execute when the component is mounted
  });
</script>

<form on:submit={handleSubmit} class="flex gap-4 mx-auto sm:mt-0">
  <input
    type="text"
    placeholder={placeholder_example}
    class="flex-grow input hover:border-primary input-bordered w-2/3 md:w-4/5 lg:w-4/5 xl:w-5/6 bg-base-200 text-lg font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent"
    bind:value={query}
  />
  {#if loading}
    <button class="btn bg-base-200 font-normal text-lg loading">LOADING</button>
  {:else}
    <button type="submit" class="btn bg-base-200 font-normal text-lg"
      >SEARCH</button
    >
  {/if}
</form>
