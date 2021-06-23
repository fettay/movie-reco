import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Navigation, Footer, Movie, Ip, Map } from "./components";
function App() {
  return (
    <div className="App">
      <Router>
        <Navigation />
        <Switch>
          <Route path="/movie" exact component={() => <Movie />} />
          <Route path="/" exact component={() => <Ip />} />
          <Route path="/map" exact component={() => <Map />} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
