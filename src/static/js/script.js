document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('select-button').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const department = document.getElementById('department-select').value;

    if (!department) {
      alert("Please select a Department.");
      return;
    }

    let batch = '2020';
    let csvFileName = `${department.replace(/\s/g, '')}.csv`;
    let filePath = `./Student Marks/${batch}/${csvFileName}`;

    fetch(filePath)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to fetch file: ${response.status} - ${response.statusText}`);
        }
        return response.text();
      })
      .then(csvData => {
        const students = parseCSV(csvData);
        const seniorAvg = calculateAverage(students);
        document.getElementById('seniors-average').textContent = `Average Marks: ${seniorAvg}`;

        batch = '2021';
        csvFileName = `${department.replace(/\s/g, '')}.csv`;
        filePath = `./Student Marks/${batch}/${csvFileName}`;

        fetch(filePath)
          .then(response => {
            if (!response.ok) {
              throw new Error(`Failed to fetch file: ${response.status} - ${response.statusText}`);
            }
            return response.text();
          })
          .then(csvData => {
            const students2 = parseCSV(csvData);
            const juniorAvg = calculateAverage(students2);
            document.getElementById('juniors-average').textContent = `Average Marks: ${juniorAvg}`;
            const students = [...students, ...students2];
            displayStudents(students);
          })
          .catch(error => {
            console.error("Error:", error);
            document.getElementById('studentDataDisplay').innerHTML = `<p>Error loading data. Please check the file path: "${filePath}"</p>`;
          });
      });

    document.getElementById('calculate-average-btn').addEventListener('click', function () {
      const internal1 = parseFloat(document.getElementById('internal1-input').value);
      const internal2 = parseFloat(document.getElementById('internal2-input').value);
      const internal3 = parseFloat(document.getElementById('internal3-input').value);

      if (isNaN(internal1) || isNaN(internal2) || isNaN(internal3)) {
        alert("Please enter valid numbers for all Internal marks.");
        return;
      }

      const average = (internal1 + internal2 + internal3) / 3;
      document.getElementById('average-result').textContent = `Average: ${average.toFixed(2)}`;
    });
  });

  function calculateAverage(students) {
    if (students.length === 0) return 'N/A';

    let sumInternal1 = 0;
    let sumInternal2 = 0;
    let sumInternal3 = 0;

    for (const student of students) {
      sumInternal1 += parseFloat(student['Internal 1'] || 0);
      sumInternal2 += parseFloat(student['Internal 2'] || 0);
      sumInternal3 += parseFloat(student['Internal 3'] || 0);
    }

    const count = students.length;
    const avgInternal1 = sumInternal1 / count;
    const avgInternal2 = sumInternal2 / count;
    const avgInternal3 = sumInternal3 / count;

    if (isNaN(avgInternal1) || isNaN(avgInternal2) || isNaN(avgInternal3)) {
      return 'N/A';
    }

    return ((avgInternal1 + avgInternal2 + avgInternal3) / 3).toFixed(2);
  }

  function parseCSV(csvText) {
    const lines = csvText.trim().split('\n'); // Split by new line
    if (lines.length === 0) return [];

    const headers = lines[0].split(',').map(header => header.trim()); // Get headers and trim

    const students = [];
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(value => value.trim()); // Get values and trim
      const student = {};
      for (let j = 0; j < headers.length; j++) {
        student[headers[j]] = values[j];
      }
      students.push(student);
    }
    return students;
  }

  function displayStudents(students) {
    const displayDiv = document.getElementById('studentDataDisplay');
    if (students.length === 0) {
      displayDiv.innerHTML = '<p>No data to display.</p>';
    } else {
      let html = '<table class="table table-bordered">';
      html += '<thead><tr>';
      for (const key in students[0]) {
        html += `<th>${key}</th>`;
      }
      html += '</tr></thead><tbody>';

      for (const student of students) {
        html += '<tr>';
        for (const key in student) {
          html += `<td>${student[key]}</td>`;
        }
        html += '</tr>';
      }

      html += '</tbody></table>';
      displayDiv.innerHTML = html;
    }
  }
});
