import { useState } from 'react'
import './App.css'

function App() {
  const [jobDesc, setJobDesc] = useState("")
  const [jdFile, setJdFile] = useState(null)
  const [resumes, setResumes] = useState([])
  const [results, setResults] = useState([])

  const submit = async () => {
    const formData = new FormData()

    resumes.forEach((file) => {
      formData.append("resumes", file)
    })

    if (jdFile) {
      formData.append("jd_file", jdFile)
    }

    formData.append("job_description", jobDesc)

    const res = await fetch("http://localhost:8000/rank-resumes-files", {
      method: "POST",
      body: formData
    })

    const data = await res.json()
    setResults(data)
  }

  return (
    <>
      <section id="center">
        <h1>Resume Ranking System</h1>
        <p>Upload resumes and job description</p>
      </section>

      <section id="input-section">
        <h2>Job Description</h2>

        <textarea
          placeholder="Enter JD (optional)"
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
        />

        <input
          type="file"
          onChange={(e) => setJdFile(e.target.files[0])}
        />

        <h2>Upload Resumes</h2>

        <input
          type="file"
          multiple
          onChange={(e) => setResumes([...e.target.files])}
        />

        <button onClick={submit}>Analyse Resumes</button>
      </section>

      <section id="results">
        <h2>Ranked Candidates</h2>

        {results.map((r) => (
          <div key={r.rank} className="card">
            <h3>Rank {r.rank}</h3>
            <p><b>Name:</b> {r.name}</p>
            <p><b>Score:</b> {r.score}</p>

            <details>
              <summary>View Details</summary>

              <p><b>Skills:</b> {r.details.skills.join(", ")}</p>

              <p><b>Matched Skills:</b> {r.details.matched_skills.join(", ")}</p>

              <p><b>Missing Skills:</b> {r.details.missing_skills.join(", ")}</p>

              <p>{r.details.explanation}</p>
            </details>
          </div>
        ))}
      </section>
    </>
  )
}

export default App