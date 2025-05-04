import { useState, useEffect } from 'react'
import './App.css'
import {
  Box,
  Heading,
  List,
  ListItem,
  Text,
  VStack,
  Spinner,
} from '@chakra-ui/react';


function App() {
  // const [list, setList] = useState([])
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/attendance')
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setAttendance(data.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching attendance:', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    console.log('attendance', attendance);
  }, []);

  // useEffect(() => {
  //   const fetchList = async () => {
  //     const response = await fetch('http://localhost:8000/leaderboard')
  //     const data = await response.json()

  //     setList(data.leaderboard)
  //   }

  //   fetchList()
  // }, [])

  const captureVideo = async () => {
    await fetch('http://localhost:8000/camera')
  }

  const stopCapture = async () => {
    await fetch("http://localhost:8000/stop")
  }

  return (
    <>
        <div style={{ padding: '1rem' }}>
            <h1>Attendance Records</h1>
            {attendance.map((record, index) => (
                <div key={index} style={{ border: '1px solid black', marginBottom: '1rem', padding: '1rem' }}>
                    <h3>Date: {new Date(record.date).toLocaleDateString()}</h3>
                    <ul>
                        {record.attendees.map((name, idx) => (
                            <li key={idx}>{name}</li>
                        ))}
                    </ul>
                </div>
            ))}

            <button onClick={captureVideo}>Start Scanning</button>
            <button onClick={stopCapture}>Stop Scanning</button>
        </div>
    </>
  )
}

export default App
