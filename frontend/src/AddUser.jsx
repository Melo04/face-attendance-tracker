import React, { useState, useEffect, useRef } from 'react'
import './App.css'
import Webcam from 'react-webcam'
import { Stack, HStack } from '@chakra-ui/react'

const videoConstraints = {
  width: 540,
  facingMode: "environment"
};

function AddUser() {
  const webcamRef = useRef(null);
  const [url, setUrl] = React.useState(null);

  const capturePhoto = React.useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setUrl(imageSrc);
  }, [webcamRef]);

  const onUserMedia = (e) => {
    console.log(e);
  };

  const [name, setName] = useState("");
  const [file, setFile] = useState(null);

  const formSubmit = async (e) => {
    e.preventDefault();
    if (!url || !name) return;

    const base64Response = await fetch(url);
    const blob = await base64Response.blob();

    const formData = new FormData();
    formData.append('file', blob, 'photo.jpg');
    formData.append('name', name);

    console.log('name', name);
    console.log(url);

    const response = await fetch('http://localhost:8000/user', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      alert(`File uploaded: ${data.filename}`);
    } else {
      alert('Upload failed.');
    }
  }

  return (
    <>
      <Stack gap="4" align="flex-start">
        <Webcam
          ref={webcamRef}
          audio={true}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          onUserMedia={onUserMedia}
        />

        {url && (
          <div>
            <img src={url} alt="Screenshot" />
          </div>
        )}
        <HStack>
          <button onClick={capturePhoto}>Capture</button>
          <button onClick={() => setUrl(null)}>Refresh</button>
        </HStack>
      </Stack>
      <form onSubmit={formSubmit}>
        <div style={{ marginBottom: 30, display: "flex", flexDirection: "column", justifyContent: "left", alignItems: "left", gap: 5 }}>
          <div style={{ fontSize: 20 }}>Name</div>
          <input type="text" onChange={(e) => setName(e.target.value)} />
        </div>
        <button type="submit">Register</button>
      </form>
    </>
  )
}

export default AddUser
