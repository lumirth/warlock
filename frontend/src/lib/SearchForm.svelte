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
    'Try typing a course',
    'Try typing a CRN',
    'Try typing a GenEd',
    'Try typing a keyword',
    'Try typing a subject',
    'Try typing a department',
    '"philosophy of mind"',
    '"data structures"',
    '"comp sci"',
    '"CS 222"',
    '"math257"',
    '"pysch 100"',
    '"music"',
    '"macs, western"',
    '"is:online, hrs:2"',
    '"adv comp, is:onl"',
    '"prof: fagen-ulmschneider"',
    '"life sci"',
    '"g:QR2, g:NAT"',
    '"psych, behavioral sci"',
    '"fall, 2004, phil"',
    '"anthro, 2019"',
    '"math, hrs:2"',
    '"nonwestern, philosophy"',
    '"minority, pot:b"',
    '"BUS 3, is:open"',
    '"astronomy"',
    '"prof: cole"',
  ];

  let placeholder_example = '';

  const randomExample = () => {
    let previous = placeholder_example;
    placeholder_example =
      examples[Math.floor(Math.random() * examples.length)];
    while (placeholder_example === previous) {
      placeholder_example =
        examples[Math.floor(Math.random() * examples.length)];
    }
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
    }, 1500);
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
