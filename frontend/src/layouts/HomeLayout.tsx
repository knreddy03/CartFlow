import { Outlet } from "react-router-dom";

import Header from "../components/layout/Header/Header";
import Footer from "../components/layout/Footer/Footer";

function HomeLayout() {
  return (
    <div className="min-h-screen bg-white text-gray-900 antialiased">
      <Header variant="transparent" />

      <main role="main">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}

export default HomeLayout;
