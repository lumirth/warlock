<script>
    import Counter from './Counter.svelte';
    let x=0;

    const increment = () => {
        x++;
    }
</script>

<svelte:head>
    <title>Home</title>
    <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
    <form  on:submit|preventDefault={increment} class="flex gap-4">
        <input  type="text" placeholder="ENTER QUERY..." class="input input-bordered w-2/3 md:w-4/5 lg:w-4/5 xl:w-5/6 bg-base-200 text-lg font-normal placeholder-neutral focus:outline-none focus:border-primary focus:placeholder-transparent" />
        <button class="btn w-1/3 md:w-1/5 lg:w-1/5 xl:w-1/6 bg-base-200 font-normal text-lg">SEARCH</button>
    </form>
    <div class="flex items-start form-control pt-2">
      <label class="label">
          <input type="checkbox" on:click={increment} class="checkbox checkbox-primary bg-base-200 border-neutral hover:border-neutral focus:border-neutral">
          <span class="label-text pl-3 cursor-pointer">ADVANCED SEARCH</span>
        </label>
    </div> 
</section>

<style>
</style>
