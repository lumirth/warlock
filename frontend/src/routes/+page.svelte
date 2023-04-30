<script lang="ts">
  import { onMount } from "svelte";
  import AdvancedSearch from "../lib/AdvancedSearch.svelte";
  import Modal from "../lib/Modal.svelte";
  import ModalButton from "../lib/ModalButton.svelte";
  import SearchForm from "../lib/SearchForm.svelte";
  import CourseCard from "../lib/CourseCard/CourseCard.svelte";

  let x = 0;
  let query = "";
  let loading = false;
  let results: any = [];
  let returned_results: boolean = false;
  let adv_params: any;

  $: {
    console.log("Results updated:", results);
    // update loading to false if results are not empty
  }
  $: {
    if (results.length > 0) {
      loading = false;
      // close advanced search modal
      // toggle checkbox with id="modal-advanced"
      // @ts-ignore
      document.getElementById("modal-advanced").checked = false;
    }
  }

  $: {
    // console.log("Advanced params updated:", adv_params);
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


  const sortByGPA = () => {
    // if already sorted by GPA, reverse the array
    let isAlreadySorted = true;
    for (let i = 0; i < results.length - 1; i++) {
      if (results[i].gpa_average < results[i + 1].gpa_average) {
        isAlreadySorted = false;
        break;
      }
    }
    if (isAlreadySorted) {
      results = results.reverse();
    } else {
      results = results.sort((a:any, b:any) => b.gpa_average - a.gpa_average);
    }
  }
  const sortByHours = () => {
    // if already sorted by hours, reverse the array
    let isAlreadySorted = true;
    for (let i = 0; i < results.length - 1; i++) {
      if (results[i].creditHours < results[i + 1].creditHours) {
        isAlreadySorted = false;
        break;
      }
    }
    if (isAlreadySorted) {
      results = results.reverse();
    } else {
      results = results.sort((a:any, b:any) => b.creditHours - a.creditHours);
    }

  }
  
  const increment = () => {
    x++;
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
  <ModalButton modalId="modal-syntax" label="SYNTAX" />
  <ModalButton modalId="modal-examples" label="EXAMPLES" />
  <Modal modalId="modal-advanced" title="ADVANCED SEARCH">
    <p class="pt-2 text-xs text-neutral">
      • Please note that some field may override others (CRN, Course ID, etc.)
    </p>
    <p class="pb-2 text-xs text-neutral">
      • Fields with an <code>*</code> must be combined with at least 1 other field.
    </p>
    <AdvancedSearch bind:adv_params bind:loading/>
  </Modal>

  <Modal modalId="modal-syntax" title="QUERY SYNTAX">
    <div class="prose text-sm pt-2 select-text cursor-text">
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
    </div>
  </Modal>

  <Modal modalId="modal-examples" title="EXAMPLES">
    <div class="prose text-sm pt-2 select-text cursor-text">
      <p>
        Find courses in the MACS department that match the Cultural Studies:
        Western GenEd:
      </p>
      <ul>
        <li><code>macs, western</code></li>
        <li><code>media and cinema studies, cultural studies western</code></li>
        <li>Specifically at the 300 level: <code>MACS 3, g:west</code></li>
        <li>Worth 3 credit hours: <code>MACS, g:west, hrs:3</code></li>
        <li>Online: <code>MACS, western, is:online</code></li>
        <li>First eight weeks: <code>macs, western, pot:a</code></li>
      </ul>
    </div>
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
      on:click={sortByGPA}
    >
      Sort by GPA
    </button>
    <button class="flex justify-end btn btn-sm bg-transparent border-transparent underline mb-5" on:click={sortByHours}>
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
      href = {result.href}
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
