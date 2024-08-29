/**
 * Dashboard
 */
 import { useNavigate, Outlet } from 'react-router-dom';
 import { memo, useState } from 'react';
 import { ProLayout } from '@ant-design/pro-components';
 import {
   SmileOutlined,
   UserOutlined,
   TabletOutlined,
   MenuUnfoldOutlined,
   MenuFoldOutlined,
   CrownOutlined,
 } from '@ant-design/icons';
 
 import icon from '../../assets/react.svg';
 
 export const Dashboard = memo(() => {
   const navigate = useNavigate();
   const [pathname, setPathname] = useState('/');
   const [collapsed, setCollapsed] = useState(true);
 
   const renderLogo = () => <img src={icon} alt="logo" />;
 
   return (
     <div style={{ height: '100vh' }}>
       <ProLayout
         title="我的应用"
         logo={renderLogo()}
         navTheme="light"
         location={{ pathname }}
         collapsed={collapsed}
         onCollapse={setCollapsed}
         fixSiderbar
         collapsedButtonRender={false}
         menuRender={(item, dom) => (
           <div
             onClick={() => {
               console.log('menuRender', item);
             }}
           >
             {dom}
           </div>
         )}
         menuItemRender={(item, dom) => (
           <div
             onClick={() => {
               console.log('menuItemRender', item);
               setPathname(item.path || '/dashboard');
               navigate(`/dashboard${item.path}`);
             }}
           >
             {dom}
           </div>
         )}
         headerContentRender={() => {
           return (
             <div
               onClick={() => setCollapsed(!collapsed)}
               style={{
                 cursor: 'pointer',
                 fontSize: '16px',
               }}
             >
               {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
             </div>
           );
         }}
         route={{
           routes: [
             {
               path: '/',
               name: '欢迎',
               icon: <SmileOutlined />,
             },
             {
               path: '/user',
               name: '用户',
               icon: <UserOutlined />,
             },
             {
               path: '/list',
               name: '列表',
               icon: <TabletOutlined />,
               routes: [
                 {
                   path: '/list/page1',
                   name: '一级页面',
                   hideInMenu: true,
                   icon: <CrownOutlined />,
                 },
                 {
                   path: '/list/page2',
                   name: '二级页面',
                   icon: <CrownOutlined />,
                 },
                 {
                   path: '/list/page3',
                   name: '三级页面',
                   icon: <CrownOutlined />,
                 },
               ],
             },
           ],
         }}
       >
         <div>
           <Outlet />
         </div>
       </ProLayout>
     </div>
   );
 });
 