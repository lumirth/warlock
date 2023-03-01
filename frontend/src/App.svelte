<script>
  let message = "";

  function callBackend() {
    fetch("http://localhost:8000/")
      .then(response => response.json())
      .then(data => {
        message = data.message;
      })
      .catch(error => {
        console.error(error);
      });
  }
</script>

<button on:click={callBackend}>Call Backend API</button>
<p>{message}</p>