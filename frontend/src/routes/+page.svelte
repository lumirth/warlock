<script lang="ts">
  import { onMount } from "svelte";
  import AdvancedSearch from "../lib/AdvancedSearch.svelte";
  import Modal from "../lib/Modal.svelte";
  import ModalButton from "../lib/ModalButton.svelte";
  import SearchForm from "../lib/SearchForm.svelte";

  let x = 0;
  let output = "";
  let query = "";
  let loading = false;

  const increment = () => {
    x++;
  };

  const queryBackend = async () => {
    const response = await fetch(
      "http://localhost:8000/search/simple?query=" + query
    );
  };

  const handleSearchSubmit = (event: Event) => {
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

<section>
  <SearchForm on:submit="{handleSearchSubmit}" bind:loading={loading} bind:query={query}/>
  <ModalButton modalId="modal-advanced" label="ADVANCED" />
  <ModalButton modalId="modal-syntax" label="SYNTAX" />
  <ModalButton modalId="modal-examples" label="EXAMPLES" />
  {#if output}
    <div class="toast">
      <div class="alert alert-info bg-primary">
        <div>
          <span class="font-mono">OUTPUT: {output}</span>
        </div>
      </div>
    </div>
  {/if}

  <Modal modalId="modal-advanced" title="ADVANCED SEARCH">
    <p class="pt-2 text-xs text-neutral">• Please note that some field may override others (CRN, Course ID, etc.)</p>
    <p class="pb-2 text-xs text-neutral">• Fields with an <code>*</code> must be combined with at least 1 other field.</p>
    <AdvancedSearch />
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
      <p>Find courses in the MACS department that match the Cultural Studies: Western GenEd:</p>
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

<style>
.no-scrollbar {
  scrollbar-width: none !important;
  -ms-overflow-style: none !important; /* IE and Edge */
}
.no-scrollbar::-webkit-scrollbar {
  display: none !important;
}
</style>
