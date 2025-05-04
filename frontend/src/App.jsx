import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [list, setList] = useState([])

  useEffect(() => {
    const fetchList = async () => {
      const response = await fetch('http://localhost:8000/leaderboard')
      const data = await response.json()

      setList(data.leaderboard)
    }

    fetchList()
  }, [])

  const captureVideo = async () => {
    await fetch('http://localhost:8000/camera')
  }

  const stopCapture = async () => {
    await fetch("http://localhost:8000/stop")
  }

  return (
    <>
      <ul>
        {list && list.map((attendee) => (
          <li key={attendee._id}>{attendee.name}</li>
        ))}
      </ul>

      <button onClick={captureVideo}>Start Scanning</button>
      <button onClick={stopCapture}>Stop Scanning</button>
    </>
  )
}

export default App
