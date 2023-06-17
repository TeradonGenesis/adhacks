import { ThemeProvider } from "@mui/material";

import theme from "./theme";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <div>hello word</div>
    </ThemeProvider>
  );
};

export default App;
