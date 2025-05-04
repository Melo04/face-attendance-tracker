import { useState, useEffect } from 'react'
import './App.css'

function AddUser() {
  const [name, setName] = useState("")
  const [file, setFile] = useState(null)

    const handleFileChange = (e) => {
      setFile(e.target.files[0]);
    };

  const formSubmit = async () => {
    if (!file || !name) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);

    console.log(name)
    console.log(file)

    try {
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
    } catch (err) {
      console.error('Error uploading file:', err);
    }
  }

  return (
      <>
      <form onSubmit={formSubmit}>
        <div style={{marginBottom: 30, display: "flex", flexDirection: "column", justifyContent: "left", alignItems: "left", gap: 5}}>
          <div style={{fontSize: 20}}>Name</div>
          <input type="text" onChange={(e) => setName(e)} />
        </div>

        <div style={{marginBottom: 25, display: "flex", flexDirection: "column", justifyContent: "left", alignItems: "left"}}>
          <div style={{fontSize: 20}}>upload a picture: </div>
          <input type="file" accept="image/png, image/jpeg" onChange={(e) => handleFileChange(e)} />
        </div>

        <button type="submit">Submit</button>
      </form>
    </>
  )
}

export default AddUser
