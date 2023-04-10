<script>
  import Navbar from './lib/Navbar.svelte';
  import SearchForm from './lib/SearchForm.svelte';
  import Footer from './lib/Footer.svelte';

  let message = "";

  function callBackend() {
    fetch("http://localhost:8000/")
      .then(response => response.json())
      .then(data => {
        message = data.msg;
      })
      .catch(error => {
        console.error(error);
      });
  }

</script>

<Navbar />
<SearchForm />
<Footer />
<button on:click={callBackend}>Call Backend API</button>
<p>{message}</p>

<style>
  /* Add any necessary global styles */
</style>