import styled from "styled-components";

export const Container = styled.div`
  position: relative;
  color: white;
  height: 100vh;
  background: linear-gradient(
    200.96deg,
    #fedc2a -29.09%,
    #dd5789 51.77%,
    #7a2c9e 129.35%
  );
  font-family: sans-serif;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

export const Content = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
`;

export const Text = styled.div`
  background-image: linear-gradient(#ffcf02, #ff7352);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  font-size: 64px;
`;
