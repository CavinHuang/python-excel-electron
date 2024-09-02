import React,{ useRef,useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card,CardContent,CardHeader,CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RadioGroup,RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Loader2, Upload } from "lucide-react";

import {SSE} from 'sse.js'
import { Switch } from '../ui/switch';

enum FileType {
  SEA_RAIL = "SEA_RAIL",
  AIR_TRANSPORT = "AIR_TRANSPORT",
}

const fileTypes = [
  { label: "海铁",value: FileType.SEA_RAIL },
  { label: "空运",value: FileType.AIR_TRANSPORT },
]
let sse: SSE | null = null
const ExcelProcessor = () => {
  const [file,setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [logs,setLogs] = useState<string[]>([]);
  const [fileType,setFileType] = useState<FileType>(FileType.SEA_RAIL);
  const [isProcessing,setIsProcessing] = useState<boolean>(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [isPrice,setIsPrice] = useState<boolean>(false);
  const [isFetchImg,setIsFetchImg] = useState<boolean>(false);

  const handleSse = () => {
    if(sse) {
      sse.close()
      sse = null
    }
    sse = new SSE('http://localhost:1134/logs')

    sse.stream()

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    sse.addEventListener('message', (e: any)=>{
      console.log(e)
      const message = e.data
      if (message.includes('complate:')) {
        sse?.close()
        setIsProcessing(false)
      }
      addLog(e.data)
    })

  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      addLog(`已选择文件: ${selectedFile.name}`);
    }
  };

  const handleTriggerFile = () => {
    fileInputRef.current?.click();
  };

  const handleFileTypeChange = (fileType: FileType) => {
    setFileType(fileType);
  }

  const handleProcessFile = () => {
    setLogs([])
    if (!file) {
      addLog("请先选择一个Excel文件");
      return;
    }
    if (!fileType) {
      addLog("请选择文件类型（海铁或空运）");
      return;
    }
    setIsProcessing(true)
    addLog(`开始处理${fileType}Excel文件...`);
    handleSse()

    // 上传文件
    const formData = new FormData()
    formData.append('file', file)
    formData.append('fileType', fileType)
    formData.append('isPrice', isPrice ? '1' : '0')
    formData.append('isFetchImg', isFetchImg ? '1' : '0')
    fetch('http://localhost:1134/add_task', {
      method: 'POST',
      // headers: {
      //   'Content-Type': 'multipart/form-data'
      // },
      body: formData
    })
  };

  const addLog = (message: string) => {
    setLogs(prevLogs => [...prevLogs,`${new Date().toLocaleTimeString()} - ${message}`]);
    // 滚动到最底部
    scrollAreaRef.current?.scrollTo({
      top: scrollAreaRef.current.scrollHeight,
      behavior: 'smooth'
    })
  };

  return (
    <div className="p-4 w-full">
      <Card>
        <CardHeader>
          <CardTitle>Excel文件处理工具</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-10">
            <div className='flex items-center space-x-4'>
              <Label className="w-24">开启价格获取</Label>
              <Switch checked={isPrice} onCheckedChange={setIsPrice} />
            </div>

            <div className='flex items-center space-x-4'>
              <Label className="w-24">开启图片获取</Label>
              <Switch checked={isFetchImg} onCheckedChange={setIsFetchImg} />
            </div>

            <div className="flex items-center space-x-4">
              <Label className="w-24">文件类型：</Label>
              <RadioGroup className='flex gap-5' defaultValue={fileType} onValueChange={handleFileTypeChange}>
                {
                  fileTypes.map((item) => (
                    <div className="flex items-center space-x-2" key={`file-type-${item.value}`}>
                      <RadioGroupItem value={item.value} id={item.value} />
                      <Label htmlFor={item.value}>{item.label}</Label>
                    </div>
                  ))
                }
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
                  ref={fileInputRef}
                />
                <label htmlFor="file-upload">
                  <Button className="w-96" onClick={handleTriggerFile}>
                    <Upload className="mr-2 h-4 w-4" />
                    {file ? file.name : "选择Excel文件"}
                  </Button>
                </label>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="w-24"></div>
              <Button onClick={handleProcessFile} disabled={!file || !fileType || isProcessing} className="flex-1">
                {isProcessing ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : fileType ? `处理${fileType}文件` : "处理文件"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="mt-10">
        <CardHeader>
          <CardTitle>处理日志</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-[400px] w-full rounded-md border p-4" ref={scrollAreaRef}>
            {logs.map((log,index) => (
              <div key={index} className="mb-1">{log}</div>
            ))}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
};

export default ExcelProcessor;