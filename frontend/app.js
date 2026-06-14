document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('guidance-form');
    const formSection = document.getElementById('guidance-form-section');
    const loadingState = document.getElementById('loading-state');
    const resultsSection = document.getElementById('results-section');
    const resetBtn = document.getElementById('reset-btn');

    // API URL - modify this depending on where your FastAPI server runs
    const API_URL = 'http://127.0.0.1:8000/api/guidance';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get values
        const fsc_group = document.getElementById('fsc_group').value;
        const fsc_marks = document.getElementById('fsc_marks').value;
        const city = document.getElementById('city').value;
        const interests = document.getElementById('interests').value;

        const profile = {
            fsc_group,
            fsc_marks,
            city,
            interests
        };

        // UI Transitions
        formSection.classList.add('hidden');
        loadingState.classList.remove('hidden');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(profile)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch guidance');
            }

            const data = await response.json();
            
            // Populate Results
            populateResults(data);

            // UI Transitions
            loadingState.classList.add('hidden');
            resultsSection.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating your roadmap. Please check your backend server and API keys.');
            // Reset UI
            loadingState.classList.add('hidden');
            formSection.classList.remove('hidden');
        }
    });

    resetBtn.addEventListener('click', () => {
        resultsSection.classList.add('hidden');
        form.reset();
        formSection.classList.remove('hidden');
        // scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    function populateResults(data) {
        // Summary
        document.getElementById('res-summary').innerText = data.roadmap_summary || 'Analysis complete.';

        // Career Paths
        const careersContainer = document.getElementById('res-careers');
        careersContainer.innerHTML = '';
        if (data.career_paths && data.career_paths.length > 0) {
            data.career_paths.forEach(path => {
                const tags = path.skills_required.map(skill => `<span class="tag">${skill}</span>`).join('');
                careersContainer.innerHTML += `
                    <div class="result-card">
                        <h4>${path.title}</h4>
                        <p>${path.description}</p>
                        <div class="tag-list">${tags}</div>
                    </div>
                `;
            });
        } else {
            careersContainer.innerHTML = '<p>No specific career paths found.</p>';
        }

        // Universities
        const unisContainer = document.getElementById('res-universities');
        unisContainer.innerHTML = '';
        if (data.universities && data.universities.length > 0) {
            data.universities.forEach(uni => {
                const programs = uni.programs.map(prog => `<span class="tag">${prog}</span>`).join('');
                unisContainer.innerHTML += `
                    <div class="result-card">
                        <h4>${uni.name}</h4>
                        <p><strong>Fee:</strong> ${uni.estimated_fee}<br><strong>Merit Info:</strong> ${uni.merit_info}</p>
                        <div class="tag-list">${programs}</div>
                    </div>
                `;
            });
        } else {
            unisContainer.innerHTML = '<p>No specific universities found.</p>';
        }

        // Scholarships
        const scholContainer = document.getElementById('res-scholarships');
        scholContainer.innerHTML = '';
        if (data.scholarships && data.scholarships.length > 0) {
            data.scholarships.forEach(schol => {
                const linkStr = schol.link ? `<a href="${schol.link}" target="_blank" class="link-btn">Learn More &rarr;</a>` : '';
                scholContainer.innerHTML += `
                    <div class="result-card">
                        <h4>${schol.name}</h4>
                        <p>${schol.description}</p>
                        <p><small><strong>Eligibility:</strong> ${schol.eligibility}</small></p>
                        ${linkStr}
                    </div>
                `;
            });
        } else {
            scholContainer.innerHTML = '<p>No specific scholarships found.</p>';
        }

        // Free Courses
        const coursesContainer = document.getElementById('res-courses');
        coursesContainer.innerHTML = '';
        if (data.free_courses && data.free_courses.length > 0) {
            data.free_courses.forEach(course => {
                const linkStr = course.link ? `<a href="${course.link}" target="_blank" class="link-btn">Go to Course &rarr;</a>` : '';
                coursesContainer.innerHTML += `
                    <div class="result-card">
                        <h4>${course.title}</h4>
                        <p><strong>Platform:</strong> ${course.platform}</p>
                        ${linkStr}
                    </div>
                `;
            });
        } else {
            coursesContainer.innerHTML = '<p>No specific courses found.</p>';
        }
    }
});
