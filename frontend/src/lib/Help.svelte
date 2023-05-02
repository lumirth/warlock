<div class="prose text-sm pt-2 select-text cursor-text">
  <p>
    To search, simply type a department name (with or without a course number),
    or a gened. For example, "comp sci" or "adv comp".
  </p>
  <p>You can also combine search terms using commas. For example:</p>
  <ul>
    <li>
      <code>"comp sci, adv comp"</code> will return all courses in the CS
      department that satisfy the advanced composition gened.
    </li>
      <li>

        <code>"cs, machine learning"</code> will return all courses in the CS
        department that have the key phrase "machine learning" in their title or
        description.
      </li>
  </ul>
  <p>
    You can also specify a term, year, or CRN:
  </p>
  <ul>
    <li>
      <code>"macs, western, fall"</code> will return all courses in the MACS
      department that satisfy the cultural studies - western gened and are offered in
      the fall.
    </li> 
    <li>
      <code>"phil, nonwestern, 2021"</code> will return all courses in the PHIL
      department that satisfy the cultural studies - nonwestern gened and are offered in (fall) 
      2021.
    </li>
    <li>
        <code>"74331"</code> will return the single course with a section matching the CRN.
    </li>
  </ul>
  <p>
    Note that if you don't specify either a year or a term, each will default to the most recent
    valid value. For example, during the latter spring semester, searching "macs, western, 2021"
    will return courses offered in the <i>fall</i> of 2021. 
  </p>
  <div class="text-lg font-bold text-gray-200" >TIPS</div>
  <ul>
    <li><code>"hrs:X"</code> can be used to specify an amount of credit hours</li>
    <li><code>"pot:X"</code> can be used to specify a part of term (A, B, full)</li>
    <!-- TODO: make sure this is implemented in the backend -->
    <li><code>"CS 3"</code> you can get a specific level of courses (300, 200, etc)</li>
  </ul>
  <br/>

<div class="collapse collapse-arrow">
    <input type="checkbox" />
    <div class="collapse-title text-lg font-bold bg-base-200">
        ADVANCED QUERIES
    </div>
    <div class="collapse-content">
        <p>
            If you're okay with a little more complexity, you can use the search box to get more specific results.
        </p>
          <p>
            The search box takes a comma-separated list of arguments. It will attempt to
            intelligently match your input for the following:
          </p>
          <ul>
            <li>
              Subject/course codes (<code>CS 225; macs356; mathematics</code>)
            </li>
            <li>
              GenEds (<code>adv comp; humanities & the arts; life sciences</code>)
            </li>
          </ul>
          <p>You can also input the following:</p>
          <ul>
            <li>CRNs (<code>12345; 54321</code>)</li>
            <li>Years (<code>2022; 2004</code>)</li>
            <li>
              Terms (<code>fall; spring; summer; winter; fa; sp; su; wi</code>)
            </li>
          </ul>
          <p>Most notably, you can declare search parameters explicitly:</p>
          <ul>
            <li>Subject/department (<code>subj:CS; d:MATH; dept: CPSC</code>)</li>
            <li>Course ID (<code>course:225; id: 107</code>)</li>
            <li>Year (<code>yr:2009; year:2011</code>)</li>
            <li>Term (<code>term:fall; t:sp</code>)</li>
            <li>CRN (<code>crn:12345</code>)</li>
            <li>Credit hours (<code>hrs:3; hr: 1</code>)</li>
            <!-- TODO: give a full list of gen ed codes-->
            <li>GenEd (<code>gen:ADVCOMP; g:HUM</code>)</li>
            <li>
              Part of Term (<code>pot:first; p: whole; part-of-term:all</code>)
            </li>
            <li>
              Keyword (<code>q: minds and machines; keyword: advanced applications</code
              >)
            </li>
          </ul>
          <p>
            Here are some further examples with the MACS department:
          </p>
          <ul>
            <li><code>macs, western</code></li>
            <li><code>media and cinema studies, cultural studies western</code></li>
            <li>Specifically at the 300 level: <code>MACS 3, g:west</code></li>
            <li>Worth 3 credit hours: <code>MACS, g:west, hrs:3</code></li>
            <li>Online: <code>MACS, western, is:online</code></li>
            <li>First eight weeks: <code>macs, western, pot:a</code></li>
          </ul>
        </div>
    </div>
</div>

