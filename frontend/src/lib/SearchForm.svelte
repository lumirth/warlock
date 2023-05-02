<script lang='ts'>
  import { createEventDispatcher, onMount } from 'svelte';
  import { dev } from '$app/environment';
  import { fade } from 'svelte/transition';

  export let query = '';
  export let loading = false;
  export let returned_results: boolean = false;
  export let results: any = [];

  const examples = [
    'Try typing a course title',
    'Try typing a course ID',
    'Try typing a CRN',
    'Try typing the name of a GenEd',
    'Try typing a keyword',
    '"comp sci"',
    '"CS 222"',
    '"math257"',
    '"pysch 100"',
    '"mus"',
    '"MACS, western"',
    '"is:online, hrs:2"',
    '"gen:ADVCOMP, is:online"',
    '"prof: fagen-ulmschneider"',
    '"life sciences"',
    '"gen: QR2, gen: NAT"',
    '"PSYC, behavioral science"',
    '"fall, 2004, phil"',
    '"anthropology, 2019"',
    '"2005, mathematics, hrs:2"',
    '"hrs:3, phil, nonwestern"',
    '"pot:b, us minority"',
    '"bus 3, is:open"',
    '"astronomy"',
    '"prof: cole"',
  ];

  let placeholder_example = '';

  const randomExample = () => {
    placeholder_example =
      examples[Math.floor(Math.random() * examples.length)];
  };

  const dispatch = createEventDispatcher();

  const handleSubmit = (event: Event) => {
    results = [];
    returned_results = false;
    loading = true;
    queryBackend();
    event.preventDefault();
    dispatch('submit', query);
  };

  const queryBackend = async () => {
    try {
      let url: string = '';
      if (dev) url = 'http://localhost:8000/search/simple?query=';
      else url = 'https://warlock-backend.fly.dev/search/simple?query=';
      const response = await fetch(
        url + encodeURIComponent(query)
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
    setInterval(() => {
      randomExample();
    }, 2000);
  });
</script>

<form on:submit={handleSubmit} class='flex gap-4 mx-auto sm:mt-0'>
  <div class='relative flex-grow'>
    <input
      type='text'
      class='flex-grow input hover:border-primary input-bordered w-full bg-base-200 text-lg font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent peer'
      bind:value={query}
    />
    <!-- hide when peer is not empty-->
    <div class='absolute top-0 left-0 w-full peer-focus:opacity-0 pointer-events-none {query === '' ? 'opacity-100' : 'opacity-0'}'>
      <!-- use fade-->
      {#each [placeholder_example] as example (example)}
        <span
          in:fade={{ duration: 250, delay: 250 }}
          out:fade={{ duration: 250 }}
          class='text-lg font-normal text-neutral absolute w-11/12 top-1.5 left-1.5 px-3 py-1 select-none overflow-x-hidden whitespace-nowrap'
        >
          {example}
        </span>
      {/each}
    </div>
    <!-- well-placed placeholder div -->
  </div>

  
  {#if loading}
    <button class='btn bg-base-200 font-normal text-lg loading'>LOADING</button>
  {:else}
    <button type='submit' class='btn bg-base-200 font-normal text-lg'
      >SEARCH</button
    >
  {/if}
</form>
