<script lang="ts">
  import { onMount } from "svelte";
  import Counter from "./Counter.svelte";

  let x = 0;
  let query = "";
  let output = "";

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
        output = 'NO BACKEND RESPONSE';
    }
  };

  onMount(() => {
    // code to execute when the component is mounted
  });
</script>

<svelte:head>
  <title>Home</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
  <form on:submit={handleSubmit} class="flex gap-4">
    <input
      type="text"
      placeholder="ENTER QUERY..."
      class="input input-bordered w-2/3 md:w-4/5 lg:w-4/5 xl:w-5/6 bg-base-200 text-lg font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent"
      bind:value={query}
    />
    <button
      type="submit"
      class="btn w-1/3 md:w-1/5 lg:w-1/5 xl:w-1/6 bg-base-200 font-normal text-lg"
      >SEARCH</button
    >
  </form>
  <label for="my-modal-4" class="btn btn-sm mt-4 font-normal bg-base-100 border-none h-3 underline">ADVANCED</label>
  <label for="my-modal-5" class="btn btn-sm mt-4 font-normal bg-base-100 border-none h-3 underline">WHAT IS A QUERY?</label>
  {#if output}
    <div class="toast">
      <div class="alert alert-info bg-primary">
        <div>
          <span class="font-mono">OUTPUT: {output}</span>
        </div>
      </div>
    </div>
  {/if}

<input type="checkbox" id="my-modal-4" class="modal-toggle" />
<label for="my-modal-4" class="modal modal-bottom sm:modal-middle cursor-pointer">
<label class="modal-box relative" for="">
    <label for="my-modal-4" class="btn btn-xs absolute right-2 top-2 border-neutral bg-base-200">✕</label>
    <h3 class="text-lg font-bold">ADVANCED SEARCH</h3>
    <p class="py-4">TODO: implement the advanced search fields here</p>
</label>
</label>
<input type="checkbox" id="my-modal-5" class="modal-toggle" />
<label for="my-modal-5" class="modal modal-bottom sm:modal-middle cursor-pointer">
<label class="modal-box relative" for="">
    <label for="my-modal-5" class="btn btn-xs absolute right-2 top-2 border-neutral bg-base-200">✕</label>
    <h3 class="text-lg font-bold">QUERY SYNTAX</h3>
    <p class="py-4">TODO: explain how queries work in a way normies can understand</p>
</label>
</label>
</section>

<style>
</style>
