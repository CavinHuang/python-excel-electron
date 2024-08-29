import * as React from "react";
import { Routes, Route, HashRouter } from "react-router-dom";

import WelcomePage from "./Welcome";
import { DashboardPage } from "./Dashboard/Loadable";
import { ListPage } from './Dashboard/List/Loadable';
import { UserPage } from './Dashboard/User/Loadable';

import { GlobalStyle } from "../styles/global-styles";

function App() {
  return (
    <>
      <HashRouter>
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="dashboard" element={<DashboardPage />}>
            <Route path="user" element={<UserPage />} />
            <Route index element={<div>欢迎使用控制台1234567</div>} />
            <Route path="list">
            <Route index element={<ListPage />} />
            <Route path="page1" element={<div>列表页面1</div>} />
            <Route path="page2" element={<ListPage />} />
            <Route path="page3" element={<div>列表页面3</div>} />
          </Route>
          </Route>
        </Routes>
      </HashRouter>
      <GlobalStyle />
    </>
  );
}

export default App;
