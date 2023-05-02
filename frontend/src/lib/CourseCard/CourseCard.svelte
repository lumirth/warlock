<script lang="ts">
  import CourseCardHeader from "./CourseCardHeader.svelte";
  import CourseCardContent from "./CourseCardContent.svelte";
  import CourseCardFooter from "./CourseCardFooter.svelte";
  import CourseCardSections from "./CourseCardSections.svelte";

  export let course: any;
  let course_id: string = course.id;
  let sem_code: string =
    course.term[0] + course.term[1] + course.year[2] + course.year[3];
  let tags_text = course.genEdAttributes
    ? course.genEdAttributes.map((genEd: any) => {
        if (genEd.id[0] == "1") {
          return genEd.id.slice(1);
        } else {
          return genEd.id;
        }
      })
    : [];
</script>

<div class="mb-4">
  <div class="bg-base-200 border-neutral border-[1px] flex flex-col">
    <CourseCardHeader
      {course_id}
      course_detail={course.label}
      href={course.href}
    />
    <div class="border-t border-neutral w-full mx-auto" />
    <CourseCardContent description={course.description} />
    <!-- show if either tags_text has a length or if gpa_average isnt 0-->
    <!-- {#if tags_text.length > 0 || average_gpa != 0} -->
    <div class="border-t border-neutral w-full mx-auto" />
    <CourseCardFooter
      credit_hours={course.creditHours}
      {sem_code}
      average_gpa={course.gpa_average ? course.gpa_average : 0}
      {tags_text}
    />
    <!-- {/if} -->
  </div>
  <CourseCardSections
    sections={course.sections}
    year={course.year}
    term={course.term}
    course_id={course.id}
  />
</div>
