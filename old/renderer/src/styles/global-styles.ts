import { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
  html,
  body {
    height: 100%;
    width: 100%;
    font-size: 14px!important;
    font-weight: 400!important;
    background-color: #FAFAFA!important;
    color: #838383!important;
  }

  body {
    font-family: "PingFang SC","Microsoft YaHei",Arial,sans-serif!important;
  }

  #app {
    min-height: 100%;
    min-width: 1197px;
  }
  body,
  dl,
  dd,
  h1,
  h2,
  h3,
  h4,
  h5,
  h6,
  p,
  ol, li, ul
  form {
    margin: 0;
  }
  ol, li, ul {
    margin: 0;
    padding: 0;
  }
  input,
  button {
    outline: none;
    font-family: 'PingFangSC-Light','Roboto', 'Microsoft YaHei', Arial,  sans-serif !important;
  }
  hr {
    display: none;
  }
  li {
    list-style:none;
    outline: none;
  }
  input,textarea {
    caret-color: #1890ff;
    font-family: 'PingFangSC-Light','Roboto', 'Microsoft YaHei', Arial,  sans-serif !important;
  }
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button{
      margin: 0;
  }
  .icon {
    width: 1em;
    height: 1em;
    fill: currentColor;
    display: block;
    margin-right: 14px;
  }
  .clip-iconfont {
    width: 1em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
  }
`;
