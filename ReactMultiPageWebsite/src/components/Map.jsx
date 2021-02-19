import React, {Component} from "react";
import axios from 'axios';
import Plot from 'react-plotly.js';
import { Autocomplete } from '@material-ui/lab';
import TextField from "@material-ui/core/TextField";


class Map extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      x: [],
      y: [],
      hover: [],
      autocompleteInput: [],
      selectedVals: []
    };
  }
  
  componentDidMount(){
    axios.get(`http://localhost:1994/map` )
      .then(res => {
        this.setState({x: res.data.x, y: res.data.y, hover: res.data.hover});
      });
      axios.get(`http://localhost:1994/autocomplete` )
      .then(res => {
        this.setState({ autocompleteInput: res.data.results });
      });
  }

  updateSelection(value){
    var index = this.state.hover.indexOf(value);
    if(index > -1)
      this.setState({selectedVals: [index]});
    else
      this.setState({selectedVals: []});
  }

  render(){
    return (
      <div className="home">
        <div class="container">
          <div class="row align-items-center my-5">
            <div class="col-7">
              <Plot
                data={[
                  {
                    x: this.state.x,
                    y: this.state.y,
                    type: 'scatter',
                    mode: 'markers',
                    hovertext: this.state.hover,
                    selectedpoints: this.state.selectedVals
                  }
                ]}
                layout={ {title: 'The movie map'} }
              />
            </div>
            <div class="col-5">
            <Autocomplete
                style={{ width: 300 }}
                options={this.state.autocompleteInput}
                onChange={(str) => this.updateSelection(str.target.textContent)}
                renderInput={(params) => <TextField {...params} label="Movie" variant="outlined" />}/ >
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Map;
