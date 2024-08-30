import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Upload } from "lucide-react";

const ExcelProcessor = () => {
  const [file, setFile] = useState<File | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [fileType, setFileType] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      addLog(`已选择文件: ${selectedFile.name}`);
    }
  };

  const handleFileTypeChange = (value: string) => {
    setFileType(value);
    addLog(`已选择文件类型: ${value}`);
  };

  const handleProcessFile = () => {
    if (!file) {
      addLog("请先选择一个Excel文件");
      return;
    }
    if (!fileType) {
      addLog("请选择文件类型（海铁或空运）");
      return;
    }
    addLog(`开始处理${fileType}Excel文件...`);
    // 这里添加处理Excel文件的逻辑，根据fileType区分处理方式
    setTimeout(() => {
      addLog(`${fileType}Excel文件处理完成`);
    }, 2000);
  };

  const addLog = (message: string) => {
    setLogs(prevLogs => [...prevLogs, `${new Date().toLocaleTimeString()} - ${message}`]);
  };

  return (
    <div className="p-4 w-full">
      <Card>
        <CardHeader>
          <CardTitle>Excel文件处理工具</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <Label className="w-24">文件类型：</Label>
              <RadioGroup defaultValue="comfortable">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="default" id="r1" />
                  <Label htmlFor="r1">Default</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="comfortable" id="r2" />
                  <Label htmlFor="r2">Comfortable</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="compact" id="r3" />
                  <Label htmlFor="r3">Compact</Label>
                </div>
              </RadioGroup>
            </div>
            <div className="flex items-center space-x-4">
              <Label htmlFor="file-upload" className="w-24">选择文件：</Label>
              <div className="flex-1">
                <input
                  type="file"
                  accept=".xlsx, .xls"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload">
                  <Button className="w-full">
                    <Upload className="mr-2 h-4 w-4" />
                    {file ? file.name : "选择Excel文件"}
                  </Button>
                </label>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="w-24"></div>
              <Button onClick={handleProcessFile} disabled={!file || !fileType} className="flex-1">
                {fileType ? `处理${fileType}文件` : "处理文件"}
              </Button>
            </div>
          </div>

          <Card className="mt-4">
            <CardHeader>
              <CardTitle>处理日志</CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[200px] w-full rounded-md border p-4">
                {logs.map((log, index) => (
                  <div key={index} className="mb-1">{log}</div>
                ))}
              </ScrollArea>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </div>
  );
};

export default ExcelProcessor;