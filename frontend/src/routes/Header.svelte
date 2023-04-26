<script>
	import { page } from '$app/stores';
	import warlock from '$lib/images/warlock.svg';
</script>

<header class="mb-10 md:mb-20 lg:mb-32 xl:mb-40 ">
	<nav class="h-16 border-b border-neutral bg-base-200 w-auto justify-between">
    <div class="navbar w-auto justify-between">
      <div class="flex space-x-0">
        <a href="/" class="flex items-center">
          <span class="btn btn-ghost normal-case text-xl">
            <img src="{warlock}" alt="Warlock logo" class="h-9 w-9 mr-1 ml-[-9px]">
            <div class="flex flex-col text-left gap-0 leading-5">
              <span class="block">COURSE</span>
              <span class="block">WARLOCK</span>
            </div>
          </span>
        </a>
      </div>
      <div class="flex-none">
          <a class="btn font-normal text-lg border-none bg-transparent" href="/about">ABOUT</a>
      </div>
    </div>
</header>

<style>
	img {
		fill: currentColor;
	}
</style>
