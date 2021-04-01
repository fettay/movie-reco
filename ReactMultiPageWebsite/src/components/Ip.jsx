import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from 'axios';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';


class Ip extends Component {
  constructor (props) {
    super(props);    
    this.state = {
      autocompleteInput: [],
      recommandations: [],
      movieReco: "",
      tags: []
    };
    this.curContent = "";
    this.recoType = "storyline";
  }
  


  getAllRecommandations(){
    axios.post(process.env.REACT_APP_API + "themes", {ip: this.curContent})
    .then(res => {
      this.setState({tags: res.data.results});
      console.log(res.data.results);
    });

    axios.post(process.env.REACT_APP_API + "ip/" + this.recoType, {ip: this.curContent})
    .then(res => {
      this.setState({recommandations: res.data.results});
      console.log(res.data.results);
    });
  }

  handleTypeChange(event, newValue){
    this.recoType = newValue;
    this.getAllRecommandations();
  }

  render(){

    const movies = [];

    this.state.recommandations.forEach(movie => {
      movies.push(<li>{movie}</li>);
    });

    var tags = [];
    this.state.tags.forEach(tag => {
      tags.push(<span class="badge badge-pill badge-primary tags">{tag}</span>)
    });

    return (
      <div className="home">
        <div class="container">
        <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <ToggleButtonGroup
              value={this.recoType}
              exclusive
              onChange={this.handleTypeChange.bind(this)}
              aria-label="text alignment">
              <ToggleButton value="tagline" aria-label="tagline">
                Tagline
              </ToggleButton>
              <ToggleButton value="storyline" aria-label="storyline">
                Storyline
              </ToggleButton>
              <ToggleButton value="synopsis" aria-label="synopsis">
                Synopsis
              </ToggleButton>
            </ToggleButtonGroup>
            </div>
            <div class="row tags-container">
                {tags}
            </div>
          </div>
          <div class="row align-items-center my-5">
            <div class="col-lg-7">
            <TextField fullWidth 
            id="outlined-multiline-static"
            label="Multiline"
            multiline
            rows={10}
            onChange={(val) => this.curContent = val.target.value}
            variant="outlined"
            />
            <Button variant="contained" color="primary" onClick={() => this.getAllRecommandations()}>
              Validate
            </Button>
            </div>
            <div class="col-lg-5">
              <h1 class="font-weight-light">Recommandation for the IP</h1>
              {movies}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Ip;
