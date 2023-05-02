<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";

  export let query = "";
  export let loading = false;
  export let returned_results: boolean = false;
  export let results: any = [];

  const examples = [
    "comp sci",
    "CS 222",
    "math257",
    "pysch 100",
    "mus",
    "MACS, western",
    "is:online, hrs:2",
    "gen:ADVCOMP, is:online",
    "prof: fagen-ulmschneider",
    "life sciences",
    "gened: QR2, gened: NAT",
    "PSYC, behavioral science",
    "fall, 2004, phil",
    "anthropology, 2019",
    "2005, mathematics, hrs:2",
    "hrs:3, phil, nonwestern",
    "pot:b, us minority",
    "bus 3, is:open",
    "astronomy",
    "prof: cole",
  ];

  let placeholder_example = "";

  const randomExample = () => {
    placeholder_example =
      '"' + examples[Math.floor(Math.random() * examples.length)] + '"';
  };

  const dispatch = createEventDispatcher();

  const handleSubmit = (event: Event) => {
    results = [];
    returned_results = false;
    loading = true;
    queryBackend();
    event.preventDefault();
    dispatch("submit", query);
  };

  const queryBackend = async () => {
    try {
      const response = await fetch(
        "https://warlock-backend.fly.dev/search/simple?query=" + encodeURIComponent(query)
      );
      const data = await response.json();
      results = data;
      returned_results = true;
      loading = false;
    } catch (error) {
      console.error(error);
      loading = false;
      returned_results = true;
      results = [];
    }
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
