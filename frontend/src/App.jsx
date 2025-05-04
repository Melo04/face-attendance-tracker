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
        setAttendance(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching attendance:', err);
        setLoading(false);
      });
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
      <Box p={6}>
        <Heading size="lg" mb={6}>Attendance Records</Heading>
        <VStack spacing={6} align="stretch">
          {attendance.map((record, index) => (
            <Box
              key={index}
              borderWidth="1px"
              borderRadius="lg"
              p={5}
              shadow="md"
            >
              <Heading size="md">
                Date: {new Date(record.date).toLocaleDateString()}
              </Heading>
              <List spacing={2} mt={3}>
                {record.attendees.map((name, idx) => (
                  <ListItem key={idx} pl={2}>
                    <Text>- {name}</Text>
                  </ListItem>
                ))}
              </List>
            </Box>
          ))}
        </VStack>
      </Box>

      <button onClick={captureVideo}>Start Scanning</button>
      <button onClick={stopCapture}>Stop Scanning</button>
    </>
  )
}

export default App
