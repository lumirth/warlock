# Course Warlock

This is a streamlined and modified version of the original project proposal. It keeps the spirit of the original proposal while making it less verbose and easier to understand.

## Introduction

Students have a confusing amount of options for getting information about their courses, including Enhanced Registration, Classic Registration, GPA++, Waf’s Gen Ed by GPA visualizations, RateMyProfessor, Coursicle, and likely more than a few  more. 

Course Warlock aims to solve this—when a course *explorer* won't do, look to a course *warlock*. Course Warlock aims to be a comprehensive tool for streamlining the process of selecting and obtaining information about courses. Data is consolidated from various sources, such as RateMyProfessor ratings, historic GPA data, and the University's courses API, allowing students to make informed decisions about whether a course is worth taking.

## Functionality

### Essential Features

- **View courses:** Allow students to view courses by various filters, such as semester, subject, and CRN.
- **Search courses:** Enable searching for courses by name, professor name, department, and other criteria.
- **View course details:** Display detailed information for each course, including descriptions, schedules, and requirements.
- **View GPA data:** Present historic GPA data for courses, helping students assess course difficulty.
  - Match a course with its own historic GPA data, even when the data lags behind current course information.
  - Display GPA data for specific semesters when looking at older course offerings.
- **View RateMyProfessor ratings:** Integrate RateMyProfessor ratings for courses, providing insights into professor quality and course experiences.
  - Address potential challenges in obtaining RMP data, such as the lack of a clean public-facing developer API, by considering options like periodic scraping or live scraping with a modular frontend component.

### Nice-to-have Features

- **App-specific course rating system:** Implement a simple, app-specific rating system (e.g., a star-based system) to complement or replace RMP data.
  - Consider challenges related to implementing a login system, such as the potential for bot abuse with anonymous ratings.
  - Explore options like restricting ratings by IP address to mitigate potential issues.

## Components

### Frontend

- **TypeScript:** Utilize TypeScript, a strict superset of JavaScript developed by Microsoft, to improve development speed and efficiency through type safety and better error detection.
- **Svelte/SvelteKit:** Adopt the Svelte/SvelteKit frontend framework, developed by Vercel, for its simplicity, ease of use, and potential to accelerate development by offering straightforward templating and component systems.

### Backend

- **Python (with Django):** Consider Python with Django for its relatively low barrier of entry and user-friendly syntax.
- **Rust (with Actix):** Evaluate Rust with Actix as an alternative due to its mandatory error handling, high performance, and excellent toolchain.
- **SvelteKit (as a full-stack framework):** Assess the feasibility of using SvelteKit as a full-stack framework that employs Svelte for UI components, offering an all-in-one solution for both frontend and backend development.

## Data Handling

- **API reliance:** Whenever possible, rely on APIs for data retrieval to minimize storage requirements and costs.
- **Data storage:** Store data only if necessary to provide a better user experience (UX) and overcome potential API limitations or issues.
- **User authentication:** Avoid implementing user login or authentication systems, as they can be complex and introduce security risks.

## Testing

- **Unit test library selection:** Choose a unit test library based on the backend language selected, focusing on testing the most critical components.
- **Style guides:** Follow appropriate style guides for each language, such as PEP8 for Python, Google's style guide for TypeScript, and the official style guide for Rust.
- **Code reviews:** Use GitHub branches and commenting systems to review significant feature changes and ensure the maintainability and stability of the codebase.

## Weekly Planning Schedule

1. **Week 1: Set up project structure and establish development workflow.**
   - Configure development environment, including Docker for standardization and portability.
   - Set up version control using Git and GitHub, including the creation of branches, issue tracking, and project organization.

2. **Week 2: Integrate course API for course information and professor information.**
   - Connect to University's course API.
   - Retrieve relevant course and professor data.
   - Design data structures for storing and processing retrieved data.

3. **Week 3: Integrate datasets to allow for GPA component. Integrate with courses.**
   - Acquire and process historic GPA datasets.
   - Associate GPA data with relevant courses.
   - Ensure compatibility and consistency between GPA data and course API data.

4. **Week 4: Develop refined barebones UI, with standardized styling. Wire up with backend.**
   - Create UI components for displaying course information, GPA data, and professor information.
   - Implement standardized styling across the application.
   - Connect frontend UI components to backend APIs.

5. **Week 5: Integrate RMP data/API. Show alongside course information.**
   - Obtain RateMyProfessor data through scraping or APIs.
   - Match RMP data with corresponding courses and professors.
   - Display RMP data alongside course information in the UI.

6. **Week 6: Refine UI. Add better searching options for courses and professors.**
   - Enhance search functionality with advanced filters and sorting options.
   - Improve the UI's responsiveness and overall user experience.
   - Implement any necessary UI optimizations and refinements.

7. **Week 7: Test pre-existing content. Attempt "put in your requirements, get best courses" option.**
   - Conduct thorough testing of the application's functionality and UI.
   - Develop a feature for recommending courses based on user-inputted requirements.
   - Evaluate the performance and effectiveness of the recommendation system.

8. **Week 8: Implement basic feedback system. Finalize user interface and refine existing frontend and backend code.**
   - Create a system for users to provide feedback on courses and professors.
   - Finalize the application's UI design and implement any last-minute refinements.
   - Optimize frontend and backend code for performance and maintainability.

## Risks

- **Data accuracy and currency:** The data from external APIs may not be accurate, current, or reliable, which can impact the project's UX.
- **API limitations:** The APIs used may have restrictions on the amount of data that can be obtained or how the data can be used.
- **Data storage:** Storing data may conflict with the goal of minimizing costs, but it could be necessary if external APIs prove to be problematic.
- **Ongoing maintenance:** Course Warlock will require regular updates to ensure accuracy and up-to-date information, which may become challenging after graduation.
  - Possible solutions include automating updates or passing on maintenance responsibilities to someone else.
- **Data integration:** Integrating data from multiple sources can be technically challenging and may require significant effort to ensure compatibility and consistency.

- ## Teamwork

  - **Development environment:** Utilize Docker to standardize the development environment and minimize "it works on my machine" errors. This ensures portability and consistency between operating systems, which is crucial for a project of this scale.

  - **Team roles and responsibilities:** Although the team has decided against a strictly defined division of tasks, members will initially be assigned tasks based on their experience levels to maximize efficiency and productivity.
    - Lukas: Frontend (TypeScript, Svelte)
    - Parth, Bangyan, and Tiancheng: Backend (C++, Python, Rust)
    - The team will remain open to learning and experimenting with different technologies, allowing members to explore areas outside their primary expertise.

  - **Collaboration tools:** The team will use Discord for communication and real-time collaboration. GitHub's Projects and Issues features will be employed to organize tasks, track progress, and ensure that all team members are aware of the work that needs to be done.

  - **Learning and growth:** By fostering an environment that encourages exploration and learning, the team will provide opportunities for members to develop new skills and gain experience with various technologies. This approach will help maintain motivation and engagement throughout the project.

  - **Code quality:** The focus will be on producing high-quality code that adheres to best practices and is easily maintainable. Emphasis will be placed on understanding and utilizing the most effective tools, frameworks, and libraries for each aspect of the project.
