import { Outlet } from "react-router-dom";

import Header from "../components/layout/Header/Header";
import Footer from "../components/layout/Footer/Footer";

function MainLayout() {
  return (
    <div className="min-h-screen bg-white text-gray-900 antialiased">
      <Header variant="solid" />

      <main className="min-h-screen pt-16" role="main">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}

export default MainLayout;
