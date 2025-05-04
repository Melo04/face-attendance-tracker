import { useState, useEffect } from 'react'
import './App.css'

function Leaderboard() {
  const [list, setList] = useState([])

  useEffect(() => {
    const fetchList = async () => {
      const response = await fetch('http://localhost:8000/leaderboard')
      const data = await response.json()

      setList(data.leaderboard)
    }

    fetchList()
  }, [])

  return (
    <>
      <ul>
        {list && list.map((attendee) => (
          <li key={attendee._id}>{attendee.name}</li>
        ))}
      </ul>
    </>
  )
}

export default Leaderboard
