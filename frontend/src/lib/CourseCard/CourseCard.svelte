<script lang="ts">
    import CourseCardHeader from "./CourseCardHeader.svelte";
    import CourseCardContent from "./CourseCardContent.svelte";
    import CourseCardFooter from "./CourseCardFooter.svelte";
    import CourseCardSections from "./CourseCardSections.svelte";
    // Define type for props
    export let href: string = "https://example.com";
    export let course_id: string = "CS 222";
    export let course_detail: string = "Software Programming Lab";
    export let sem_code: string = "SP23";
    export let credit_hours: string = "1";
    export let description: string =
      "Design and implementation of novel software solutions. Problem identification and definition; idea generation and evaluation; and software implementation, testing, and deployment. Emphasizes software development best practices—including framework selection, code review, documentation, appropriate library usage, project management, continuous integration and testing, and teamwork. Prerequisite: CS 128; credit or concurrent registration in CS 225. Restricted to majors in Computer Science undergraduate curricula only.";
    export let average_gpa: number = 3.1;
    export let tags_text: Array<string> = ["MIN", "HUM"];
  </script>
  
  <div class="bg-base-200 border-neutral border-[1px] flex flex-col mb-6">
    <CourseCardHeader
      {course_id}
      {course_detail}
      {href}
    />
    <div class="border-t border-neutral w-full mx-auto"></div>
    <CourseCardContent
      {description}
      />
    <!-- show if either tags_text has a length or if gpa_average isnt 0-->
    <!-- {#if tags_text.length > 0 || average_gpa != 0} -->
      <div class="border-t border-neutral w-full mx-auto"></div>
      <CourseCardFooter
      {credit_hours}
      {sem_code}
      {average_gpa}
      {tags_text}
      />
      <!-- {/if} -->
  </div>
  <!-- <CourseCardSections/> -->