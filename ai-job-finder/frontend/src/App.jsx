import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const res = await fetch(
        "https://manoj-ai-job-finder-ejeac4d3e7avacdz.centralindia-01.azurewebsites.net/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            message: message
          })
        }
      );

      const data = await res.json();

      console.log("API RESPONSE:", data);

      setJobs(
        Array.isArray(data.reply)
          ? data.reply
          : []
      );

    } catch (error) {
      console.error(error);
      alert("Unable to fetch jobs");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">

      <div className="header">
        <h1>AI Job Finder</h1>
        <p>
          Search jobs using natural language
        </p>
      </div>

      <div className="search-bar">

        <input
          type="text"
          placeholder="e.g. Python Developer Bangalore"
          value={message}
          onChange={(e) =>
            setMessage(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          className="send-btn"
          onClick={sendMessage}
        >
          Search
        </button>

      </div>

      {loading && (
        <div className="loading">
          Searching jobs...
        </div>
      )}

      {!loading && jobs.length > 0 && (
      <div style={{ textAlign: "left", marginBottom: "8px" }}>
        <div className="results-count">
          Found {jobs.length} jobs
        </div>
      </div>
      )}

      {jobs.map((job, index) => (

      <div
        key={index}
        className="job-card"
      >

        <div className="job-content">

          <h3>{job.role}</h3>

          <div className="job-meta">
            <span>🏢 {job.company}</span>
            <span>📍 {job.location}</span>
          </div>

        </div>

        <a
          href={job.url}
          target="_blank"
          rel="noreferrer"
          className="apply-btn"
        >
          Apply
        </a>

      </div>

      ))}

    </div>
  );
}

export default App;
