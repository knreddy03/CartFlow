import { Outlet } from "react-router-dom";

import Header from "../components/layout/Header/Header";
import Footer from "../components/layout/Footer/Footer";

function HomeLayout() {
  return (
    <>
      <Header variant="transparent" />

      <main>
        <Outlet />
      </main>

      <Footer />
    </>
  );
}

export default HomeLayout;
