<script lang="ts">
  import { onMount } from "svelte";
  import AdvancedSearch from "../lib/AdvancedSearch.svelte";
  import Modal from "../lib/Modal.svelte";
  import ModalButton from "../lib/ModalButton.svelte";
  import SearchForm from "../lib/SearchForm.svelte";
  import CourseCard from "../lib/CourseCard/CourseCard.svelte";
  import Help from "../lib/Help.svelte";
  import { sortByField } from "../sorting";
  import { dev } from "$app/environment";

  let query = "";
  let loading = false;
  let results: any = [];
  let returned_results: boolean = false;
  let adv_params: any;

  // Create a helper function to update loading state
  const updateLoading = (newState: boolean) => {
    loading = newState;
  };

  // Create a helper function to close advanced search modal
  const closeAdvancedSearchModal = () => {
    // @ts-ignore
    document.getElementById("modal-advanced").checked = false;
  };

  // Watch for results updates
  $: {
    // console.log("Results updated:", results);
    if (results.length > 0) {
      closeAdvancedSearchModal();
      updateLoading(false);
    }
  }

  // Watch for adv_params updates
  $: {
    if (adv_params) {
      closeAdvancedSearchModal();
      queryBackend();
    }
  }

  // this happens in two different places. here and in SearchForm.svelte. this needs to be fixed
  const queryBackend = async () => {
    try {
      let url = "";
      if (dev) url = "http://localhost:8000/search/advanced";
      else url = "https://warlock-backend.fly.dev/search/advanced";
      const response = await fetch(
        url,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(adv_params),
        }
      );
      const data = await response.json();
      results = data;
      returned_results = true;
      updateLoading(false);
    } catch (error) {
      console.error(error);
      loading = false;
      returned_results = true;
      results = [];
    }
  };

  onMount(() => {
    // code to execute when the component is mounted
  });
</script>

<svelte:head>
  <title>Course Warlock</title>
  <meta name="description" content="UIUC Course Search Engine" />
</svelte:head>

<section>
  <SearchForm bind:loading bind:query bind:results bind:returned_results />
  <ModalButton modalId="modal-advanced" label="ADVANCED" />
  <ModalButton modalId="modal-help" label="HELP" />
  <Modal modalId="modal-advanced" title="ADVANCED SEARCH">
    <p class="pt-2 text-xs text-neutral">
      • Please note that some field may override others (CRN, Course ID, etc.)
    </p>
    <p class="pb-2 text-xs text-neutral">
      • Fields with an <code>*</code> must be combined with at least 1 other field.
    </p>
    <AdvancedSearch bind:adv_params bind:loading />
  </Modal>

  <Modal modalId="modal-help" title="HELP">
    <Help />
  </Modal>
</section>
{#if results.length > 0}
  <hr class="border-neutral border-t my-4"/>
{/if}
<section class="">
  {#if returned_results && results.length == 0}
    <div class="flex justify-center bg-base-200 my-5 py-2 border border-neutral opacity-50">
      <p class="text-2xl font-mono uppercase text-neutral ">No results found</p>
    </div>
  {/if}
  <!-- for each result-->
  {#if results.length > 1}
    <!-- sort by GPA-->
    <div class="flex justify-end gap-1">
      <button
        class="btn btn-xs font-normal bg-base-100 border-none h-3 underline"
        on:click={() => (results = sortByField(results, "gpa_average", "id"))}
      >
        Sort by GPA
      </button>
      <button
        class="btn btn-xs font-normal bg-base-100 border-none h-3 underline mb-4"
        on:click={() => (results = sortByField(results, "creditHours", "id"))}
      >
        Sort by Credit Hours
      </button>
    </div>
  {/if}
  {#each results as result (result.id)}
    <CourseCard
      course={result}
    />
  {/each}
</section>