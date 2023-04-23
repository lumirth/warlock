<script lang="ts">
  import { onMount } from "svelte";
  import Counter from "./Counter.svelte";
  import AdvancedSearch from "../lib/AdvancedSearch.svelte";

  let x = 0;
  let query = "";
  let output = "";
  let loading = false;

  
  const increment = () => {
    x++;
  };

  const queryBackend = async () => {
    const response = await fetch(
      "http://localhost:8000/search/simple?query=" + query
    );
  };

  const handleSubmit = (event: Event) => {
    event.preventDefault();
    queryBackend();
    if (output === "") {
      output = "NO BACKEND RESPONSE";
    }
    loading = true;
    setTimeout(() => {
      loading = false;
    }, 10000);
  };

  onMount(() => {
    // code to execute when the component is mounted
  });
</script>

<svelte:head>
  <title>Course Warlock</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<!-- <div class="radial-progress text-xs bg-primary text-primary-content border-4 border-primary" style="--value:70; --size:2rem; --thickness: 3px;">3.5</div> -->
<section>
  <form on:submit={handleSubmit} class="flex gap-4 mx-auto">
    <input
      type="text"
      placeholder="ENTER QUERY..."
      class="flex-grow input hover:border-primary input-bordered w-2/3 md:w-4/5 lg:w-4/5 xl:w-5/6 bg-base-200 text-lg font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent"
      bind:value={query}
    />
    <button
      type="submit"
      class="btn bg-base-200 font-normal text-lg {loading ? 'loading' : ''}"
      >SEARCH</button
    >
  </form>
  <label
    for="modal-advanced"
    class="btn btn-xs mt-4 font-normal bg-base-100 border-none h-3 underline"
    >ADVANCED</label
  >
  <label
    for="modal-syntax"
    class="btn btn-xs mt-4 font-normal bg-base-100 border-none h-3 underline"
    >SYNTAX</label
  >
  <label
    for="modal-examples"
    class="btn btn-xs mt-4 font-normal bg-base-100 border-none h-3 underline"
    >EXAMPLES</label
  >
  {#if output}
    <div class="toast">
      <div class="alert alert-info bg-primary">
        <div>
          <span class="font-mono">OUTPUT: {output}</span>
        </div>
      </div>
    </div>
  {/if}

  <input type="checkbox" id="modal-advanced" class="modal-toggle" />
  <label
    for="modal-advanced"
    class="modal modal-bottom sm:modal-middle cursor-pointer"
  >
    <label class="modal-box relative" for="">
      <label
        for="modal-advanced"
        class="btn btn-sm absolute right-2 top-2 border-neutral bg-base-200"
        >✕</label
      >
      <h3 class="text-lg font-bold">ADVANCED SEARCH</h3>
      <!-- <p class="py-4">TODO: implement full advanced search with correct forms</p> -->
      <p class="py-2 text-xs text-neutral">Please note that some field may override others (CRN, Course ID, etc.)</p>
      <AdvancedSearch />
    </label>
  </label>
  <input type="checkbox" id="modal-syntax" class="modal-toggle" />
  <label
    for="modal-syntax"
    class="modal modal-bottom sm:modal-middle cursor-pointer"
  >
    <label class="modal-box relative" for="">
      <label
        for="modal-syntax"
        class="btn btn-sm absolute right-2 top-2 border-neutral bg-base-200"
        >✕</label
      >
      <article class="prose prose-sm">
        <h3 class="text-lg font-bold">QUERY SYNTAX</h3>
        <p>
          The search box takes a comma-separated list of arguments. It will
          attempt to intelligently match your input for the following:
        </p>
        <ul>
          <li>
            Subject/course codes (<code>CS 225; macs356; mathematics</code>)
          </li>
          <li>
            GenEds (<code>adv comp; humanities & the arts; life sciences</code>)
          </li>
        </ul>
        <p>You can also input the following:</p>
        <ul>
          <li>CRNs (<code>12345; 54321</code>)</li>
          <li>Years (<code>2022; 2004</code>)</li>
          <li>
            Terms (<code>fall; spring; summer; winter; fa; sp; su; wi</code>)
          </li>
        </ul>
        <p>Or you can declare values explicitly:</p>
        <ul>
          <li>Subject/department (<code>subj:CS; d:MATH; dept: CPSC</code>)</li>
          <li>Course ID (<code>course:225; id: 107</code>)</li>
          <li>Year (<code>yr:2009; year:2011</code>)</li>
          <li>Term (<code>term:fall; t:sp</code>)</li>
          <li>CRN (<code>crn:12345</code>)</li>
          <li>Credit hours (<code>hrs:3; hr: 1</code>)</li>
          <li>GenEd (<code>gen:adv comp; g:hum</code>)</li>
          <li>
            Part of Term (<code>pot:first; p: whole; part-of-term:all</code>)
          </li>
          <li>
            Keyword (<code
              >q: minds and machines; keyword: advanced applications</code
            >)
          </li>
        </ul>
      </article>
    </label>
  </label>
  <input type="checkbox" id="modal-examples" class="modal-toggle" />
  <label
    for="modal-examples"
    class="modal modal-bottom sm:modal-middle cursor-pointer"
  >
    <label class="modal-box relative" for="">
      <label
        for="modal-examples"
        class="btn btn-sm absolute right-2 top-2 border-neutral bg-base-200"
        >✕</label
      >
      <h3 class="text-lg font-bold">EXAMPLES</h3>
      <p class="py-4">TODO: give easy top understand query examples</p>
    </label>
  </label>
</section>

<style>
</style>
