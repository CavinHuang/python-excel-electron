import React, { useRef, useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Loader2, Upload } from "lucide-react";

import { SSE } from 'sse.js'
import { Switch } from '../ui/switch';

import { List as VirtualizedList, AutoSizer, CellMeasurer, CellMeasurerCache } from 'react-virtualized';

enum FileType {
  SEA_RAIL = "SEA_RAIL",
  AIR_TRANSPORT = "AIR_TRANSPORT",
}

const fileTypes = [
  { label: "海铁", value: FileType.SEA_RAIL },
  { label: "空运", value: FileType.AIR_TRANSPORT },
]

let sse: SSE | null = null

const viewHeight = 500

const ExcelProcessor = () => {
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [fileType, setFileType] = useState<FileType>(FileType.SEA_RAIL);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [isPrice, setIsPrice] = useState<boolean>(false);
  const [isFetchImg, setIsFetchImg] = useState<boolean>(false);

  const cache = useRef(new CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 100,
  }));

  useEffect(() => {
    return () => {
      if (sse) {
        sse.close();
      }
    };
  }, []);

  const handleSse = () => {
    if (sse) {
      sse.close();
      sse = null;
    }
    cache.current.clearAll();
    sse = new SSE('http://localhost:1134/logs');

    sse.onmessage = (e) => {
      const message = e.data;
      if (message.includes('complate:')) {
        sse?.close();
        setIsProcessing(false);
      }
      addLog(message);
    };

    sse.onerror = () => {
      console.error('SSE连接错误');
      setIsProcessing(false);
    };

    sse.stream();
  };

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
  };

  const handleProcessFile = () => {
    setLogs([]);
    if (!file) {
      addLog("请先选择一个Excel文件");
      return;
    }
    if (!fileType) {
      addLog("请选择文件类型（海铁或空运）");
      return;
    }
    setIsProcessing(true);
    addLog(`开始处理${fileType}Excel文件...`);
    handleSse();

    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileType', fileType);
    formData.append('isPrice', isPrice ? '1' : '0');
    formData.append('isFetchImg', isFetchImg ? '1' : '0');
    fetch('http://localhost:1134/add_task', {
      method: 'POST',
      body: formData
    }).catch(error => {
      console.error('上传文件错误:', error);
      setIsProcessing(false);
      addLog('上传文件失败，请重试');
    });
  };

  const addLog = (message: string) => {
    setLogs(prevLogs => [...prevLogs, `${new Date().toLocaleTimeString()} - ${message}`]);
  };

  const listRef = useRef<VirtualizedList>(null);


  const onRowsRendered = () => {
    // const { startIndex, stopIndex } = data;
    // if (
    //     scrollIndex !== -1 &&
    //     (scrollIndex >= startIndex || scrollIndex <= stopIndex)
    // ) {
    //     setScrollIndex(-1);
    //   }
    listRef.current?.scrollToRow(logs.length - 1);
    setTimeout(() => {
      listRef.current?.scrollToRow(logs.length - 1);
    }, 100);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const renderRow = ({ index, key, parent, style }: { index: number; key: string; parent: any; style: React.CSSProperties }) => {
    const itemData = logs[index];
    return (
      <CellMeasurer
        cache={cache.current}
        columnIndex={0}
        key={key}
        parent={parent}
        rowIndex={index}
      >
        {({ measure }: { measure: () => void }) => (
          <div style={style} className='p-2' onLoad={measure}>
            <div className="mb-1">{itemData}</div>
          </div>
        )}
      </CellMeasurer>
    );
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
        <CardContent className='h-[500px]'>
          <AutoSizer>
            {({ width }: { width: number; height: number }) => (
              <VirtualizedList
                width={width}
                height={viewHeight}
                rowHeight={cache.current.rowHeight}
                rowCount={logs.length}
                rowRenderer={renderRow}
                deferredMeasurementCache={cache.current}
                overscanRowCount={5}
                onRowsRendered={onRowsRendered}
                ref={listRef}
              />
            )}
          </AutoSizer>
        </CardContent>
      </Card>
    </div>
  );
};

export default ExcelProcessor;