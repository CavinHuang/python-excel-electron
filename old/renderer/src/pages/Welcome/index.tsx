import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { Button } from "antd";
import axios from "axios";

import * as Styled from "./style";

const Welcome = () => {
  const [result, setResult] = useState<string>("");
  const navigate = useNavigate();

  const handleClick = async () => {
    const res = await axios.get("http://localhost:1134/hello");
    console.log("res", res);
    setResult(res.data)
  };
  const handleJump = async () => {
    navigate("/dashboard")
  };

  return (
    <Styled.Container>
      <Styled.Text>Welcome</Styled.Text>
      <Button onClick={handleJump} style={{ display: 'none' }}>Jump</Button>
      <Button onClick={handleClick}>request py</Button>
      <p>result:{result}</p>
    </Styled.Container>
  );
};

export default Welcome;
