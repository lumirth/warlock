<script>
  import Header from './Header.svelte';
  import "../app.css";
</script>

<div class="app">
  <Header />

  <!-- responsive for different screen sizes -->
  <main class="container mx-auto px-4 md:px-10 lg:px-20 xl:px-40">
    <slot />
  </main>
  <footer class="footer footer-center p-4 text-base-content mt-5 md:mt-10 lg:mt-20 xl:mt-30">
    <div class="flex gap-4">
      <div class="uppercase">Copyright © 2023</div>
      <!-- <a href="https://github.com" role="button" class="btn cursor-pointer rounded-full btn-xs">GITHUB</a> -->
    </div>
  </footer>
</div>

<style>

</style>
