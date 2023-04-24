<script lang="ts">
  import Dropdown from "./Dropdown.svelte";
  import TextInput from "./TextInput.svelte";
  import NumberInput from "./NumberInput.svelte";
  import Checkbox from "./Checkbox.svelte";

  import yearsJson from "../data/years.json";
  // TODO: add conditional semester dropdown that shows the correct semesters for the selected year
  // import termsJson from "../data/terms.json";
  import collegesJson from "../data/colleges.json";
  import subjectsJson from "../data/subjects_display.json";
  import genEdsJson from "../data/gen_eds_display.json";
  import potsJson from "../data/pots.json";

  // Create arrays using imported JSON data, sorted alphabetically
  const collegeOptions = Object.entries(collegesJson)
    .sort()
    .map(([text, value]) => ({
      text,
      value: String(value),
    }));
  const subjectOptions = Object.entries(subjectsJson)
    .sort()
    .map(([text, value]) => ({
      text,
      value: String(value),
    }));
  const genedReqsOptions = Object.entries(genEdsJson)
    .sort()
    .map(([text, value]) => ({
      text,
      value: String(value),
    }));
  const partOfTermOptions = Object.entries(potsJson)
    .sort()
    .map(([text, value]) => ({
      text,
      value: String(value),
    }));
  // years is different because it is an array of numbers. make sure to reverse sort
  const yearOptions = yearsJson
    .sort()
    .reverse()
    .map((year) => ({
      value: String(year),
      text: String(year),
    }));
  // semester is different because it is pre-defined
  const semesterOptions = [
    { value: "fall", text: "Fall" },
    { value: "spring", text: "Spring" },
    { value: "summer", text: "Summer" },
    { value: "winter", text: "Winter" },
  ];

  // Create additional options arrays (not using JSON files)
  const keywordTypeOptions = [
    { value: "default", text: "Default" },
    { value: "exact phrase", text: "Exact Phrase" },
    { value: "any of these words", text: "Any Words" },
    { value: "all of these words", text: "All Words" },
  ];

  const sectionAttributesOptions = [
    { value: "attribute1", text: "Attribute 1" },
    { value: "attribute2", text: "Attribute 2" },
  ];

  const courseLevelOptions = [
    { value: "1", text: "100 Level" },
    { value: "2", text: "200 Level" },
    { value: "3", text: "300 Level" },
    { value: "4", text: "400 Level" },
    { value: "5", text: "500 Level" },
    { value: "6", text: "600 Level" },
  ];

  const defaultYear = yearOptions[0].value;
  const defaultSemester = semesterOptions[0].value;
  const defaultKeywordType = keywordTypeOptions[0].value;
  // Define selected value variables for each dropdown
  let selectedYear: string = defaultYear;
  let selectedSemester: string = defaultSemester;
  let selectedCollege: string;
  let selectedSubject: string;
  let selectedGenedReqs1: string;
  let selectedGenedReqs2: string;
  let selectedGenedReqs3: string;
  let selectedPartOfTerm: string;
  let selectedKeywordType: string = defaultKeywordType;
  let selectedCourseLevel: string;

  let keywordValue: string;
  let instructorValue: string;
  let courseIdValue: number;
  let crnValue: number;
  let creditHoursValue: number;
  let matchAllGenedReqs: boolean = true;
  let matchAnyGenedReqs: boolean = false;
  let online: boolean;
  let onCampus: boolean;
  let openSections: boolean;
  let evenings: boolean;

  let error_message: string = "";

  function handleSubmit(event: Event): void {
    // if only year and semester are selected, then do not submit
    if (
      selectedYear === defaultYear &&
      selectedSemester === defaultSemester &&
      !selectedCollege &&
      !selectedSubject &&
      !selectedGenedReqs1 &&
      !selectedGenedReqs2 &&
      !selectedGenedReqs3 &&
      !selectedPartOfTerm &&
      !keywordValue &&
      !instructorValue &&
      !courseIdValue &&
      !crnValue &&
      !creditHoursValue &&
      !selectedCourseLevel &&
      !online &&
      !onCampus &&
      !openSections &&
      !evenings
    ) {
      event.preventDefault();
      error_message = "Please give at least one search option.";
    } else {
      error_message = "";
    }

    // gen eds is a list of non-empty values
    // no genedReqs if all are empty
    let genedReqs =
      selectedGenedReqs1 || selectedGenedReqs2 || selectedGenedReqs3
        ? [selectedGenedReqs1, selectedGenedReqs2, selectedGenedReqs3].filter(
            Boolean
          )
        : null;
    // no keyword type if keyword is empty
    let keywordType = keywordValue ? selectedKeywordType : null;
    // no matchAllGenedReqs if genedReqs is empty
    // no matchAnyGenedReqs if genedReqs is empty
    let matchAllGenedReqsValue = genedReqs ? matchAllGenedReqs : null;
    let matchAnyGenedReqsValue = genedReqs ? matchAnyGenedReqs : null;
    let AdvancedSearchAllVals = {
      year: selectedYear,
      semester: selectedSemester,
      keyword: keywordValue,
      keywordType: keywordType,
      instructor: instructorValue,
      courseId: courseIdValue,
      crn: crnValue,
      creditHours: creditHoursValue,
      college: selectedCollege,
      subject: selectedSubject,
      partOfTerm: selectedPartOfTerm,
      genedReqs: genedReqs,
      matchAllGenedReqs: matchAllGenedReqsValue,
      matchAnyGenedReqs: matchAnyGenedReqsValue,
      online: online,
      onCampus: onCampus,
      openSections: openSections,
      evenings: evenings,
      courseLevel: selectedCourseLevel,
    };
    // filter out empty values
    let AdvancedSearchFiltered = Object.fromEntries(
      Object.entries(AdvancedSearchAllVals).filter(([_, v]) => v != null)
    );

    console.log(AdvancedSearchFiltered);
  }
</script>

<form class="space-y-4" on:submit={handleSubmit}>
  <Dropdown
    id="year"
    label="Year"
    options={yearOptions}
    selectedValue={selectedYear}
    addEmptyOption={false}
  />
  <Dropdown
    id="semester"
    label="Semester"
    options={semesterOptions}
    selectedValue={selectedSemester}
    addEmptyOption={false}
  />
  <TextInput id="keyword" label="Keyword" value={keywordValue} />
  <Dropdown
    id="keywordType"
    label="Keyword Type"
    options={keywordTypeOptions}
    selectedValue={selectedKeywordType}
    addEmptyOption={false}
  />
  <TextInput id="instructor" label="Instructor" value={instructorValue} />
  <Dropdown
    id="college"
    label="College"
    options={collegeOptions}
    selectedValue={selectedCollege}
  />
  <Dropdown
    id="subject"
    label="Subject"
    options={subjectOptions}
    selectedValue={selectedSubject}
  />
  <NumberInput id="courseId" label="Course ID" value={courseIdValue} />
  <NumberInput id="crn" label="CRN" value={crnValue} />
  <NumberInput id="creditHours" label="Credit Hours" value={creditHoursValue} />
  <!-- TODO: add section attributes back. this would require adding maintenance
  scripts to fetch attributes. the query parameter for it is not documented. it
  is degreeAtt -->
  <!-- <Dropdown
    id="sectionAttributes"
    label="Section Attributes"
    options={sectionAttributesOptions}
    selectedValue={selectedSectionAttributes}
  /> -->
  <Dropdown
    id="courseLevel"
    label="Course Level"
    options={courseLevelOptions}
    selectedValue={selectedCourseLevel}
  />
  <Dropdown
    id="genedReqs1"
    label="GenEd Requirement 1"
    options={genedReqsOptions}
    selectedValue={selectedGenedReqs1}
  />
  <Dropdown
    id="genedReqs2"
    label="GenEd Requirement 2"
    options={genedReqsOptions}
    selectedValue={selectedGenedReqs2}
  />
  <Dropdown
    id="genedReqs3"
    label="GenEd Requirement 3"
    options={genedReqsOptions}
    selectedValue={selectedGenedReqs3}
  />
  <Checkbox
    id="matchAllGenedReqs"
    label="Match all GenEd requirements"
    checked={matchAllGenedReqs}
  />
  <Checkbox
    id="matchAnyGenedReqs"
    label="Match any GenEd requirements"
    checked={matchAnyGenedReqs}
  />
  <Dropdown
    id="partOfTerm"
    label="Part of Term"
    options={partOfTermOptions}
    selectedValue={selectedPartOfTerm}
  />
  <Checkbox id="online" label="Online" checked={online} />
  <Checkbox id="onCampus" label="On Campus" checked={onCampus} />
  <Checkbox id="openSections" label="Open Sections" checked={openSections} />
  <Checkbox id="evenings" label="Evenings" checked={evenings} />
  <div class="flex flex-row gap-4">
    <button type="submit" class="btn bg-base-200 font-normal text-lg">
      SEARCH
    </button>
    {#if error_message}
    <div class="text-red-500">{error_message}</div>
    {/if}
  </div>
</form>
