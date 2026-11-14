import { useState } from "react";

function ReseumeUI() {
  const [file, setFile] = useState(null);
  const [load, setLoad] = useState(false);
  const [result, setResult] = useState(null);

 const handleUpload = async() => {
    if (!file) {
        alert("Please select a file first!");
        return;
    }
    setLoad(true);  

    const formData = new FormData();
    formData.append("file",file);

    try{
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            body: formData,
        });

        const res = await response.json();
        console.log("File uploaded successfully:", res);
        setResult(res);
        setLoad(false); 
    }
    catch(error){
        console.error("Error uploading file:", error);
    }
    finally{
        setLoad(false); 
    }
 }
    return (
    <div >
      <h1 className= 'heading'>Resume Analyzer-Gen0
      </h1>

      {/* File Upload Section   */}


        <div className='upload-section'>
        <h1>Check Your Resume Quality</h1>
        <h1>By Using this Analyzer! </h1>

        <input id='org-file-input' type="file"  style={{display:"none"}}
            onChange={(e) => setFile(e.target.files[0])}>
        </input>
        &nbsp; &nbsp;
        <button className='file-input' onClick={()=> document.getElementById('org-file-input').click()}>Choose File</button>
        
        <button className='upload-btn' onClick={handleUpload} disabled={load}>
            {load ? "Uploading..." : "Upload"}
        </button>
        <p id='display-select'>{file ? `Selected file: ${file.name}` : "No file selected"}</p>

        </div>

        {/* Analysis Result */}
        {result && (
         <div id='result-section'>
            <h2>Analysis Result:</h2>
        <p>prediction Role: {result.prediction_Role}</p>
        <p>Confidence: {result.Confidence}</p>
        <p>Detected Skills: {result.Detected_Skills}</p>
        <p>Suggestions: {result.Suggestions}</p>
        </div>)}
    </div>
    
  );
}
export default ReseumeUI