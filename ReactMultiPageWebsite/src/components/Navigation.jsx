import React from "react";
import { Link, withRouter } from "react-router-dom";

function Navigation(props) {
  return (
    <div className="navigation">
      <nav class="navbar navbar-expand navbar-dark bg-dark">
        <div class="container">
          <Link class="navbar-brand" to="/">
            Good Heroes Recommender
          </Link>
          <div>
            <ul class="navbar-nav ml-auto">
              {/* <li
                class={`nav-item  ${
                  props.location.pathname === "/" ? "active" : ""
                }`}
              >
                <Link class="nav-link" to="/">
                  Movies
                  <span class="sr-only">(current)</span>
                </Link>
              </li> */}
              {/* <li
                class={`nav-item  ${
                  props.location.pathname === "/ip" ? "active" : ""
                }`}
              >
                <Link class="nav-link" to="/ip">
                  IPs
                </Link>
              </li> */}
              {/* <li
                class={`nav-item  ${
                  props.location.pathname === "/map" ? "active" : ""
                }`}
              >
                <Link class="nav-link" to="/map">
                  Map
                </Link>
              </li> */}
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default withRouter(Navigation);
