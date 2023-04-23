<script lang="ts">
  import Dropdown from "./Dropdown.svelte";
  import TextInput from "./TextInput.svelte";
  import NumberInput from "./NumberInput.svelte";
  import Checkbox from "./Checkbox.svelte";

  // Replace the following arrays with the appropriate data
  const yearOptions = [
    { value: "2023", text: "2023" },
    { value: "2022", text: "2022" },
    { value: "2021", text: "2021" },
    { value: "2020", text: "2020" },
    { value: "2019", text: "2019" },
    { value: "2018", text: "2018" },
    { value: "2017", text: "2017" },
    { value: "2016", text: "2016" },
    { value: "2015", text: "2015" },
    { value: "2014", text: "2014" },
    { value: "2013", text: "2013" },
    { value: "2012", text: "2012" },
    { value: "2011", text: "2011" },
    { value: "2010", text: "2010" },
    { value: "2009", text: "2009" },
    { value: "2008", text: "2008" },
    { value: "2007", text: "2007" },
    { value: "2006", text: "2006" },
    { value: "2005", text: "2005" },
    { value: "2004", text: "2004" },
  ];

  const semesterOptions = [
    { value: "spring", text: "Spring" },
    { value: "fall", text: "Fall" },
    { value: "summer", text: "Summer" },
    { value: "winter", text: "Winter" },
  ];

  const keywordTypeOptions = [
    { value: "default", text: "Default" },
    { value: "exact phrase", text: "Exact Phrase" },
    { value: "any of these words", text: "Any Words" },
    { value: "all of these words", text: "All Words" },
  ];

  const collegeOptions = [
    {
      value: "ACES",
      text: "Agricultural, Consumer and Environmental Sciences",
    },
    { value: "AHS", text: "Applied Health Sciences" },
    { value: "AFROTC", text: "Armed Forces" },
    { value: "CARLE", text: "Carle Illinois College of Medicine" },
    { value: "MEDIA", text: "College of Media" },
    { value: "DGS", text: "Division of General Studies" },
    { value: "EDUC", text: "Education" },
    { value: "FAA", text: "Fine and Applied Arts" },
    { value: "BUS", text: "Gies College of Business" },
    { value: "GRAD", text: "Graduate College" },
    { value: "ENG", text: "Grainger College of Engineering" },
    { value: "LAW", text: "Law" },
    { value: "LAS", text: "Liberal Arts and Sciences" },
    { value: "iSchool", text: "School of Information Sciences" },
    { value: "LER", text: "School of Labor and Employee Relations" },
    { value: "SSW", text: "School of Social Work" },
    { value: "VETMED", text: "Veterinary Medicine" },
  ];

  const subjectOptions = [
    { value: "AAS", text: "Asian American Studies" },
    { value: "ABE", text: "Agricultural and Biological Engineering" },
    { value: "ACCY", text: "Accountancy" },
    { value: "ACE", text: "Agricultural and Consumer Economics" },
    { value: "ACES", text: "Agricultural, Consumer and Environmental Sciences" },
    { value: "ADV", text: "Advertising" },
    { value: "AE", text: "Aerospace Engineering" },
    { value: "AFAS", text: "Air Force Aerospace Studies" },
    { value: "AFRO", text: "African American Studies" },
    { value: "AFST", text: "African Studies" },
    { value: "AGCM", text: "Agricultural Communications" },
    { value: "AGED", text: "Agricultural Education" },
    { value: "AGLL", text: "Agricultural Leadership and Science Education" },
    { value: "AGRO", text: "Agroecology and Sustainable Food Systems" },
    { value: "AHS", text: "Applied Health Sciences" },
    { value: "AIS", text: "American Indian Studies" },
    { value: "ANSC", text: "Animal Sciences" },
    { value: "ANTH", text: "Anthropology" },
    { value: "ARAB", text: "Arabic" },
    { value: "ARCH", text: "Architecture" },
    { value: "ART", text: "Art" },
    { value: "ARTD", text: "Art and Design" },
    { value: "ARTF", text: "Art Foundations" },
    { value: "ARTS", text: "Art and Art History" },
    { value: "ASRM", text: "Actuarial Science and Risk Management" },
    { value: "ASTR", text: "Astronomy" },
    { value: "ATMS", text: "Atmospheric Sciences" },
    { value: "BADM", text: "Business Administration" },
    { value: "BASQ", text: "Basque" },
    { value: "BCOG", text: "Brain and Cognitive Science" },
    { value: "BCS", text: "Bosnian-Croatian-Serbian" },
    { value: "BIOC", text: "Biochemistry" },
    { value: "BIOE", text: "Bioengineering" },
    { value: "BIOL", text: "Biology" },
    { value: "BIOP", text: "Biophysics" },
    { value: "BSE", text: "Biomedical Sciences and Engineering" },
    { value: "BTW", text: "Business and Technical Writing" },
    { value: "BULG", text: "Bulgarian" },
    { value: "BUS", text: "Business" },
    { value: "C&I", text: "Curriculum and Instruction" },
    { value: "CEE", text: "Civil and Environmental Engineering" },
    { value: "CFS", text: "Child and Family Studies" },
    { value: "CHBE", text: "Chemical and Biomolecular Engineering" },
    { value: "CHEM", text: "Chemistry" },
    { value: "CHIN", text: "Chinese" },
    { value: "CHLH", text: "Community Health" },
    { value: "CHP", text: "Campus Honors Program" },
    { value: "CI", text: "Curriculum and Instruction" },
    { value: "CINE", text: "Cinema Studies" },
    { value: "CITL", text: "Center for Innovation in Teaching and Learning" },
    { value: "CLCV", text: "Classical Civilization" },
    { value: "CMN", text: "Communication" },
    { value: "CPSC", text: "Crop Sciences" },
    { value: "CS", text: "Computer Science" },
    { value: "CSE", text: "Computer Science and Engineering" },
    { value: "CW", text: "Creative Writing" },
    { value: "CWL", text: "Comparative and World Literature" },
    { value: "CZCH", text: "Czech" },
    { value: "DANC", text: "Dance" },
    { value: "DTX", text: "Human-Centered Design and Design Thinking" },
    { value: "EALC", text: "East Asian Languages and Cultures" },
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

  const genedReqsOptions = [
    { value: "COMP1", text: "Composition I" },
    { value: "1CLL", text: "Advanced Composition" },
    { value: "HUM", text: "Humanities and the Arts" },
    { value: "1LA", text: "Humanities and the Arts: Literature & the Arts" },
    {
      value: "1HP",
      text: "Humanities and the Arts: Historical & Philosophical Perspectives",
    },
    { value: "1LS", text: "Natural Sciences and Technology: Life Science" },
    { value: "1PS", text: "Natural Sciences and Technology: Physical Science" },
    { value: "1QR1", text: "Quantitative Reasoning I" },
    { value: "1QR2", text: "Quantitative Reasoning II" },
    { value: "1SS", text: "Social Science" },
    { value: "1BSC", text: "Behavioral Science" },
    { value: "CS", text: "Cultural Studies" },
    { value: "1WCC", text: "Western/Comparative Cultures" },
    { value: "1NW", text: "Non-Western Cultures" },
    { value: "1US", text: "US Minority Cultures" },
  ];

  const partOfTermOptions = [
    { value: "fullterm", text: "Full Term" },
    { value: "first8weeks", text: "First 8 Weeks" },
    { value: "last8weeks", text: "Last 8 Weeks" },
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
