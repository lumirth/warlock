<script lang="ts">
  import Dropdown from "./Dropdown.svelte";
  import TextInput from "./TextInput.svelte";
  import NumberInput from "./NumberInput.svelte";
  import Checkbox from "./Checkbox.svelte";

  import yearsJson from "../data/years.json";
  import termsJson from "../data/terms.json";
  import collegesJson from "../data/colleges.json";
  import subjectsJson from "../data/subjects.json";
  import genEdsJson from "../data/gen_eds.json";
  import potsJson from "../data/pots.json";

  // Create arrays using imported JSON data
  const yearOptions = Object.entries(yearsJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));
  const semesterOptions = Object.entries(termsJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));
  const collegeOptions = Object.entries(collegesJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));
  const subjectOptions = Object.entries(subjectsJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));
  const genedReqsOptions = Object.entries(genEdsJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));
  const partOfTermOptions = Object.entries(potsJson).map(([text, value]) => ({
    text,
    value: String(value),
  }));

  // Define selected value variables for each dropdown
  let selectedYear: string;
  let selectedSemester: string;
  let selectedCollege: string;
  let selectedSubject: string;
  let selectedGenedReqs1: string;
  let selectedGenedReqs2: string;
  let selectedGenedReqs3: string;
  let selectedPartOfTerm: string;
  let selectedKeywordType: string;
  let selectedCourseLevel: string;

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
    { value: "level1", text: "100 Level" },
    { value: "level2", text: "200 Level" },
    { value: "level3", text: "300 Level" },
    { value: "level4", text: "400 Level" },
    { value: "level5", text: "500 Level" },
  ];

  let keywordValue: string;
  let instructorValue: string;
  let courseIdValue: number;
  let crnValue: number;
  let creditHoursValue: number;
  let matchAllGenedReqs: boolean;
  let matchAnyGenedReqs: boolean;
  let online: boolean;
  let onCampus: boolean;
  let openSections: boolean;
  let evenings: boolean;
</script>

<form class="space-y-4">
  <Dropdown
    id="year"
    label="Year"
    options={yearOptions}
    selectedValue={selectedYear}
  />
  <Dropdown
    id="semester"
    label="Semester"
    options={semesterOptions}
    selectedValue={selectedSemester}
  />
  <TextInput id="keyword" label="Keyword" value={keywordValue} />
  <Dropdown
    id="keywordType"
    label="Keyword Type"
    options={keywordTypeOptions}
    selectedValue={selectedKeywordType}
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
  <button type="submit" class="btn bg-base-200 font-normal text-lg">
    SEARCH
  </button>
</form>
