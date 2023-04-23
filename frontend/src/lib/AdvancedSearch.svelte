<script lang="ts">
  import Dropdown from "./Dropdown.svelte";
  import TextInput from "./TextInput.svelte";
  import NumberInput from "./NumberInput.svelte";
  import Checkbox from "./Checkbox.svelte";

  // Replace the following arrays with the appropriate data
  const yearOptions = [
    { value: "2023", text: "2023" },
    { value: "2022", text: "2022" },
  ];

  const semesterOptions = [
    { value: "spring", text: "Spring" },
    { value: "fall", text: "Fall" },
  ];

  const keywordTypeOptions = [
    { value: "type1", text: "Type 1" },
    { value: "type2", text: "Type 2" },
  ];

  const collegeOptions = [
    { value: "college1", text: "College 1" },
    { value: "college2", text: "College 2" },
  ];

  const subjectOptions = [
    { value: "subject1", text: "Subject 1" },
    { value: "subject2", text: "Subject 2" },
  ];

  const sectionAttributesOptions = [
    { value: "attribute1", text: "Attribute 1" },
    { value: "attribute2", text: "Attribute 2" },
  ];

  const courseLevelOptions = [
    { value: "level1", text: "Level 1" },
    { value: "level2", text: "Level 2" },
  ];

  const genedReqsOptions = [
    { value: "req1", text: "Requirement 1" },
    { value: "req2", text: "Requirement 2" },
  ];

  const partOfTermOptions = [
    { value: "part1", text: "Part 1" },
    { value: "part2", text: "Part 2" },
  ];

  // Define selected value variables for each dropdown
  let selectedYear: string;
  let selectedSemester: string;
  let selectedKeywordType: string;
  let selectedCollege: string;
  let selectedSubject: string;
  let selectedSectionAttributes: string;
  let selectedCourseLevel: string;
  let selectedGenedReqs1: string;
  let selectedGenedReqs2: string;
  let selectedGenedReqs3: string;
  let selectedPartOfTerm: string;

  let keywordValue: string;
  let instructorValue: string;
  let courseIdValue: number;
  let crnValue: number;
  let creditHoursValue: number;
  let matchAllGenedReqs: boolean;
  let matchAnyGenedReqs: boolean;
  let online: boolean;
  let openSections: boolean;
  let evenings: boolean;
</script>

<form class="space-y-4">
  <Dropdown id="year" label="Year" options="{yearOptions}" selectedValue="{selectedYear}" />
  <Dropdown id="semester" label="Semester" options="{semesterOptions}" selectedValue="{selectedSemester}" />
  <TextInput id="keyword" label="Keyword" value={keywordValue}/>
  <Dropdown id="keywordType" label="Keyword Type" options="{keywordTypeOptions}" selectedValue="{selectedKeywordType}" />
  <TextInput id="instructor" label="Instructor" value={instructorValue}/>
  <Dropdown id="college" label="College" options="{collegeOptions}" selectedValue="{selectedCollege}" />
  <Dropdown id="subject" label="Subject" options="{subjectOptions}" selectedValue="{selectedSubject}" />
  <NumberInput id="courseId" label="Course ID" value={courseIdValue}/>
  <NumberInput id="crn" label="CRN" value={crnValue}/>
  <NumberInput id="creditHours" label="Credit Hours" value={creditHoursValue}/>
  <Dropdown id="sectionAttributes" label="Section Attributes" options="{sectionAttributesOptions}" selectedValue="{selectedSectionAttributes}" />
  <Dropdown id="courseLevel" label="Course Level" options="{courseLevelOptions}" selectedValue="{selectedCourseLevel}" />
  <Dropdown id="genedReqs1" label="GenEd Requirement 1" options="{genedReqsOptions}" selectedValue="{selectedGenedReqs1}" />
  <Dropdown id="genedReqs2" label="GenEd Requirement 2" options="{genedReqsOptions}" selectedValue="{selectedGenedReqs2}" />
  <Dropdown id="genedReqs3" label="GenEd Requirement 3" options="{genedReqsOptions}" selectedValue="{selectedGenedReqs3}" />
  <Checkbox id="matchAllGenedReqs" label="Match all GenEd requirements" checked={matchAllGenedReqs}/>
  <Checkbox id="matchAnyGenedReqs" label="Match any GenEd requirements" checked={matchAnyGenedReqs}/>
  <Dropdown id="partOfTerm" label="Part of Term" options="{partOfTermOptions}" selectedValue="{selectedPartOfTerm}" />
  <Checkbox id="online" label="Online" checked={online}/>
  <Checkbox id="onCampus" label="On Campus" checked={!online}/>
  <Checkbox id="openSections" label="Open Sections" checked={openSections}/>
  <Checkbox id="evenings" label="Evenings" checked={evenings}/>
  <button type="submit" class="btn bg-base-200 font-normal text-lg">
    SEARCH
  </button>
</form>