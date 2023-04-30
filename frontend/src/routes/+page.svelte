<script lang="ts">
  import { onMount } from "svelte";
  import AdvancedSearch from "../lib/AdvancedSearch.svelte";
  import Modal from "../lib/Modal.svelte";
  import ModalButton from "../lib/ModalButton.svelte";
  import SearchForm from "../lib/SearchForm.svelte";
  import CourseCard from "../lib/CourseCard/CourseCard.svelte";
  import Help from "../lib/Help.svelte";
  import { sortByField } from "../sorting";

  let x = 0;
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
    console.log("Results updated:", results);
    if (results.length > 0) {
      updateLoading(false);
      closeAdvancedSearchModal();
    }
  }

  // Watch for adv_params updates
  $: {
    if (adv_params) {
      queryBackend();
    }
  }

  const queryBackend = async () => {
    const response = await fetch(
      "https://warlock-backend.fly.dev/search/advanced",
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
  };

  onMount(() => {
    // code to execute when the component is mounted
  });
</script>

<svelte:head>
  <title>Course Warlock</title>
  <meta name="description" content="Svelte demo app" />
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
<section class="pt-20">
  {#if returned_results && results.length == 0}
    <div class="flex justify-center">
      <p class="text-2xl font-mono uppercase">No results found</p>
    </div>
  {/if}
  <!-- for each result-->
  {#if results.length > 0}
    <!-- sort by GPA-->
    <div class="flex justify-end">
      <button
        class="flex justify-end btn btn-sm bg-transparent border-transparent underline mb-5"
        on:click={() => (results = sortByField(results, "gpa_average", "id"))}
      >
        Sort by GPA
      </button>
      <button
        class="flex justify-end btn btn-sm bg-transparent border-transparent underline mb-5"
        on:click={() => (results = sortByField(results, "creditHours", "id"))}
      >
        Sort by Credit Hours
      </button>
    </div>
  {/if}
  {#each results as result}
    <CourseCard
      course_id={result.id}
      course_detail={result.label}
      sem_code={result.term[0] +
        result.term[1] +
        result.year[2] +
        result.year[3]}
      credit_hours={result.creditHours}
      description={result.description}
      average_gpa={result.gpa_average ? result.gpa_average : 0}
      tags_text={result.genEdAttributes
        ? result.genEdAttributes.map((genEd) => genEd.id)
        : []}
      href={result.href}
    />
  {/each}
</section>

<style>
  .no-scrollbar {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important; /* IE and Edge */
  }
  .no-scrollbar::-webkit-scrollbar {
    display: none !important;
  }
</style>
