import React, { useState } from 'react'
import { Button } from "./components/ui/button"
import { Input } from "./components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card"

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [result, setResult] = useState<any | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [res, setRes] = useState<any>({});
  const handleClick = async () => {
    const resFetch = await fetch("http://localhost:1134/hello");
    const res = await resFetch.json();
    setRes(res)
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/process_excel', {
        method: 'POST',
        // body: formData,
      });
      const data = await response.json();
      console.log('🚀 ~ handleSubmit ~ data:', data)
      setResult(data);
    } catch (error) {
      console.error('Error processing file:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Excel Processor</CardTitle>
        </CardHeader>
        <CardContent>
          <Input type="file" onChange={handleFileChange} className="mb-4" />
          <Button onClick={handleSubmit}>Process Excel</Button>
          {result && (
            <div className="mt-4">
              <h2 className="text-lg font-semibold">Results:</h2>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
          <Button onClick={handleClick}>request py</Button>
          <p>result:{res && res.text}</p>
        </CardContent>
      </Card>
    </div>
  );
}